# Collecte, périmètre et fiabilité

## Inventaire minimal
- Date d'arrêté (fin de journée), devise, périmètre juridique, comptes inclus, soldes bancaires disponibles et rapprochés, espèces si significatives, restrictions sur les fonds.
- Balance âgée clients et fournisseurs: identifiant facture, tiers, solde restant, échéance, statut, litige, règlement partiel, historique de règlement, promesse de paiement.
- Paie nette, prélèvements, cotisations, TVA, impôts, loyers, abonnements, assurances, remboursements d'emprunts (capital/intérêts), investissements, échéanciers, acomptes, financements engagés.
- Carnet de commandes, ventes futures, conditions de règlement et saisonnalité lorsque pertinentes. Lister les données manquantes par catégorie et période.

## Contrôles avant calcul
1. Unité, devise, dates, signe, périmètre et source de chaque montant. Conserver la cellule, ligne ou référence documentaire. Distinguer date de facture, date d'échéance et date de caisse attendue.
2. Rapprocher le solde initial avec les extraits à la même date. Identifier les paiements en transit et les intégrer une seule fois s'ils ne sont pas déjà dans le solde. Exclure les soldes bloqués du disponible, mais les documenter séparément.
3. Pour chaque facture, solde TTC restant = montant TTC moins encaissements/paiements déjà constatés moins avoirs imputables. Vérifier que le solde de la balance âgée est bien net de ces éléments avant tout retraitement.
4. Rechercher les doublons via identifiant, tiers, montant, date et référence bancaire; un paiement fractionné doit avoir des identifiants distincts reliés à la même facture. Ne pas fusionner automatiquement deux opérations réellement différentes.
5. Vérifier la couverture de chaque catégorie par période, notamment paie, social, fiscal et dette. Établir explicitement « complète pour le périmètre et les hypothèses retenus » ou « partielle ». Le calculateur ne peut pas vérifier cette déclaration contre la comptabilité réelle.
6. Si une échéance est dépassée et non réglée, obtenir une date probable documentée. Sinon conserver le montant dans la liste des flux non datés, sans le placer fictivement dans la semaine 1. Les flux non datés n'entrent pas dans les sommes datées.

## Traitement des données incomplètes
Solde absent : flux nets uniquement. Montant/date absents : conserver l'élément non chiffré/non daté et déclarer la projection partielle. Si plusieurs devises, produire des projections séparées ou appliquer des hypothèses de change datées et explicites avant agrégation. Ne jamais convertir sans taux. Des comptes appartenant à des entités différentes ne sont pas fongibles sans accord et capacité de transfert.

Sources : Bpifrance Création, [plan de trésorerie](https://bpifrance-creation.fr/encyclopedie/previsions-financieres-business-plan/previsions-financieres/plan-tresorerie-projet) ; ACT, [Cash-flow forecasting](https://hub.treasurers.org/bedrock-of-treasury-cash-flow-forecasting/), consultés le 24/11/2026.
