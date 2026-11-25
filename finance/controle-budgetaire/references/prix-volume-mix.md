# Prix, volume, mix et contribution

Indices b = budget, r = réel. Les prix sont nets des remises selon le même périmètre. Pour un produit, CA = q × p; volume = (qr − qb) × pb; prix = qr × (pr − pb). La somme égale exactement le CA réel moins le CA prévu; l'interaction prix-quantité est incluse dans l'effet prix. Ne pas ajouter un résidu mix à ces deux effets.

## Portefeuille homogène
Pour chaque produit i, Qb = somme(qbi), Qr = somme(qri), mbi = qbi/Qb, qi* = Qr × mbi. Qb doit être strictement positif, les quantités non négatives et exprimées dans une unité commune. Les retours nets négatifs ou unités incompatibles empêchent cette décomposition agrégée.

| Effet | CA | Marge sur coûts variables |
|---|---|---|
| Volume total | Σ(qi* − qbi) × pbi | Σ(qi* − qbi) × (pbi − cbi) |
| Mix | Σ(qri − qi*) × pbi | Σ(qri − qi*) × (pbi − cbi) |
| Prix | Σ qri × (pri − pbi) | même formule |
| Coût unitaire variable | sans objet | Σ qri × (cbi − cri) |

La somme du pont de CA égale Σ(qri×pri−qbi×pbi). La somme du pont de contribution égale Σ(qri×(pri−cri)−qbi×(pbi−cbi)). Les charges fixes ne figurent pas dans la contribution; ajouter leur effet séparément pour rapprocher le résultat si le périmètre est complet. Ne pas utiliser ces coûts variables comme coûts complets.

Si les quantités ne sont pas comparables : calculer les effets quantité et prix pour chaque produit, puis sommer uniquement les montants; ne pas isoler volume total et mix. Si Qb = 0, le mix budgété est indéfini; utiliser le pont par produit seulement si les prix de référence sont documentés. Un prix ou coût de référence manquant interdit la décomposition correspondante. Pour les lancements et arrêts, isoler les montants d'entrée/sortie si le zéro et le périmètre sont confirmés; réconcilier avec le périmètre commun et préciser que le mix porte sur ce dernier.

## Exemple indépendant
Budget A : 100 unités à 10 €, coût variable 6 €; B : 100 unités à 20 €, coût 12 €. Réel A : 150 à 11 €, coût 7 €; B : 100 à 19 €, coût 11 €. Budget CA 3 000 €, réel 3 550 €. Quantités au mix budgété : 125/125. Volume +750 €, mix −250 €, prix +50 €, total +550 €. Contribution budget 1 200 €, réel 1 400 €. Volume +300 €, mix −100 €, prix +50 €, coût −50 €, total +200 €. La croissance du CA ne se transmet donc pas intégralement à la contribution.

Références : [DCG UE11, écarts CA/marge](https://innovaweb.fr/fr/kit/templates/dcg-ue11-budgets/controle-budgetaire-ecarts-ca-marges), [ACCA PM FAQ](https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f5/faqs.html), [Anthropic Variance Analysis](https://github.com/anthropics/knowledge-work-plugins/blob/main/finance/skills/variance-analysis/SKILL.md). Identités algébriques et exemple propres à ce skill.
