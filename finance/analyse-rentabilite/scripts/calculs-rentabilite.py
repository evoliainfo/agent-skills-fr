#!/usr/bin/env python3
"""Calculs analytiques déterministes, sans dépendances externes. Entrée JSON, sortie JSON."""
import json, math, sys
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
D=Decimal
ZERO=D(0)

def nombre(x, nom, positif=False):
    if isinstance(x,bool) or not isinstance(x,(int,float,Decimal,str)):
        raise ValueError(f'{nom}: nombre requis (absence interdite)')
    try: n=D(str(x))
    except InvalidOperation: raise ValueError(f'{nom}: nombre invalide') from None
    if not n.is_finite() or (positif and n<0): raise ValueError(f'{nom}: nombre fini'+(' non négatif' if positif else '')+' requis')
    if n and abs(n.adjusted())>100: raise ValueError(f'{nom}: ordre de grandeur hors périmètre')
    return n

def lire(o,k,positif=True): return nombre(o.get(k),k,positif)
def ratio(a,b): return a/b if b>0 else None
def liste(o,k):
    v=o.get(k)
    if not isinstance(v,list) or not v: raise ValueError(f'{k}: liste non vide requise')
    if not all(isinstance(r,dict) for r in v): raise ValueError(f'{k}: objets requis')
    return v

def ident(r, vus):
    i=r.get('id')
    if not isinstance(i,str) or not i.strip() or i in vus: raise ValueError('id absent ou dupliqué')
    vus.add(i); return i

def segments(o):
    commun=lire(o,'fixes_communs'); vus=set(); lignes=[]
    for r in liste(o,'segments'):
        i=ident(r,vus); ca=lire(r,'ca'); cv=lire(r,'variables'); fs=lire(r,'fixes_specifiques')
        m=ca-cv
        lignes.append(dict(id=i,ca=ca,variables=cv,fixes_specifiques=fs,mcv=m,taux_mcv=ratio(m,ca),marge_specifique=m-fs))
    total={k:sum((r[k] for r in lignes),ZERO) for k in ('ca','variables','fixes_specifiques','mcv','marge_specifique')}
    total.update(taux_mcv=ratio(total['mcv'],total['ca']),fixes_communs=commun,resultat=total['marge_specifique']-commun)
    return dict(segments=lignes,total=total)

def abc(o):
    vus=set(); centres=[]; par_objet={}
    for r in liste(o,'centres'):
        i=ident(r,vus); cout=lire(r,'cout'); c=r.get('consommations')
        if not isinstance(c,dict) or not all(isinstance(k,str) and k.strip() for k in c): raise ValueError('consommations: objet id -> quantité requis')
        con={k:nombre(v,k,True) for k,v in c.items()}; total=sum(con.values(),ZERO)
        mode=r.get('base')
        if mode not in ('reelle','capacite'): raise ValueError('base: reelle ou capacite requise')
        base=total if mode=='reelle' else lire(r,'capacite')
        if total>base: raise ValueError('consommation supérieure à la capacité')
        taux=ratio(cout,base); imput={k:(v*taux if taux is not None else ZERO) for k,v in con.items()}
        affecte=sum(imput.values(),ZERO); residu=cout-affecte
        for k,v in imput.items(): par_objet[k]=par_objet.get(k,ZERO)+v
        centres.append(dict(id=i,cout=cout,base=base,taux=taux,imputations=imput,cout_impute=affecte,non_impute=residu))
    return dict(centres=centres,par_objet=par_objet,total_couts=sum((r['cout'] for r in centres),ZERO),total_impute=sum(par_objet.values(),ZERO),total_non_impute=sum((r['non_impute'] for r in centres),ZERO))

def seuil(o):
    ca=lire(o,'ca'); cv=lire(o,'variables'); f=lire(o,'fixes'); cible=lire(o,'resultat_cible'); jours=lire(o,'jours')
    if jours<=0: raise ValueError('jours doit être positif')
    m=ca-cv; t=ratio(m,ca); s=None; objectif=None; statut='ca_nul_modele_indetermine'
    if t is not None:
        if t>0: s=f/t; objectif=(f+cible)/t; statut='seuil_calculable'
        elif f>0: statut='aucun_seuil_atteignable'
        elif t==0: statut='equilibre_tous_volumes'
        else: s=ZERO; statut='equilibre_uniquement_volume_nul'
    pm=s/ca*jours if s is not None and ca>0 else None
    return dict(mcv=m,taux_mcv=t,resultat=m-f,seuil_ca=s,ca_cible=objectif,statut=statut,marge_securite=ca-s if s is not None else None,taux_securite=ratio(ca-s,ca) if s is not None else None,point_mort_theorique_jours=pm,hors_periode=pm>jours if pm is not None else None)

