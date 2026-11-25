#!/usr/bin/env python3
"""Calculateur de contrôle budgétaire. JSON en entrée/sortie, bibliothèque standard."""
import json
import sys
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction


def nombre(x, nom):
    if isinstance(x, bool) or not isinstance(x, (int, str, Decimal, float)):
        raise ValueError(f'{nom}: nombre requis, absence interdite')
    try:
        d = Decimal(str(x))
        if not d.is_finite() or abs(d) > Decimal('1e18') or d.as_tuple().exponent < -12:
            raise ValueError(f'{nom}: nombre non fini ou hors précision/plage admise')
        return Fraction(d)
    except (InvalidOperation, OverflowError) as e:
        raise ValueError(f'{nom}: nombre invalide') from e


def champs(d, *cles):
    if not isinstance(d, dict):
        raise ValueError('Objet JSON requis')
    return [nombre(d.get(c), c) for c in cles]


def positif(*xs):
    if any(x < 0 for x in xs):
        raise ValueError('Quantités, activités ou coûts standards négatifs: vérifier le périmètre')


def pont(debut, fin, effets):
    total = fin - debut
    assert sum(effets.values(), Fraction(0)) == total, 'Pont non réconcilié'
    return {'reference': debut, 'reel': fin, 'ecart': total, 'effets': effets, 'reconciliation_exacte': True}


def ecart(d):
    b,r = champs(d,'budget','reel')
    n = d.get('nature')
    if n not in ('produit','charge','marge','resultat','neutre'):
        raise ValueError('nature: produit, charge, marge, resultat ou neutre')
    e = r-b
    impact = None if n == 'neutre' else (-e if n == 'charge' else e)
    return {'budget':b,'reel':r,'ecart':e,'ecart_pct':None if b==0 else e/abs(b)*100,
            'impact_economique':impact,'lecture': 'non qualifie' if impact is None else ('F' if impact>0 else 'D' if impact<0 else 'N')}


def portefeuille(d):
    lignes=d.get('produits')
    if not isinstance(lignes,list) or not lignes:
        raise ValueError('produits: liste non vide requise')
    mix=d.get('mix',False)
    marge=d.get('contribution',False)
    if not isinstance(mix,bool) or not isinstance(marge,bool):
        raise ValueError('mix et contribution: booléens requis')
    ids=set(); donnees=[]; unites=set()
    for l in lignes:
        if not isinstance(l,dict): raise ValueError('Chaque produit doit être un objet')
        ident=l.get('id'); unite=l.get('unite')
        if not isinstance(ident,str) or not ident.strip() or ident in ids: raise ValueError('id produit vide ou dupliqué')
        if not isinstance(unite,str) or not unite.strip(): raise ValueError('unite obligatoire')
        ids.add(ident); unites.add(unite)
        qb,qr,pb,pr=champs(l,'quantite_budget','quantite_reelle','prix_budget','prix_reel')
        positif(qb,qr)
        cb,cr=champs(l,'cout_variable_budget','cout_variable_reel') if marge else (Fraction(0),Fraction(0))
        donnees.append((ident,qb,qr,pb,pr,cb,cr))
    Qb=sum(x[1] for x in donnees); Qr=sum(x[2] for x in donnees)
    if mix and (len(unites)!=1 or Qb<=0 or d.get('unites_comparables') is not True):
        raise ValueError('Mix: unités homogènes confirmées et volume budget strictement positif requis')
    ca_b=ca_r=mc_b=mc_r=Fraction(0)
    ca_e={k:Fraction(0) for k in (('volume','mix','prix') if mix else ('quantite','prix'))}
    mc_e={k:Fraction(0) for k in (*ca_e,'cout_unitaire')}
    details=[]
    for ident,qb,qr,pb,pr,cb,cr in donnees:
        ca_b+=qb*pb; ca_r+=qr*pr; mc_b+=qb*(pb-cb); mc_r+=qr*(pr-cr)
        de={'prix':qr*(pr-pb)}; dm={'prix':de['prix'],'cout_unitaire':qr*(cb-cr)}
        if mix:
            qs=Qr*qb/Qb
            de.update(volume=(qs-qb)*pb,mix=(qr-qs)*pb)
            dm.update(volume=(qs-qb)*(pb-cb),mix=(qr-qs)*(pb-cb))
        else:
            de['quantite']=(qr-qb)*pb; dm['quantite']=(qr-qb)*(pb-cb)
        for k,v in de.items(): ca_e[k]+=v
        for k,v in dm.items(): mc_e[k]+=v
        detail={'id':ident,'chiffre_affaires':pont(qb*pb,qr*pr,de)}
        if marge: detail['contribution']=pont(qb*(pb-cb),qr*(pr-cr),dm)
        details.append(detail)
    out={'chiffre_affaires':pont(ca_b,ca_r,ca_e),'details':details}
    if marge: out['contribution']=pont(mc_b,mc_r,mc_e)
    return out


