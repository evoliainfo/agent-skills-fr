# Référentiel comptable français

## Périmètre et sources
- ANC, PCG consolidé au 1er janvier 2026 : https://www.anc.gouv.fr/plan-comptable-general-0
- ANC, règlement 2022-06 et commentaires : https://www.anc.gouv.fr/reglement-ndeg-2022-06-du-4-novembre-2022
- Bpifrance Création, SIG : https://bpifrance-creation.fr/encyclopedie/piloter-lentreprise/finance-pilotage-economique/comprendre-calculer-soldes
Références consultées le 24/11/2026 ; vérifier les textes applicables à l'exercice si une question normative est déterminante. Les conventions d'analyse financière ne constituent pas des règles de comptabilisation.

## Lecture des données PCG
Identifier la nomenclature exacte de l'entité, les libellés et subdivisions, les comptes de régularisation et les soldes. Repères de classes : 1 financement/capitaux, 2 immobilisations, 3 stocks, 4 tiers, 5 financiers, 6 charges, 7 produits. Ce sont des indices, non un mapping automatique universel. Une balance avant clôture peut contenir simultanément classes 6/7 et un résultat antérieur : ne pas compter le résultat deux fois. Les soldes débiteurs/créditeurs ne sont pas équivalents à la présentation positive des états. Pour les comptes de bilan, distinguer soldes d'ouverture, mouvements et soldes de clôture. Pour le résultat, retenir les mouvements de la période ou les soldes appropriés à la balance avant clôture. Si le fichier est un FEC, rapprocher la balance reconstruite des états fournis et respecter dates, journaux, écritures d'ouverture et clôture. Ne pas déduire un agrégat non fourni de la seule classe comptable lorsque des subdivisions ou reclassements sont nécessaires.

### Points de mapping à contrôler
| Poste | Repères à vérifier, non exhaustifs | Contrôle |
|---|---|---|
| Chiffre d'affaires | 70 et réductions commerciales correspondantes | HT, net des remises, hors production stockée/immobilisée |
| Marchandises | ventes 707, achats 607, variation de stocks correspondante | signe de la variation ; coût des ventes = achats nets + stock initial − stock final |
| Production | ventes de produits/prestations, 71 et 72 | production stockée et immobilisée distinctes |
| Consommations de tiers | achats consommés, services extérieurs | exclure le coût des marchandises déjà déduit ; affecter les remises |
| Personnel | 64 et éléments assimilés selon référentiel | distinguer personnel externe, intérim, retraitements facultatifs |
| Financement | emprunts, comptes courants, concours bancaires | échéances et nature ; ne pas assimiler toute classe 5 à du cash libre |
| Créances/dettes | clients, fournisseurs, fiscal/social, autres tiers | ventilation exploitation/hors exploitation, acomptes et échéances |
| Immobilisations | brut, amortissements, dépréciations, cessions | rapprocher état des immobilisations, VNC et prix de cession |

## Rupture de comparabilité depuis 2025
Pour les exercices ouverts à compter du 1er janvier 2025, la réforme de modernisation des états financiers modifie notamment le périmètre du résultat exceptionnel et supprime les transferts de charges comme rubrique autonome. Examiner la date d'ouverture et les méthodes réelles, y compris une éventuelle application anticipée. Les produits et charges liés à un événement majeur et inhabituel sont à distinguer selon les règles du texte ; ne pas reclasser automatiquement tout élément non récurrent en exceptionnel. Des cessions d'immobilisations peuvent être comptabilisées en exploitation ou en financier selon leur nature et la version applicable ; la CAF doit être neutralisée selon la nature économique et non un ancien numéro de compte fixe. Vérifier l'annexe et les comparatifs retraités. Si les comparatifs ne sont pas disponibles, ne pas fabriquer de retraitement ; montrer les séries telles que publiées avec réserve, ou calculer un pont documenté à périmètre constant.

## Hors périmètre
Les états consolidés IFRS, les établissements financiers et les organismes sans but lucratif nécessitent des référentiels spécifiques. Ne pas transposer sans adaptation les SIG, le bilan fonctionnel ou les ratios d'une entreprise industrielle et commerciale.
