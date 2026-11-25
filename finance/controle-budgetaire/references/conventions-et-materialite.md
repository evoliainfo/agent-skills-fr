# Conventions et matérialité

## Écarts simples
Pour chaque poste : E = R − B. Pourcentage = E / |B| × 100 si B ≠ 0. Le dénominateur absolu permet de lire le signe de l'écart même pour un budget négatif; ce n'est pas un taux de croissance conventionnel. Si B = 0, afficher « non calculable », même si R = 0. Si B manque, ne calculer aucun écart. Ne pas confondre écart en pourcentage et différence en points de pourcentage (marges, taux).

| Nature | Impact sur résultat / lecture |
|---|---|
| Produit, contribution, résultat | E; positif F, négatif D |
| Charge exprimée en montant | −E; positif F, négatif D |
| KPI non financier | direction explicitée par l'utilisateur, sinon neutre |

Les variations de postes intermédiaires (CA, marge) ne constituent pas toutes des impacts indépendants sur le résultat. Ne pas sommer des sous-totaux ou des KPI de nature différente.

## Gestion par exception
Utiliser les seuils approuvés (montant, pourcentage, combinaison OU/ET). À défaut, classer par valeur absolue, présenter les plus importants dans le contexte et signaler que la sélection est descriptive. Un petit montant en pourcentage peut être important à cause d'un risque de conformité ou d'un KPI critique. Un gros pourcentage sur une base proche de zéro ne suffit pas à qualifier une anomalie. Ne pas omettre les compensations : montrer total net et principaux écarts bruts.

## Réconciliation
Calculer avant d'arrondir. Sur un pont de résultat, la somme des effets signés doit correspondre à résultat réel − résultat budget. Les écarts d'arrondi d'affichage sont explicitement séparés; un écart de données n'est pas un arrondi. Pour une somme à zéro, vérifier la présence de compensations avant de conclure à la stabilité.

Références : [Anthropic, Variance Analysis](https://github.com/anthropics/knowledge-work-plugins/blob/main/finance/skills/variance-analysis/SKILL.md) (organisation des commentaires et seuils); [DCG UE11, contrôle budgétaire](https://innovaweb.fr/fr/kit/templates/dcg-ue11-budgets/controle-budgetaire-ecarts-ca-marges) (conventions et réconciliation). Conventions locales explicites; rédaction originale.

**Restitution commune au pack Finance :** pour une référence négative, présenter le montant absolu en priorité. Le pourcentage sur |B| est facultatif et doit être libellé « écart rapporté à la valeur absolue du budget ». Il n’est pas un taux de croissance.
