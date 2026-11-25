# Utilisation du calculateur

Le script ne lit pas directement les PDF ou les tableurs. L'assistant extrait et rapproche les données, puis construit un JSON en respectant ce contrat. Montants en unités de devise, au centime maximum (préférer les chaînes décimales avec point, sans séparateur de milliers); sens séparé du montant toujours positif. Un solde initial peut être négatif ou null. Les montants inconnus et dates inconnues sont null, jamais zéro. La couverture est une déclaration de l'analyste, pas une certification du script. Les catégories sont libres mais stables et homogènes. Les dates sont ISO AAAA-MM-JJ. Les flux déjà comptabilisés dans le solde initial ne sont pas fournis; un flux non réglé avec une date passée est signalé comme non résolu.

Exemple interne au contrat (données illustratives) :

```json
{
  "arrete": "2026-11-24",
  "devise": "EUR",
  "solde_initial": "25000.00",
  "seuil": "5000.00",
  "horizon_jours": 91,
  "couverture": "partielle",
  "donnees_manquantes": ["Prévisions fournisseurs des semaines 8 à 13"],
  "flux": [
    {"id":"C001","sens":"entree","categorie":"clients","date":"2026-12-03","montant":"18000.00","source":"Balance âgée, facture C001","nature":"engage"},
    {"id":"S001","sens":"sortie","categorie":"salaires","date":"2026-11-30","montant":"22000.00","source":"Échéancier de paie","nature":"confirme"}
  ],
  "scenarios": [
    {"nom":"Retard client","hypothese":"Règlement décalé de 14 jours","modifications":[{"id":"C001","date":"2026-12-17","motif":"Hypothèse de retard de deux semaines"}]}
  ]
}
```

Exécuter : `python scripts/calculs-tresorerie.py /chemin/entree.json > /chemin/resultats.json` (Python 3.9+; adapter le chemin au dossier réel). Aucun réseau, aucun paquet tiers. Les variantes peuvent modifier `date` et/ou `montant`, ou utiliser `annuler: true` avec un motif. `ajouts` est une liste facultative de flux au même format, avec des identifiants nouveaux. Ne jamais modifier une variante pour masquer un paiement obligatoire.

Lire les résultats : `central` et `scenarios[].projection` contiennent les totaux, les soldes, dates de tension, 13 blocs hebdomadaires par défaut, détails quotidiens, totaux par catégorie et listes de flux avec leurs sources. Les montants de sortie sont des chaînes à deux décimales; convertir de manière exacte si nécessaire. `minimum_cloture` inclut le solde à l'arrêté; le seuil est testé strictement en dessous. Si solde initial absent, la projection est partielle et tous les indicateurs de niveau sont null. Les flux non résolus rendent automatiquement la projection partielle; les flux futurs au-delà de l'horizon sont listés à part. Une projection complète selon déclaration n'implique pas que les hypothèses sont certaines. Aucune disponibilité de crédit n'est calculée automatiquement.

En cas d'erreur, lire stderr, corriger le JSON à partir de la source, puis relancer. Ne pas supprimer une ligne problématique sans l'inscrire parmi les données manquantes. Si Python n'est pas disponible, reproduire les calculs manuellement avec rapprochement et le signaler. Les erreurs de mapping documentaire et les doublons économiques ayant des identifiants distincts ne peuvent pas être détectés automatiquement par ce script.
