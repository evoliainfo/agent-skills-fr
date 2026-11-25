# Utilisation du calculateur intégré

Python 3.9+, bibliothèque standard, aucun réseau. Le calculateur ne lit pas directement des PDF, balances ou FEC : il reçoit des valeurs normalisées, dont le mapping et la provenance sont contrôlés par l'assistant. Enregistrer un JSON temporaire, lancer `python scripts/calculs-financiers.py donnees.json` depuis le dossier du skill (ou utiliser son chemin absolu). La sortie JSON contient les indicateurs, les champs manquants, les contrôles et les alertes. Les nombres en sortie sont des chaînes décimales (précision conservée). Les ratios suffixés `_pct` sont exprimés en pourcentage, les autres en coefficient ou jours selon le nom. Ne pas confondre résultat du calcul et données validées.

## Entrée
Objet avec `periodes` (liste chronologique non vide). Chaque période : `libelle` unique, `devise`, `unite` (facultatif : `unite_monetaire` par défaut ; renseigner `kEUR` si milliers), `jours` entier positif, `comparabilite_precedente` (true uniquement après vérification des durées, référentiel, périmètre et devise), `tolerance` (montant dans l'unité commune, 0 par défaut), `donnees` (objet). Tous les montants dans une unité homogène par période et entre périodes comparées (le calculateur bloque les comparaisons si les unités déclarées diffèrent), par exemple EUR. Les clés inconnues sont rejetées ; valeurs absentes ou nulles ne sont pas calculées. Montants en nombre JSON ou chaîne décimale simple, jamais séparateur de milliers. Ne pas mettre zéro pour compléter une liste. Si l'exercice n'est pas annuel, le ratio dette/CAF n'est pas exprimé en années. Charges ordinaires positives ; soldes de résultats et variations signés. Les ratios de structure utilisent les valeurs nettes comptables, distinctes des agrégats fonctionnels.

### Champs de `donnees`
- Activité : `ventes_marchandises`, `cout_marchandises`, `production_vendue`, `production_stockee`, `production_immobilisee`, `consommations_tiers`, `subventions_exploitation`, `impots_exploitation`, `charges_personnel`, `autres_produits_exploitation`, `reprises_exploitation`, `autres_charges_exploitation`, `dotations_exploitation`, `resultat_financier`, `quote_part_operations_communes`, `resultat_exceptionnel`, `participation`, `impot_benefices`.
- Agrégats publiés indépendants : `ca_ht`, `ebe`, `resultat_exploitation`, `resultat_net`, `total_actif`, `total_passif`. Si agrégat calculé et publié divergent, signaler et ne pas utiliser le résultat contesté dans les ratios.
- CAF : `dotations_totales`, `reprises_totales`, `vnc_cessions`, `produits_cessions`, `quote_part_subventions_investissement` (montants positifs ; zéro seulement si absence confirmée). Autres retraitements non pris en charge automatiquement : les documenter séparément.
- Fonctionnel : `ressources_stables`, `emplois_stables`, `actif_exploitation`, `passif_exploitation`, `actif_hors_exploitation`, `passif_hors_exploitation`, `tresorerie_active`, `tresorerie_passive`.
- Ratios : `capitaux_propres`, `capitaux_propres_ouverture`, `actif_ouverture`, `dette_financiere_brute`, `liquidites_disponibles`, `charges_interets`, `actifs_court_terme`, `passifs_court_terme`, `stocks_court_terme`, `creances_clients_ttc`, `ca_ttc`, `dettes_fournisseurs_ttc`, `achats_concernes_ttc`, `resultat_operationnel_apres_impot`, `capitaux_employes_ouverture`, `capitaux_employes_cloture`.

## Exemple minimal
```json
{"periodes":[{"libelle":"2025","devise":"EUR","jours":365,"donnees":{"ca_ht":1300000,"ebe":90000,"resultat_net":42000}}]}
```
Marge EBE 6,923... %, marge nette 3,230... %. Le BFR et la CAF sont indisponibles. Le rapport ne prétend pas que les comptes sont rapprochés. Un contrôle « non_verifiable » n'est pas une réussite.
