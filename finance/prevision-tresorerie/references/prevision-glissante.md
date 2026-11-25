# Prévision glissante et conventions de calcul

## Horizon
Le solde de départ correspond à la fin de la date d'arrêté J. La projection couvre J+1 à J+91 inclus (13 blocs de sept jours, pas nécessairement des semaines civiles). Un horizon différent est possible de 1 à 366 jours. Si la demande porte sur des semaines civiles, conserver les dates exactes puis reclasser les résultats; ne pas comparer deux périodes de longueurs différentes sans avertissement.

Pour chaque date t, E(t) = somme des encaissements datés, D(t) = somme des décaissements datés (montants positifs). F(t) = E(t) - D(t). S(t) = S(t-1) + F(t). Pour une semaine, sommer E et D et reprendre le dernier solde de clôture; ne jamais sommer les soldes. Réconcilier S(fin) - S(initial) avec la somme des flux nets, au centime. Le calculateur utilise des centimes entiers, pas de flottants.

## Alertes
Calculer le minimum des soldes de clôture (en incluant le solde initial), la date associée, la première date strictement inférieure au seuil convenu, et l'écart maximum au seuil. Si le seuil est absent, n'inventer aucune réserve de sécurité; vérifier uniquement les soldes négatifs. Une marge positive au seuil ne garantit pas la disponibilité bancaire. Le minimum théorique si tous les décaissements d'une journée précédaient ses encaissements peut servir de signal de risque intrajournalier; ce n'est pas un solde observé. À défaut d'horaires, le calculateur ne donne que des clôtures journalières.

Les flux hors période sont listés séparément. Les flux sans date ou montant restent non résolus. Si le solde initial est inconnu, les soldes, seuils, points bas et besoins de financement sont indéterminés: seules les variations nettes datées sont présentées.

## Actualisation
Chaque semaine, remplacer la partie passée par les flux bancaires constatés, rapprocher le nouveau solde, revoir les engagements restants, conserver les identifiants stables et étendre l'horizon de sept jours. Un paiement reporté change de date, il ne devient pas un deuxième flux. Garder la projection antérieure pour analyser les écarts et ne pas réécrire l'historique.

Référence : [ACT — Cash-flow forecasting](https://hub.treasurers.org/bedrock-of-treasury-cash-flow-forecasting/). Le choix de 13 semaines et la granularité journalière sont des conventions de ce skill.
