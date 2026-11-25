---
name: analyse-rentabilite
description: 'Analyse les marges et coûts par produit, client ou activité : coûts complets, variables, ABC, seuil de rentabilité, prix et décisions sous contrainte.'
metadata:
  version: 1.0.0-rc3
  reference: FIN-04
  langue: fr
compatibility: 'Données fournies par l’utilisateur. Calculateur facultatif : Python 3.9+ et exécution de code, sans dépendance
  externe ni réseau.'
---
# Analyse de rentabilité

## Mission
Fournir une analyse de gestion traçable, adaptée à la décision et aux données d'une entreprise. Ne jamais assimiler un coût imputé à une économie réalisable. Distinguer rentabilité comptable, contribution, résultat différentiel et trésorerie.

## Démarche
1. Identifier la question de décision, le périmètre (entité, segment, produit/client), l'horizon, la période, la devise, l'unité d'activité, le destinataire et le référentiel de coûts. Si une donnée déterminante manque, demander une précision ciblée ou produire une analyse conditionnelle.
2. Inventorier les fichiers et leurs champs, relever les sources et les unités. Appliquer [le contrôle des données](references/controle-des-donnees.md) avant tout calcul. Traiter les retours, remises, commissions, coûts de service et la TVA non récupérable explicitement. Ne pas supposer qu'une cellule vide vaut zéro.
3. Sélectionner la méthode en fonction de la question (voir tableau ci-dessous). Ne pas charger les autres références sans besoin.
4. Construire une base analytique sans double comptage : coûts directs/indirects et fixes/variables sont deux axes distincts. Séparer les coûts attribuables des coûts communs. Réconcilier les totaux au compte de résultat ou expliquer l'écart (stocks, production immobilisée, périmètre, éléments exclus).
5. Exécuter les calculs avec [le calculateur](references/utilisation-du-calculateur.md) si un environnement Python est disponible. Sinon calculer explicitement, vérifier les identités et signaler que le script n'a pas été exécuté. Ne jamais inventer une exécution. Les allocations et hypothèses demeurent sous contrôle du professionnel.
6. Comparer les segments selon des définitions identiques ; présenter à la fois les montants et taux, les volumes et la contribution aux coûts communs. Les comparaisons à des périodes ou unités différentes exigent une normalisation justifiée.
7. Examiner au moins une alternative et les hypothèses sensibles lorsqu'une décision est demandée. Si la décision concerne un abandon, un prix, une commande spéciale ou un arbitrage de capacité, charger les coûts pertinents, même si une analyse en coûts complets existe déjà.
8. Restituer selon la demande : réponse courte, rapport, note de décision ou tableau de bord. Appliquer [le contrôle de restitution](references/diagnostic-et-restitution.md). Ne pas générer de fichier si ce n'est pas utile.

## Choix de méthode
| Question | Référence à charger |
|---|---|
| Marge par activité, produit, client, canal ; coûts spécifiques | [Marges et segmentation](references/marges-et-segmentation.md) |
| Coût de revient, frais indirects, centres d'analyse, ABC | [Coûts complets et ABC](references/couts-complets-et-abc.md) |
| Seuil, point mort, objectif de résultat, sensibilité | [Seuil et scénarios](references/seuil-et-scenarios.md) |
| Prix, abandon, commande spéciale, faire ou acheter | [Décisions et coûts pertinents](references/decisions-et-couts-pertinents.md) |
| Capacité limitée, mix optimal, rentabilité unitaire | [Capacité et économie unitaire](references/capacite-et-economie-unitaire.md) |

## Contrôles incontournables
- Une marge positive n'est pas une preuve de résultat net positif ; une perte après imputation n'est pas une preuve qu'il faut arrêter l'activité.
- Une charge fixe directe peut être évitable ou non : obtenir un horizon et une justification avant de la retenir dans une décision.
- Refuser les taux dont le dénominateur est nul ou non pertinent ; ne pas annoncer de seuil fini lorsque la contribution est négative ou nulle et les charges fixes positives.
- Ne pas extrapoler une relation linéaire en dehors de la capacité et du mix étudiés. Ne pas confondre prix HT, TTC et coût de trésorerie.
- Vérifier les sommes, résidus d'allocation, conventions de signes et le résultat avant/après. Distinguer faits, estimations, hypothèses et conclusions conditionnelles.
- Ne pas prétendre avoir vérifié des données ou normes non consultées. Ne jamais envoyer des données financières vers un service externe sans instruction explicite.

## Coordination avec les autres compétences Finance
Coûts, contribution, rentabilité par segment et arbitrages économiques. Si le besoin principal est d’expliquer les écarts entre réalisé et budget, privilégier Contrôle budgétaire ; si le besoin est un diagnostic de bilan, Analyse financière. Ne pas transformer un résultat différentiel en variation de trésorerie sans calendrier des flux.

## Périmètre détaillé et critères de déclenchement
Analyse la rentabilité par produit, client, commande, canal ou prestation et aide aux décisions de prix, de mix, de sous-traitance et de maintien d'activité. À utiliser pour calculer les marges, coûts de revient, coûts complets, coûts spécifiques, méthode ABC, seuil de rentabilité, point mort, coûts pertinents et rentabilité sous contrainte de capacité. Ne pas utiliser comme substitut à un diagnostic de bilan, une analyse d'écarts budgétaires ou une prévision de trésorerie.
