---
name: controle-budgetaire
description: 'Analyse les écarts budget/réalisé, prévisions et N-1 : effets prix, volume, mix, coûts standards, budget flexible et commentaires de gestion.'
metadata:
  version: 1.0.0-rc3
  langue: fr
  reference: FIN-02
compatibility: 'Données fournies par l’utilisateur. Calculateur facultatif : Python 3.9+ et exécution de code, sans dépendance
  externe ni réseau.'
---

# Contrôle budgétaire et analyse des écarts

## Mission
Produire une analyse réconciliée, explicative et exploitable par la direction ou le responsable opérationnel, à partir des chiffres de l'utilisateur. Ne pas inventer de budget, de cause, de seuil ou de standard de coût. Adapter la profondeur et le format au destinataire.

## 1. Cadrer et contrôler
- Identifier période, entité, centre, produit, devise, unité, référentiel analytique, version/date du budget ou forecast, clôture et périmètre. Demander seulement les précisions bloquantes; sinon expliciter les hypothèses et poursuivre partiellement.
- Lire [controle-des-donnees.md](references/controle-des-donnees.md). Construire une table de correspondance des lignes réelles et prévues avec source (fichier, onglet, ligne ou identifiant). Séparer détail et sous-totaux; ne jamais additionner les deux. Une absence n'est pas un zéro. Harmoniser les charges positives en montant, sans effacer les avoirs. Ne pas convertir les devises sans taux documentés.
- Conserver budget initial, forecast et éventuel budget révisé séparés. Comparer périodes de même durée et même périmètre; isoler les changements plutôt que les masquer.

## 2. Calculer selon la question
- Écart brut = réalisé − référence. Pour produits/marges/résultat, impact favorable si positif; pour charges, signe économique inversé. Pour KPI sans direction évidente, demander ou laisser neutre. Lire [conventions-et-materialite.md](references/conventions-et-materialite.md).
- CA, contribution, portefeuille produits : lire [prix-volume-mix.md](references/prix-volume-mix.md). N'utiliser le mix que pour des quantités homogènes et des standards comparables; sinon décomposer par produit sans agréger les volumes.
- Coûts de production, charges variables/fixes, rendement, masse salariale : lire [couts-et-budget-flexible.md](references/couts-et-budget-flexible.md). Distinguer consommation, achats, production et ventes; ne pas les substituer.
- Révision de standards, forecast, effets de calendrier et de change : lire [comparaisons-et-revisions.md](references/comparaisons-et-revisions.md). Ne pas présenter une révision de prévision comme un budget autorisé.
- Si exécution Python disponible, utiliser le calculateur selon [utilisation-du-calculateur.md](references/utilisation-du-calculateur.md), avec un JSON normalisé construit à partir des données sources. Vérifier sorties et réconciliation avec les totaux de contrôle. Le script ne lit ni Excel ni PDF directement. Sans exécution, appliquer les identités manuellement, montrer les opérandes et préciser que les calculs n'ont pas été automatisés.
- Ne pas forcer un effet mix, volume, prix ou rendement si les inducteurs manquent. Restituer l'écart global calculable et la liste des données nécessaires. Pour un produit nouveau/sorti, ne jamais inventer le prix ou le coût unitaire de référence; isoler son effet d'entrée/sortie si les montants sont connus, sinon s'abstenir.
- Vérifier les identités à la précision des sources, puis expliquer tout écart d'arrondi. Si écart inexpliqué, marquer le pont comme non réconcilié; ne jamais l'attribuer arbitrairement au mix.

## 3. Interpréter et restituer
- Classer les écarts selon leur impact absolu et leur importance métier. Montrer favorable/défavorable séparément, y compris les compensations. Les seuils sont ceux de l'entreprise; à défaut présenter un classement descriptif sans prétendre à un seuil officiel.
- Lire [commentaires-et-actions.md](references/commentaires-et-actions.md). Pour chaque écart significatif : fait chiffré, décomposition, cause démontrée ou hypothèse, caractère récurrent/ponctuel si documenté, conséquence, action et responsable pressenti (à confirmer).
- Rapprocher le résultat total des effets non redondants; ne pas additionner un effet CA et sa décomposition, ni un effet marge et ses composantes. Ne pas assimiler un effet comptable à un gain de trésorerie.
- Présenter une synthèse décisionnelle, un tableau budget/réel/écart/%/F-D, le pont des effets disponibles, les actions prioritaires et les limites. Générer un Excel, un rapport ou un graphique uniquement si demandé et si les outils sont disponibles.
- Terminer par les contrôles réalisés, les sources des chiffres et les données manquantes qui pourraient changer le diagnostic. Ne jamais modifier un budget ou transmettre un rapport sans demande explicite.

## Coordination avec les autres compétences Finance
Analyse explicative des écarts contre une référence et des coûts standards. Si la demande vise un dossier global de comité de direction, contribuer au Reporting financier sans dupliquer le rapport. Pour une décision de prix ou d’arrêt d’activité, privilégier Analyse de rentabilité. Sur un budget négatif, présenter d’abord l’écart absolu ; le pourcentage sur valeur absolue de la base est un indicateur complémentaire explicitement libellé, jamais un taux de croissance. Ne pas imposer ce pourcentage dans le reporting consolidé.

## Périmètre détaillé et critères de déclenchement
Analyse les écarts entre budget, réalisé, forecast ou exercice précédent, explique les effets prix, volume, mix, coûts et rendement, construit un budget flexible et rédige des commentaires de gestion. Utiliser pour les revues budgétaires, analyses de marge, P&L de gestion, coûts standards, reporting des écarts et plans d'action. Ne pas utiliser pour établir un diagnostic de solvabilité, une prévision de trésorerie autonome ou un budget initial sans analyse d'écarts.
