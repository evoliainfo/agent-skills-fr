# Contrôle des données et traçabilité

1. Inventorier les pièces et leur période ; déterminer laquelle est la source de référence par poste (états arrêtés plutôt qu'extraction provisoire, sauf demande différente). Ne jamais écraser un chiffre divergent sans expliquer la décision.
2. Constituer un registre : identifiant de poste, exercice, valeur d'origine, unité, valeur normalisée, signe, source précise, nature (publié/calculé/hypothèse), retraitement et justification. Si OCR ou image, vérifier les chiffres ambigus et les colonnes N/N-1.
3. Vérifier devises, HT/TTC, durée, dates de début/fin, périmètre juridique, présence de comparatifs retraités, conventions d'arrondi. Ne comparer ni consolider des montants de devises différentes sans taux documenté. Ne pas annualiser mécaniquement un exercice saisonnier.
4. Rapprocher actif et passif ; les totaux de détail doivent correspondre aux totaux publiés selon la précision affichée. Pour un état arrondi au k€, la tolérance doit découler du nombre de termes et du pas d'arrondi, et être indiquée. Un écart dans cette tolérance est un rapprochement approché, pas une égalité exacte. Si la précision est inconnue, ne supposer aucune tolérance.
5. Rapprocher produits − charges avec résultat net, bilan et compte de résultat ; vérifier l'affectation du résultat. Contrôler les soldes négatifs inattendus (avoirs, pertes, corrections) sans les transformer en positifs. Détecter doublons et sous-totaux inclus. Les données agrégées et détaillées doivent être traitées dans des blocs distincts.
6. Les valeurs non disponibles sont `null`. Un zéro signifie que l'absence de montant est confirmée. Ne déduire un zéro que d'une présentation dont l'exhaustivité est établie. Une différence résiduelle n'est pas un poste comptable sans justification.
7. Classer chaque indicateur : calculable et rapproché ; calculable mais non rapproché ; non calculable ; non interprétable. La confiance est qualitative et liée à des vérifications observables, pas un score inventé.

### Registre minimal (exemple illustratif)
| Exercice | Poste | Montant EUR | Origine | Source | Contrôle |
|---|---|---:|---|---|---|
| N | CA HT | 1 300 000 | publié | Compte de résultat, page 2, ligne CA | rapproché |
| N | EBE | 90 000 | calculé | VA + subventions − taxes − personnel | voir opérandes |
| N | Délai clients | indisponible | — | CA TTC manquant | non calculable |

Si les données sont incohérentes, isoler les conclusions concernées. Une question ciblée peut être traitée malgré une anomalie ailleurs si elle n'en dépend pas. Ne pas interpréter des valeurs provenant d'un bloc déclaré incohérent. Respecter la confidentialité ; aucun transfert externe sans accord.
