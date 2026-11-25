# Utilisation du calculateur

Le script `scripts/calculs-rentabilite.py` utilise Python 3 et la bibliothèque standard. Il ne lit ni Excel ni PDF directement : extraire les données avec les outils du contexte, les rapprocher et créer un JSON local temporaire. Exécuter `python3 scripts/calculs-rentabilite.py entree.json` depuis le dossier du skill (ou utiliser le chemin absolu). Il accepte aussi le JSON sur stdin. Sortie JSON, valeurs Decimal sérialisées en chaînes numériques pour préserver la précision ; `null` = non calculable. Code retour 2 et message stderr si entrée invalide. Ne pas modifier les données originales. Arrondir uniquement à la restitution et vérifier les résidus à la précision appropriée (centime ou unité de présentation).

Toutes les valeurs monétaires doivent être dans la même devise, période et convention fiscale. Les champs numériques sont obligatoires ; zéro doit être explicite et justifié. Les quantités et coûts sont non négatifs sauf la contribution unitaire de l'opération capacité. Les données de retours et avoirs doivent être agrégées correctement avant passage au script. Les taux sont des fractions (0.25 = 25 %). Chaque opération est indépendante : ne pas sommer deux sorties qui couvrent les mêmes coûts.

## Exemples JSON originaux (illustratifs)

### Cascade de marges
```json
{"operation":"segments","fixes_communs":30000,"segments":[{"id":"A","ca":100000,"variables":60000,"fixes_specifiques":15000},{"id":"B","ca":80000,"variables":50000,"fixes_specifiques":10000}]}
```
Résultat 15000 ; MCV globale 70000. Fournir les coûts variables exhaustifs et fixes spécifiques sans doublon.

### ABC
```json
{"operation":"abc","centres":[{"id":"preparation","cout":12000,"base":"capacite","capacite":400,"consommations":{"A":240,"B":60}}]}
```
Coût imputé 9000, non imputé 3000. Pour base réelle, `base:"reelle"` et omettre `capacite`. L'outil ne classe pas les coûts fixes/variables ni ne traite les prestations croisées.

### Seuil
```json
{"operation":"seuil","ca":150000,"variables":90000,"fixes":45000,"resultat_cible":15000,"jours":365}
```
Seuil 112500, CA cible 150000, résultat 15000. Le point mort est théorique sous activité uniforme.

### Scénarios mono-produit
```json
{"operation":"scenarios","scenarios":[{"id":"central","prix":100,"volume":1000,"cout_variable_unitaire":60,"fixes":30000,"resultat_cible":0,"jours":365,"capacite":1200},{"id":"baisse","prix":90,"volume":1050,"cout_variable_unitaire":60,"fixes":30000,"resultat_cible":0,"jours":365,"capacite":1200}]}
```
Résultats 10000 et 1500. La demande n'est pas prédite par le calculateur ; le volume est une hypothèse.

### Décision différentielle
```json
{"operation":"decision","revenu_gagne":0,"revenu_perdu":100,"cout_evite":70,"cout_ajoute":0,"contribution_alternative":0,"contribution_sacrifiee":0}
```
Variation −30. Les coûts évités doivent être réellement évitables ; ne pas inclure à nouveau les coûts dans les contributions alternatives.

### Prix cible
```json
{"operation":"prix","cout_variable_unitaire":50,"taux_cible":0.30,"taux_commission":0.10}
```
Prix théorique 83,33 avant arrondi commercial ; la commission ne doit pas déjà être incluse dans le coût unitaire.

### Capacité continue à une contrainte
```json
{"operation":"capacite","capacite":100,"unites_divisibles":true,"une_seule_contrainte":true,"produits":[{"id":"A","contribution_unitaire":30,"ressource_unitaire":3,"demande_max":40},{"id":"B","contribution_unitaire":20,"ressource_unitaire":1,"demande_max":70}]}
```
B 70 puis A 10, contribution 1700. Ne pas arrondir arbitrairement un résultat fractionnaire pour un problème entier. Le script ne gère ni plusieurs ressources ni lots/minima ni coûts par palier.
