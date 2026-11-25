#!/usr/bin/env python3
"""Calculs déterministes sur agrégats normalisés. Aucun accès réseau."""
import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, localcontext

CHAMPS = set('''ventes_marchandises cout_marchandises production_vendue production_stockee production_immobilisee consommations_tiers subventions_exploitation impots_exploitation charges_personnel autres_produits_exploitation reprises_exploitation autres_charges_exploitation dotations_exploitation resultat_financier quote_part_operations_communes resultat_exceptionnel participation impot_benefices ca_ht ebe resultat_exploitation resultat_net total_actif total_passif dotations_totales reprises_totales vnc_cessions produits_cessions quote_part_subventions_investissement ressources_stables emplois_stables actif_exploitation passif_exploitation actif_hors_exploitation passif_hors_exploitation tresorerie_active tresorerie_passive capitaux_propres capitaux_propres_ouverture actif_ouverture dette_financiere_brute liquidites_disponibles charges_interets actifs_court_terme passifs_court_terme stocks_court_terme creances_clients_ttc ca_ttc dettes_fournisseurs_ttc achats_concernes_ttc resultat_operationnel_apres_impot capitaux_employes_ouverture capitaux_employes_cloture'''.split())
POSITIFS = set('''dotations_totales reprises_totales vnc_cessions produits_cessions quote_part_subventions_investissement total_actif total_passif dette_financiere_brute liquidites_disponibles charges_interets actifs_court_terme passifs_court_terme stocks_court_terme creances_clients_ttc dettes_fournisseurs_ttc actif_ouverture tresorerie_active tresorerie_passive'''.split())

def nombre(v):
    if v is None: return None
    if isinstance(v, bool) or not isinstance(v, (int, float, str, Decimal)):
        raise ValueError('Valeur numérique attendue')
    try: x = Decimal(str(v))
    except InvalidOperation: raise ValueError('Nombre décimal invalide') from None
    if not x.is_finite() or abs(x) > Decimal('1e30'):
        raise ValueError('Nombre non fini ou hors plage')
    return x