def flexible(d):
    ab,ar,f,v,r=champs(d,'activite_budget','activite_reelle','fixes_budget','taux_variable_budget','cout_reel')
    positif(ab,ar,f,v)
    b=f+v*ab; bf=f+v*ar
    return {**pont(b,r,{'niveau_activite':bf-b,'depense':r-bf}),'budget_flexible':bf,'convention':'écart de coût, impact résultat de signe opposé'}


def direct(d):
    qs,qr,ps,pr=champs(d,'quantite_standard_autorisee','quantite_reelle','prix_standard','prix_reel')
    positif(qs,qr,ps,pr)
    return {**pont(qs*ps,qr*pr,{'prix_taux':qr*(pr-ps),'consommation':(qr-qs)*ps}),'convention':'écart de coût, impact résultat de signe opposé'}


def indirect(d):
    ab,ar,ap,f,v,r=champs(d,'activite_budget','activite_reelle','activite_preetablie','fixes_budget','taux_variable_budget','cout_reel')
    positif(ab,ar,ap,f,v)
    if ab==0: raise ValueError('Activité budgétée strictement positive requise')
    cs=v+f/ab; bf=f+v*ar
    return {**pont(ap*cs,r,{'depenses':r-bf,'absorption':bf-ar*cs,'rendement':(ar-ap)*cs}),'cout_standard_unitaire':cs,'budget_flexible':bf,'convention':'écart de coût imputé, pas un flux de trésorerie'}


def revision(d):
    b,br,r=champs(d,'budget_initial','reference_revisee','reel')
    return pont(b,r,{'revision':br-b,'operationnel':r-br})


def change(d):
    b,r,tb,tr=champs(d,'budget_local','reel_local','taux_budget','taux_reel')
    if min(tb,tr)<=0: raise ValueError('Taux strictement positifs requis')
    return pont(b*tb,r*tr,{'operationnel':(r-b)*tb,'change':r*(tr-tb)})


MODES={'ecart':ecart,'portefeuille':portefeuille,'budget_flexible':flexible,'cout_direct':direct,'cout_indirect':indirect,'revision':revision,'change':change}


def formater(x):
    if isinstance(x,Fraction):
        with localcontext() as ctx:
            ctx.prec=80
            # Strings to preserve monetary precision; exact internal arithmetic precedes rounding.
            return format((Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal('0.000001')),'f')
    if isinstance(x,dict): return {k:formater(v) for k,v in x.items()}
    if isinstance(x,list): return [formater(v) for v in x]
    return x


def unique(paires):
    d={}
    for k,v in paires:
        if k in d: raise ValueError(f'Clé JSON dupliquée: {k}')
        d[k]=v
    return d


def main():
    try:
        if len(sys.argv)!=2: raise ValueError('Usage: python calculs-budgetaires.py entree.json (ou - pour stdin)')
        if sys.argv[1]=='-': raw=sys.stdin.read()
        else:
            with open(sys.argv[1],encoding='utf-8') as f: raw=f.read()
        d=json.loads(raw,parse_float=Decimal,object_pairs_hook=unique)
        if not isinstance(d,dict) or not isinstance(d.get('mode'),str) or d['mode'] not in MODES:
            raise ValueError('Mode inconnu; modes: '+', '.join(MODES))
        result=MODES[d['mode']](d)
        print(json.dumps({'mode':d['mode'],'precision_affichage':6,'resultat':formater(result)},ensure_ascii=False,allow_nan=False))
    except (ValueError, OSError, TypeError, ArithmeticError) as e:
        print(json.dumps({'erreur':str(e)},ensure_ascii=False),file=sys.stderr); return 2
    return 0


if __name__=='__main__': sys.exit(main())
