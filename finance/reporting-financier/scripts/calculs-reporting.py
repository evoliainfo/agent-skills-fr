"""Calculs de reporting sur données mensuelles normalisées; aucune dépendance externe."""
import argparse, calendar, json, re, sys
from decimal import Decimal, InvalidOperation


def nombre(v):
    if v is None: return None
    if isinstance(v, bool) or not isinstance(v, (str, int, float, Decimal)): raise ValueError('Nombre invalide')
    try: n=Decimal(str(v))
    except InvalidOperation: raise ValueError('Nombre invalide')
    if not n.is_finite(): raise ValueError('Nombre non fini')
    return n


def mois(v):
    if not isinstance(v,str) or not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])',v) or not 1<=int(v[:4])<=9999: raise ValueError('Mois attendu AAAA-MM')
    return int(v[:4])*12+int(v[5:])-1


def periodes(debut,fin):
    a,b=mois(debut),mois(fin)
    if not 0<=b-a<=119: raise ValueError('Intervalle invalide ou supérieur à 120 mois')
    return [f'{i//12:04d}-{i%12+1:02d}' for i in range(a,b+1)]


def ecart(reel,ref,type_indicateur='flux',sens='neutre'):
    if type_indicateur not in ('flux','solde','ratio') or sens not in ('hausse','baisse','neutre'): raise ValueError('Type ou sens invalide')
    a,b=nombre(reel),nombre(ref)
    if a is None or b is None: return {'ecart':None,'pourcentage':None,'points':None,'direction':'indisponible'}
    d=a-b
    direction='neutre' if sens=='neutre' else 'stable' if not d else 'favorable' if (d>0)==(sens=='hausse') else 'defavorable'
    return {'ecart':d,'pourcentage':d/b*100 if b>0 and type_indicateur!='ratio' else None,'points':d if type_indicateur=='ratio' else None,'direction':direction}


def agreger(lignes, debut, fin, type_indicateur, contexte):
    # Une seule série normalisée: même indicateur, scénario, version, périmètre, monnaie et unité.
    requis=('indicateur','scenario','version','perimetre','devise','unite')
    if not isinstance(contexte,dict) or any(not isinstance(contexte.get(k),str) or not contexte[k].strip() for k in requis): raise ValueError('Contexte incomplet')
    if type_indicateur not in ('flux','solde','ratio'): raise ValueError('Type invalide')
    attendus=periodes(debut,fin); index={}
    for l in lignes:
        if any(l.get(k)!=contexte[k] for k in requis): raise ValueError('Contexte incompatible')
        m=l['mois']; mois(m)
        if m in index: raise ValueError('Mois dupliqué')
        if m not in attendus: raise ValueError('Mois hors périmètre')
        index[m]=l
    necessaires=attendus[-1:] if type_indicateur=='solde' else attendus
    manquants=[]; valeurs=[]; denoms=[]
    for m in necessaires:
        l=index.get(m,{})
        if type_indicateur=='ratio':
            n,d=nombre(l.get('numerateur')),nombre(l.get('denominateur'))
            if n is None or d is None or d<0: manquants.append(m); continue
            valeurs.append(n); denoms.append(d)
        else:
            n=nombre(l.get('valeur'))
            if n is None: manquants.append(m); continue
            valeurs.append(n)
    resultat=None
    if not manquants:
        if type_indicateur=='ratio':
            total=sum(denoms,Decimal(0)); resultat=sum(valeurs,Decimal(0))/total*100 if total>0 else None
        else: resultat=sum(valeurs,Decimal(0))
    return {'valeur':resultat,'mois_manquants':manquants,'statut':'calculable' if resultat is not None else 'indisponible'}


def atterrissage(lignes,debut,fin,dernier_cloture,type_indicateur,contexte,version_reel,version_prevision):
    attendus=periodes(debut,fin); borne=mois(dernier_cloture)
    if borne<mois(debut)-1 or borne>mois(fin): raise ValueError('Date de clôture hors exercice')
    if any(not isinstance(v,str) or not v.strip() for v in (version_reel,version_prevision)): raise ValueError('Version manquante')
    selection=[]; vus=set()
    for l in lignes:
        m=l['mois']; mois(m)
        if m not in attendus: raise ValueError('Mois hors exercice')
        if any(l.get(k)!=contexte.get(k) for k in ('indicateur','perimetre','devise','unite')): raise ValueError('Contexte incompatible')
        scenario=l.get('scenario'); attendu='reel' if mois(m)<=borne else 'prevision'
        if scenario not in ('reel','prevision'): raise ValueError('Scénario inconnu')
        if scenario!=attendu: continue
        if l.get('version')!=(version_reel if scenario=='reel' else version_prevision): raise ValueError('Version incompatible')
        if m in vus: raise ValueError('Mois dupliqué')
        vus.add(m)
        if scenario=='reel' and l.get('statut')!='cloture': raise ValueError('Réalisé non clôturé')
        selection.append(dict(l,scenario='atterrissage',version='combinee'))
    resultat=agreger(selection,debut,fin,type_indicateur,dict(contexte,scenario='atterrissage',version='combinee'))
    resultat['mois_reels']=[m for m in attendus if mois(m)<=borne]
    resultat['mois_previsionnels']=[m for m in attendus if mois(m)>borne]
    return resultat


def pont(depart,arrivee,effets,tolerance='0.01'):
    a,b,t=nombre(depart),nombre(arrivee),nombre(tolerance)
    if a is None or b is None or t is None or t<0: raise ValueError('Entrées du pont invalides')
    if not isinstance(effets,dict): raise ValueError('Effets attendus sous forme de dictionnaire')
    valeurs=[nombre(v) for v in effets.values()]
    if any(v is None for v in valeurs): raise ValueError('Effet manquant')
    somme=sum(valeurs,Decimal(0)); residu=b-a-somme
    return {'ecart_total':b-a,'somme_effets':somme,'residu':residu,'reconcilie':abs(residu)<=t}


def main():
    p=argparse.ArgumentParser(); p.add_argument('fichier'); args=p.parse_args()
    try:
        with open(args.fichier,encoding='utf-8') as f: data=json.load(f,parse_float=Decimal)
        op=data['operation']; params=data['parametres']; fonctions={'ecart':ecart,'agreger':agreger,'atterrissage':atterrissage,'pont':pont}
        resultat=fonctions[op](**params)
        print(json.dumps(resultat,ensure_ascii=False,default=str,allow_nan=False))
    except (ValueError,KeyError,TypeError,OSError,ArithmeticError) as e:
        print(json.dumps({'erreur':str(e)},ensure_ascii=False),file=sys.stderr); return 1
    return 0

if __name__=='__main__': sys.exit(main())