def periode(p):
    if not isinstance(p, dict): raise ValueError('Période invalide')
    lib, dev, jours = p.get('libelle'), p.get('devise'), p.get('jours')
    if not isinstance(lib,str) or not lib.strip() or not isinstance(dev,str) or not dev.strip() or type(jours) is not int or not 1 <= jours <= 3660:
        raise ValueError('Libellé, devise et durée en jours requis')
    unite=p.get('unite', 'unite_monetaire')
    if not isinstance(unite,str) or not unite.strip(): raise ValueError('Unité invalide')
    comp = p.get('comparabilite_precedente', False)
    if type(comp) is not bool: raise ValueError('comparabilite_precedente doit être booléen')
    tol = nombre(p.get('tolerance',0))
    if tol is None or tol < 0: raise ValueError('Tolérance invalide')
    brut = p.get('donnees')
    if not isinstance(brut,dict): raise ValueError('donnees doit être un objet')
    if set(brut)-CHAMPS: raise ValueError('Champs inconnus : '+', '.join(sorted(set(brut)-CHAMPS)))
    d={k:nombre(v) for k,v in brut.items()}
    for k in POSITIFS:
        if d.get(k) is not None and d[k]<0: raise ValueError(f'{k} ne peut pas être négatif dans cette convention')
    r={}; m={}; controles={}; alertes=[]
    def val(k): return r[k] if k in r else d.get(k)
    def calcul(k, deps, f):
        absents=[x for x in deps if val(x) is None]
        if absents: r[k]=None; m[k]={'raison':'donnees_manquantes_ou_contestees','champs':absents}; return None
        r[k]=f(*[val(x) for x in deps]); return r[k]
    def controle(k,a,b):
        if a is None or b is None: controles[k]={'statut':'non_verifiable'}; return None
        ecart=a-b
        statut='exact' if not ecart else ('approxime' if abs(ecart)<=tol else 'incoherent')
        controles[k]={'statut':statut,'ecart':ecart,'tolerance':tol}
        if statut=='incoherent': alertes.append(k+' : incohérence à résoudre')
        return statut
    def rapproche(k,deps,f):
        publie=d.get(k); calc=calcul(k,deps,f)
        statut=controle('rapprochement_'+k,calc,publie)
        if statut=='incoherent': r[k]=None; m[k]={'raison':'agregat_conteste','champs':deps}; return
        if publie is not None:
            r[k]=publie; m.pop(k,None)
    def ratio(k,n,den,facteur=1,condition=True,raison='denominateur_non_positif_ou_condition_non_remplie'):
        a,b=val(n),val(den)
        if a is None or b is None:
            r[k]=None; m[k]={'raison':'donnees_manquantes_ou_contestees','champs':[x for x in (n,den) if val(x) is None]}
        elif b<=0 or not condition:
            r[k]=None; m[k]={'raison':raison,'champs':[n,den]}
        else:r[k]=a/b*facteur
    rapproche('ca_ht',['ventes_marchandises','production_vendue'],lambda a,b:a+b)
    calcul('marge_commerciale',['ventes_marchandises','cout_marchandises'],lambda a,b:a-b)
    calcul('production_exercice',['production_vendue','production_stockee','production_immobilisee'],lambda a,b,c:a+b+c)
    calcul('valeur_ajoutee',['marge_commerciale','production_exercice','consommations_tiers'],lambda a,b,c:a+b-c)
    rapproche('ebe',['valeur_ajoutee','subventions_exploitation','impots_exploitation','charges_personnel'],lambda a,b,c,e:a+b-c-e)
    rapproche('resultat_exploitation',['ebe','autres_produits_exploitation','reprises_exploitation','autres_charges_exploitation','dotations_exploitation'],lambda a,b,c,e,f:a+b+c-e-f)
    calcul('resultat_courant_avant_impot',['resultat_exploitation','resultat_financier','quote_part_operations_communes'],lambda a,b,c:a+b+c)
    rapproche('resultat_net',['resultat_courant_avant_impot','resultat_exceptionnel','participation','impot_benefices'],lambda a,b,c,e:a+b-c-e)
    # A material contradiction in an upstream aggregate invalidates downstream derived result/CAF, even if an independent published amount exists.
    chaine=['ebe','resultat_exploitation','resultat_courant_avant_impot','resultat_net']
    conteste=False
    for k in chaine:
        conteste=conteste or m.get(k,{}).get('raison')=='agregat_conteste'
        if conteste: r[k]=None; m[k]={'raison':'chaine_de_resultat_contestee','champs':[]}
    calcul('caf',['resultat_net','dotations_totales','reprises_totales','vnc_cessions','produits_cessions','quote_part_subventions_investissement'],lambda a,b,c,e,f,g:a+b-c+e-f-g)
    calcul('frng',['ressources_stables','emplois_stables'],lambda a,b:a-b)
    calcul('bfre',['actif_exploitation','passif_exploitation'],lambda a,b:a-b)
    calcul('bfrhe',['actif_hors_exploitation','passif_hors_exploitation'],lambda a,b:a-b)
    calcul('bfr',['bfre','bfrhe'],lambda a,b:a+b)
    calcul('tresorerie_nette_fonctionnelle',['frng','bfr'],lambda a,b:a-b)
    calcul('tresorerie_nette_directe',['tresorerie_active','tresorerie_passive'],lambda a,b:a-b)
    statut=controle('identite_tresorerie',val('tresorerie_nette_fonctionnelle'),val('tresorerie_nette_directe'))
    bilan=controle('equilibre_bilan_comptable',val('total_actif'),val('total_passif'))
    if statut=='incoherent' or bilan=='incoherent':
        for k in ['frng','bfre','bfrhe','bfr','tresorerie_nette_fonctionnelle','tresorerie_nette_directe']:
            r[k]=None; m[k]={'raison':'bilan_ou_retraitements_contestes','champs':[]}
    calcul('dette_nette',['dette_financiere_brute','liquidites_disponibles'],lambda a,b:a-b)
    calcul('capitaux_propres_moyens',['capitaux_propres_ouverture','capitaux_propres'],lambda a,b:(a+b)/2)
    calcul('actif_moyen',['actif_ouverture','total_actif'],lambda a,b:(a+b)/2)
    calcul('capitaux_employes_moyens',['capitaux_employes_ouverture','capitaux_employes_cloture'],lambda a,b:(a+b)/2)
    calcul('actifs_rapides',['actifs_court_terme','stocks_court_terme'],lambda a,b:a-b)
    if val('actifs_rapides') is not None and val('actifs_rapides')<0:
        r['actifs_rapides']=None; m['actifs_rapides']={'raison':'stocks_superieurs_actifs_ct','champs':[]}; alertes.append('Stocks supérieurs aux actifs à court terme')
    def positif(k): return val(k) is not None and val(k)>0
    for k,n,den,f in [('marge_ebe_pct','ebe','ca_ht',100),('taux_marge_ebe_va_pct','ebe','valeur_ajoutee',100),('marge_operationnelle_pct','resultat_exploitation','ca_ht',100),('marge_nette_pct','resultat_net','ca_ht',100),('bfr_jours_ca','bfr','ca_ht',jours),('delai_clients_jours','creances_clients_ttc','ca_ttc',jours),('delai_fournisseurs_jours','dettes_fournisseurs_ttc','achats_concernes_ttc',jours),('autonomie_financiere_pct','capitaux_propres','total_actif',100),('gearing','dette_nette','capitaux_propres',1),('couverture_interets','resultat_exploitation','charges_interets',1),('liquidite_generale','actifs_court_terme','passifs_court_terme',1),('liquidite_reduite','actifs_rapides','passifs_court_terme',1)]:
        ratio(k,n,den,f,condition=(bilan!='incoherent' or k in ('marge_ebe_pct','taux_marge_ebe_va_pct','marge_operationnelle_pct','marge_nette_pct','couverture_interets')),raison='bilan_conteste_ou_denominateur_non_positif')
    ratio('dette_nette_sur_caf_annees','dette_nette','caf',condition=(bilan!='incoherent' and 365<=jours<=366 and val('dette_nette') is not None and val('dette_nette')>=0),raison='periode_non_annuelle_dette_nette_negative_ou_caf_non_positive')
    ratio('roe_pct','resultat_net','capitaux_propres_moyens',100,condition=(bilan!='incoherent' and positif('capitaux_propres') and positif('capitaux_propres_ouverture')))
    ratio('roa_pct','resultat_net','actif_moyen',100,condition=(bilan!='incoherent' and positif('total_actif') and positif('actif_ouverture')))
    ratio('roce_pct','resultat_operationnel_apres_impot','capitaux_employes_moyens',100,condition=(bilan!='incoherent' and positif('capitaux_employes_ouverture') and positif('capitaux_employes_cloture')))
    for k, msg in [('capitaux_propres','Capitaux propres non positifs'),('caf','CAF non positive'),('tresorerie_nette_fonctionnelle','Trésorerie nette non positive')]:
        if val(k) is not None and val(k)<=0: alertes.append(msg)
    if not 365<=jours<=366: alertes.append('Période non annuelle selon la convention du calculateur ; ratios de résultat non annualisés')
    return {'libelle':lib,'devise':dev,'unite':unite,'jours':jours,'comparabilite_precedente':comp,'indicateurs':r,'indisponibles':m,'controles':controles,'alertes':alertes}

