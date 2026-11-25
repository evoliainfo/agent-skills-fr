# Calculateur budgétaire

Python 3.9+ avec bibliothèque standard seulement. Le script ne se connecte à aucun service, ne modifie aucun fichier source et ne lit que le JSON explicitement fourni. Construire l'entrée après contrôle des données, jamais en substituant zéro aux absences.

Exécution : `python scripts/calculs-budgetaires.py entree.json` (ou `-` pour stdin). Sortie JSON sur stdout; erreurs sur stderr, code 2. Les nombres de résultat sont des chaînes décimales à six décimales; les ponts sont réconciliés en fractions exactes avant arrondi. Au moment de restituer en euros, expliquer les éventuels écarts d'arrondi. Les limites numériques d'entrée sont ±10^18 et 12 décimales. Le script ne valide pas la comparabilité des sources ou la qualité du mapping : ces contrôles restent obligatoires.

## Modes et paramètres

| mode | Champs numériques requis |
|---|---|
| ecart | budget, reel; nature = produit/charge/marge/resultat/neutre |
| budget_flexible | activite_budget, activite_reelle, fixes_budget, taux_variable_budget, cout_reel |
| cout_direct | quantite_standard_autorisee, quantite_reelle, prix_standard, prix_reel |
| cout_indirect | activite_budget, activite_reelle, activite_preetablie, fixes_budget, taux_variable_budget, cout_reel |
| revision | budget_initial, reference_revisee, reel |
| change | budget_local, reel_local, taux_budget, taux_reel |
| portefeuille | produits (liste), mix (booléen), contribution (booléen), unites_comparables (true si mix confirmé) |

Chaque produit comporte `id`, `unite`, `quantite_budget`, `quantite_reelle`, `prix_budget`, `prix_reel`. Si contribution=true, ajouter `cout_variable_budget`, `cout_variable_reel`. Si mix=false, les effets quantité sont calculés par produit, sans agréger les unités physiques. Une ligne dont le prix de référence est absent doit être traitée séparément, sans fabriquer de standard. Les quantités nettes négatives ne sont pas acceptées par ce mode.

Exemple :
```json
{"mode":"portefeuille","mix":true,"contribution":true,"unites_comparables":true,"produits":[{"id":"A","unite":"piece","quantite_budget":100,"quantite_reelle":150,"prix_budget":10,"prix_reel":11,"cout_variable_budget":6,"cout_variable_reel":7},{"id":"B","unite":"piece","quantite_budget":100,"quantite_reelle":100,"prix_budget":20,"prix_reel":19,"cout_variable_budget":12,"cout_variable_reel":11}]}
```
CA +550; contribution +200; voir détail des effets dans `prix-volume-mix.md`.

Les autres méthodes décrites dans les références (mix matière, calendrier, projection d'atterrissage, traitement des entrées/sorties) ne sont pas des modes autonomes du script; les appliquer explicitement si les données le permettent, en contrôlant leur réconciliation. Une erreur du script n'autorise pas à inventer un résultat. Si Python n'est pas disponible, calculer les identités sur les opérandes connus et préciser le mode de calcul utilisé.
