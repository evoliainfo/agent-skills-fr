# Calculateur de reporting

Le script `scripts/calculs-reporting.py` utilise Python standard. Il travaille sur des données **déjà normalisées**; il n'importe pas directement une balance, un ERP ou un PDF. L'assistant doit d'abord contrôler et préparer les données, notamment la cohérence des unités et des dates. Exécuter `python scripts/calculs-reporting.py entree.json` depuis la racine du skill. JSON sur stdout; erreur et code non nul en cas d'entrée invalide. Les décimaux sont restitués sous forme de chaînes pour préserver la précision; arrondir uniquement à la présentation. Les valeurs absentes sont `null`.

## Opérations
- `ecart` : `reel`, `ref`, `type_indicateur` (`flux`, `solde`, `ratio` exprimé en pourcentage), `sens` (`hausse`, `baisse`, `neutre`). Retourne l'écart, le pourcentage pour base positive hors ratio, les points pour ratio, la direction.
- `agreger` : `lignes`, `debut`, `fin` (AAAA-MM inclus), `type_indicateur`, `contexte`. Pour flux et soldes, champ `valeur`. Pour ratio de flux seulement, champs `numerateur`, `denominateur` (positif ou nul). Un solde utilise uniquement le dernier mois demandé. Une série incomplète renvoie null plutôt qu'un cumul partiel. Pas de calcul de moyenne de soldes par cette opération.
- `atterrissage` : mêmes champs, plus `dernier_cloture`, `version_reel`, `version_prevision`. Le contexte exige indicateur, périmètre, devise, unité. Les lignes des mois clôturés sont sélectionnées parmi le scénario `reel` avec `statut: cloture`; les mois suivants parmi `prevision`. Le premier mois précédent l'exercice peut servir de borne si aucun mois n'est clôturé. Les versions retenues doivent être distinctement identifiées. Ne pas inclure de lignes d'un autre indicateur.
- `pont` : `depart`, `arrivee`, `effets` (dictionnaire nom: valeur), `tolerance` (non négative). Vérifie le résidu, sans déduire la causalité.

## Exemples complets
```json
{"operation":"ecart","parametres":{"reel":6.9,"ref":12,"type_indicateur":"ratio","sens":"hausse"}}
```
Attendu : -5,1 points; pourcentage relatif indisponible.

```json
{"operation":"agreger","parametres":{"debut":"2026-01","fin":"2026-02","type_indicateur":"ratio","contexte":{"indicateur":"marge","scenario":"reel","version":"v1","perimetre":"societe","devise":"EUR","unite":"%"},"lignes":[{"mois":"2026-01","indicateur":"marge","scenario":"reel","version":"v1","perimetre":"societe","devise":"EUR","unite":"%","numerateur":10,"denominateur":100},{"mois":"2026-02","indicateur":"marge","scenario":"reel","version":"v1","perimetre":"societe","devise":"EUR","unite":"%","numerateur":60,"denominateur":300}]}}
```
Attendu : 17,5 %, pas la moyenne simple de 10 % et 20 %.

```json
{"operation":"pont","parametres":{"depart":100,"arrivee":130,"effets":{"volume":40,"prix":-10}}}
```
Attendu : résidu 0. Si un facteur manque, signaler le résidu et ne pas le réaffecter sans preuve.

Limites : mois calendaires entiers, une série à la fois, pas de conversion de monnaie, de consolidation juridique, de calcul automatique de matérialité ni d'extraction de documents. Pour périodes irrégulières ou données intra-mensuelles, appliquer les conventions documentées manuellement et contrôler les résultats.