def analyser(payload):
    if not isinstance(payload,dict) or not isinstance(payload.get('periodes'),list) or not payload['periodes']:
        raise ValueError('Liste periodes non vide requise')
    with localcontext() as ctx:
        ctx.prec=40
        ps=[periode(p) for p in payload['periodes']]
        if len({p['libelle'] for p in ps})!=len(ps): raise ValueError('Libellés de périodes dupliqués')
        comparaisons=[]
        for a,b in zip(ps,ps[1:]):
            c={'de':a['libelle'],'a':b['libelle'],'statut':'non_comparable','ecarts':{}}
            if b['comparabilite_precedente'] and a['devise']==b['devise'] and a['unite']==b['unite'] and (a['jours']==b['jours'] or {a['jours'],b['jours']}=={365,366}):
                c['statut']='comparable_selon_entree'
                for k in ('ca_ht','ebe','resultat_net','caf','frng','bfr','tresorerie_nette_fonctionnelle','marge_ebe_pct','marge_nette_pct'):
                    x,y=a['indicateurs'].get(k),b['indicateurs'].get(k)
                    if x is None or y is None: continue
                    item={'ecart_points' if k.endswith('_pct') else 'ecart_absolu':y-x}
                    if not k.endswith('_pct'): item['variation_pct']=(y-x)/x*100 if x>0 else None
                    c['ecarts'][k]=item
            comparaisons.append(c)
        return {'periodes':ps,'comparaisons':comparaisons,'note':'Calculs sur données normalisées, non certification des sources.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('fichier'); args=parser.parse_args()
    try:
        with open(args.fichier,encoding='utf-8') as f: data=json.load(f,parse_float=Decimal)
        print(json.dumps(analyser(data),ensure_ascii=False,indent=2,default=str,allow_nan=False))
    except (ValueError, OSError, ArithmeticError) as e:
        print('Erreur : '+str(e),file=sys.stderr); return 2
    return 0
if __name__=='__main__': sys.exit(main())
