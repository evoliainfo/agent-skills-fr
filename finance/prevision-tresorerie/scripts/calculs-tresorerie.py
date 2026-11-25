#!/usr/bin/env python3
"""Projection de caisse déterministe, bibliothèque standard uniquement."""
import json, sys, re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from collections import defaultdict
from pathlib import Path


def montant(v, champ, negatif=False, nullable=False):
    if v is None and nullable: return None
    if isinstance(v, bool) or not isinstance(v, (str, int, Decimal)):
        raise ValueError(f'{champ}: montant décimal attendu')
    try: d=Decimal(v)
    except InvalidOperation: raise ValueError(f'{champ}: montant invalide') from None
    if not d.is_finite() or abs(d)>Decimal('100000000000000') or (not negatif and d<0):
        raise ValueError(f'{champ}: montant hors limites')
    c=d*100
    if c!=c.to_integral_value(): raise ValueError(f'{champ}: précision maximale de deux décimales')
    return int(c)


def fmt(c):
    return None if c is None else f'{Decimal(c)/100:.2f}'


def jour(v, champ, nullable=False):
    if v is None and nullable: return None
    if not isinstance(v,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',v): raise ValueError(f'{champ}: date AAAA-MM-JJ attendue')
    return date.fromisoformat(v)


def texte(v, champ):
    if not isinstance(v,str) or not v.strip(): raise ValueError(f'{champ}: texte non vide requis')
    return v.strip()


def objet(v, champ):
    if not isinstance(v,dict): raise ValueError(f'{champ}: objet attendu')
    return v


def liste(v, champ):
    if not isinstance(v,list): raise ValueError(f'{champ}: liste attendue')
    return v


def champs(v, requis, facultatifs, champ):
    objet(v,champ)
    manque=set(requis)-v.keys(); surplus=v.keys()-set(requis)-set(facultatifs)
    if manque or surplus: raise ValueError(f'{champ}: champs manquants {sorted(manque)}, inconnus {sorted(surplus)}')


def flux_brut(f):
    champs(f,['id','sens','categorie','date','montant','source','nature'],[], 'flux')
    ident=texte(f['id'],'id'); sens=f['sens']; nature=f['nature']
    if sens not in ('entree','sortie'): raise ValueError(f'{ident}: sens invalide')
    if nature not in ('confirme','engage','estime'): raise ValueError(f'{ident}: nature invalide')
    return dict(id=ident,sens=sens,categorie=texte(f['categorie'],'categorie'),date=jour(f['date'],'date',True),montant=montant(f['montant'],'montant',nullable=True),source=texte(f['source'],'source'),nature=nature)


def index_flux(rows):
    out={}
    for f in liste(rows,'flux'):
        r=flux_brut(f)
        if r['id'] in out: raise ValueError(f"id de flux en double : {r['id']}")
        out[r['id']]=r
    return out


def serial_flux(f, raison):
    return {**f,'date':f['date'].isoformat() if f['date'] else None,'montant':fmt(f['montant']),'raison':raison}


def variante(base, v):
    champs(v,['nom','hypothese','modifications'],['ajouts'],'scenario')
    nom=texte(v['nom'],'nom'); hypothese=texte(v['hypothese'],'hypothese')
    out={k:x.copy() for k,x in base.items()}; vus=set(); annules=[]
    for m in liste(v['modifications'],'modifications'):
        champs(m,['id','motif'],['date','montant','annuler'],'modification')
        i=texte(m['id'],'id'); motif=texte(m['motif'],'motif')
        if i not in base or i in vus: raise ValueError(f'modification inconnue ou répétée : {i}')
        vus.add(i)
        if 'annuler' in m:
            if m['annuler'] is not True or 'date' in m or 'montant' in m: raise ValueError('annulation incompatible avec une autre modification')
            annules.append({'id':i,'motif':motif}); del out[i]; continue
        if 'date' not in m and 'montant' not in m: raise ValueError('modification vide')
        if 'date' in m: out[i]['date']=jour(m['date'],'date',True)
        if 'montant' in m: out[i]['montant']=montant(m['montant'],'montant',nullable=True)
        out[i]['nature']='estime'; out[i]['source'] += f' | scénario : {motif}'
    for i,f in index_flux(v.get('ajouts',[])).items():
        if i in base: raise ValueError(f'ajout avec id déjà utilisé : {i}')
        out[i]=f
    return nom,hypothese,out,annules


def projection(base, arrete, horizon, solde, seuil, couverture, manquants):
    debut=arrete+timedelta(days=1); fin=arrete+timedelta(days=horizon)
    parjour=defaultdict(list); hors=[]; non_resolus=[]
    for f in base.values():
        d=f['date']; m=f['montant']
        if d is not None and d>fin:
            hors.append(serial_flux(f,'apres_horizon')); continue
        if d is None or m is None or d<=arrete:
            raisons=[]
            if d is None: raisons.append('date_absente')
            if m is None: raisons.append('montant_absent')
            if d is not None and d<=arrete: raisons.append('date_passee_a_reconcilier')
            non_resolus.append(serial_flux(f,';'.join(raisons))); continue
        parjour[d].append(f)
    partielle=couverture=='partielle' or bool(non_resolus) or bool(manquants) or solde is None
    cumul=0; courant=solde; min_solde=solde; date_min=arrete if solde is not None else None
    premiere_negative=arrete if solde is not None and solde<0 else None
    premiere_seuil=arrete if seuil is not None and solde is not None and solde<seuil else None
    jours=[]; semaines=[]; categories=defaultdict(lambda:[0,0]); tot_e=tot_s=0
    for k in range(horizon):
        d=debut+timedelta(days=k); e=s=0; parcat=defaultdict(lambda:[0,0])
        for f in parjour[d]:
            i=0 if f['sens']=='entree' else 1
            categories[f['categorie']][i]+=f['montant']; parcat[f['categorie']][i]+=f['montant']
            if i==0: e+=f['montant']
            else: s+=f['montant']
        avant=courant; net=e-s; cumul+=net; tot_e+=e; tot_s+=s
        if courant is not None:
            courant+=net
            if courant<min_solde: min_solde=courant; date_min=d
            if courant<0 and premiere_negative is None: premiere_negative=d
            if seuil is not None and courant<seuil and premiere_seuil is None: premiere_seuil=d
        jours.append(dict(date=d.isoformat(),ouverture=fmt(avant),encaissements=fmt(e),decaissements=fmt(s),flux_net=fmt(net),cumul_net=fmt(cumul),cloture=fmt(courant),categories={c:{'encaissements':fmt(a),'decaissements':fmt(b)} for c,(a,b) in sorted(parcat.items())},ids=[f['id'] for f in parjour[d]]))
        if k%7==0: we=ws=0; wouv=avant; wd=d
        we+=e; ws+=s
        if k%7==6 or k==horizon-1:
            semaines.append(dict(semaine=len(semaines)+1,debut=wd.isoformat(),fin=d.isoformat(),ouverture=fmt(wouv),encaissements=fmt(we),decaissements=fmt(ws),flux_net=fmt(we-ws),cloture=fmt(courant)))
    iso=lambda d:d.isoformat() if d else None
    assert tot_e-tot_s==cumul and (solde is None or courant-solde==cumul)
    return dict(statut='partielle' if partielle else 'complete_selon_declaration',debut=debut.isoformat(),fin=fin.isoformat(),solde_initial=fmt(solde),seuil=fmt(seuil),encaissements=fmt(tot_e),decaissements=fmt(tot_s),flux_net=fmt(cumul),solde_final=fmt(courant),minimum_cloture=fmt(min_solde),date_minimum=iso(date_min),premiere_date_negative=iso(premiere_negative),premiere_date_sous_seuil=iso(premiere_seuil),deficit_maximal_au_seuil=fmt(max(0,seuil-min_solde)) if seuil is not None and min_solde is not None else None,deficit_maximal_a_zero=fmt(max(0,-min_solde)) if min_solde is not None else None,jours=jours,semaines=semaines,categories={c:{'encaissements':fmt(a),'decaissements':fmt(b)} for c,(a,b) in sorted(categories.items())},flux_non_resolus=non_resolus,flux_hors_horizon=hors,donnees_manquantes=manquants,flux_dans_horizon=[serial_flux(f,'inclus') for d in sorted(parjour) for f in parjour[d]])


def calculer(data):
    champs(data,['arrete','devise','solde_initial','couverture','flux'],['seuil','horizon_jours','donnees_manquantes','scenarios'],'entree')
    arrete=jour(data['arrete'],'arrete'); devise=data['devise']
    if not isinstance(devise,str) or not re.fullmatch('[A-Z]{3}',devise): raise ValueError('devise : code à trois lettres attendu')
    horizon=data.get('horizon_jours',91)
    if type(horizon)!=int or not 1<=horizon<=366: raise ValueError('horizon_jours : entier entre 1 et 366')
    solde=montant(data['solde_initial'],'solde_initial',negatif=True,nullable=True); seuil=montant(data.get('seuil'),'seuil',nullable=True)
    couverture=data['couverture']
    if couverture not in ('complete','partielle'): raise ValueError('couverture invalide')
    manquants=[texte(x,'donnee manquante') for x in liste(data.get('donnees_manquantes',[]),'donnees_manquantes')]
    base=index_flux(data['flux']); out={'devise':devise,'arrete':arrete.isoformat(),'horizon_jours':horizon,'central':projection(base,arrete,horizon,solde,seuil,couverture,manquants),'scenarios':[]}
    noms={'central'}
    for v in liste(data.get('scenarios',[]),'scenarios'):
        nom,hyp,flows,ann=variante(base,v)
        if nom.casefold() in noms: raise ValueError('nom de scénario en double')
        noms.add(nom.casefold())
        out['scenarios'].append({'nom':nom,'hypothese':hyp,'annulations':ann,'projection':projection(flows,arrete,horizon,solde,seuil,couverture,manquants)})
    return out


def main():
    if len(sys.argv)!=2:
        print('Usage : python calculs-tresorerie.py entree.json',file=sys.stderr); return 2
    try:
        def paires(ps):
            out={}
            for k,v in ps:
                if k in out: raise ValueError(f'clé JSON dupliquée : {k}')
                out[k]=v
            return out
        data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'),parse_float=Decimal,object_pairs_hook=paires)
        result=calculer(data)
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (ValueError,TypeError,OverflowError,OSError,InvalidOperation) as exc:
        print(f'Entrée invalide : {exc}',file=sys.stderr); return 1

if __name__=='__main__': sys.exit(main())
