# Marges et segmentation

## Définitions
Sur la même période : CA net = ventes hors TVA collectée − remises/avoirs/retours non déjà déduits. Marge commerciale (négoce) = ventes nettes de marchandises − coût d'achat des marchandises vendues. Ce coût tient compte des stocks et frais d'achat rattachables. En production, utiliser le coût des biens vendus, pas le coût de toute la production. Marge brute : définir la composition du coût des ventes avant toute comparaison.

Marge sur coûts variables (MCV) = CA net − coûts variables. Taux de MCV = MCV / CA net si CA positif. Marge sur coûts spécifiques = MCV − coûts fixes spécifiques au segment. Résultat analytique de l'ensemble = somme des marges spécifiques − charges fixes communes. Le calculateur implémente cette cascade, à condition que les coûts variables soient exhaustifs sur le périmètre et les coûts fixes spécifiques non dupliqués. Les coûts spécifiques ne sont pas automatiquement évitables.

Le taux de marge commerciale rapporté au coût d'achat et le taux de marque rapporté aux ventes sont différents. Toujours nommer le dénominateur. Pour une prestation, choisir une unité (heure facturée, dossier, mission), distinguer capacité disponible et facturée, et intégrer les coûts non facturables de service. Pour un client, inclure le coût de traitement, livraison, retours et support si causalement attribuables.

## Analyse portefeuille
- Calculer contribution absolue, taux, volume et contribution par unité ; ne pas moyenner les taux de segments : taux global = somme des contributions / somme des CA.
- Comparer les objets au même grain, éviter d'additionner les mêmes ventes ventilées par produit et client. Utiliser une table de faits unique et des vues distinctes.
- Détecter les objets à CA élevé mais faible contribution, ceux à contribution négative et les concentrations. Examiner coûts et prix observés avant d'attribuer une cause.
- Pour l'abandon d'un segment, utiliser les coûts pertinents, pas uniquement le résultat complet imputé.

## Exemple original
Produit A : CA 100 000 €, coûts variables 60 000 €, fixes spécifiques 15 000 €, contribution spécifique 25 000 €. Produit B : CA 80 000 €, coûts variables 50 000 €, fixes spécifiques 10 000 €, contribution spécifique 20 000 €. Fixes communs 30 000 € : résultat analytique 15 000 €. La clé de répartition des 30 000 € n'affecte pas ce résultat global.