def scenarios(o):
    vus=set(); out=[]
    for r in liste(o,'scenarios'):
        i=ident(r,vus); p=lire(r,'prix'); q=lire(r,'volume'); c=lire(r,'cout_variable_unitaire'); f=lire(r,'fixes'); jours=lire(r,'jours'); cible=lire(r,'resultat_cible')
        cap=lire(r,'capacite')
        if q>cap: raise ValueError(f'{i}: volume supérieur à la capacité')
        out.append(dict(id=i,prix=p,volume=q,capacite=cap,**seuil(dict(ca=p*q,variables=c*q,fixes=f,resultat_cible=cible,jours=jours))))
    return dict(scenarios=out)

def decision(o):
    # Tous les montants sont différentiels et positifs, sur le même horizon.
    revenu=lire(o,'revenu_gagne'); perdu=lire(o,'revenu_perdu'); evite=lire(o,'cout_evite'); ajoute=lire(o,'cout_ajoute'); alt=lire(o,'contribution_alternative'); opp=lire(o,'contribution_sacrifiee')
    return dict(variation_resultat=revenu-perdu+evite-ajoute+alt-opp,convention='option moins reference; contribution alternative et sacrifiée hors autres postes')

def prix(o):
    c=lire(o,'cout_variable_unitaire'); t=lire(o,'taux_cible'); a=lire(o,'taux_commission')
    if t>=1 or a>=1 or t+a>=1: raise ValueError('taux cible + taux commission doit être inférieur à 1')
    if c==0: return dict(prix_theorique=None,statut='cout_nul_pas_de_prix_unique')
    return dict(prix_theorique=c/(1-t-a),statut='prix_theorique_hors_contraintes_commerciales')

def capacite(o):
    cap=lire(o,'capacite'); vus=set(); rows=[]
    if o.get('unites_divisibles') is not True or o.get('une_seule_contrainte') is not True: raise ValueError('modèle réservé aux unités divisibles et à une seule contrainte')
    for r in liste(o,'produits'):
        i=ident(r,vus); m=lire(r,'contribution_unitaire',False); h=lire(r,'ressource_unitaire'); d=lire(r,'demande_max')
        if h<=0: raise ValueError('ressource unitaire strictement positive requise')
        rows.append((m/h,i,m,h,d))
    reste=cap; lignes=[]
    for score,i,m,h,d in sorted(rows,key=lambda r:(-r[0],r[1])):
        q=min(d,reste/h) if m>0 else ZERO
        utilise=min(reste,q*h); reste-=utilise
        lignes.append(dict(id=i,quantite=q,ressource=utilise,contribution=q*m,contribution_par_ressource=score))
    return dict(produits=lignes,capacite_restante=reste,total_contribution=sum((r['contribution'] for r in lignes),ZERO))

OPS={'segments':segments,'abc':abc,'seuil':seuil,'scenarios':scenarios,'decision':decision,'prix':prix,'capacite':capacite}
def calculer(o):
    if not isinstance(o,dict) or o.get('operation') not in OPS: raise ValueError('operation inconnue')
    with localcontext() as ctx:
        ctx.prec=34
        return OPS[o['operation']](o)

def encoder(x):
    if isinstance(x,Decimal): return str(x)  # éviter perte de précision; arrondir à la restitution
    raise TypeError(type(x).__name__)

def main():
    try:
        if len(sys.argv)>2: raise ValueError('usage : calculs-rentabilite.py [entree.json]')
        raw=Path(sys.argv[1]).read_text(encoding='utf-8') if len(sys.argv)==2 else sys.stdin.read()
        def unique(pairs):
            obj={}
            for k,v in pairs:
                if k in obj: raise ValueError('clé JSON dupliquée : '+k)
                obj[k]=v
            return obj
        o=json.loads(raw,parse_float=D,object_pairs_hook=unique)
        print(json.dumps(calculer(o),default=encoder,ensure_ascii=False,indent=2,allow_nan=False))
    except (ValueError,TypeError,ArithmeticError,OSError) as e:
        print(json.dumps({'erreur':str(e)},ensure_ascii=False),file=sys.stderr); return 2
    return 0
if __name__=='__main__': sys.exit(main())
