# Coûts, activité et budget flexible

## Budget flexible
Pour un inducteur d'activité A homogène, coût fixe F et taux variable standard v : budget initial B = F + v×Ab; budget flexible BF = F + v×Ar. Écart de niveau = BF − B; écart de dépense = R − BF; somme = R − B. Ce modèle ne s'applique que sur une plage pertinente et avec des coûts linéaires; isoler les paliers et les changements de capacité. Un effet niveau positif n'est pas, en soi, une mauvaise performance opérationnelle.

## Charges directes
Pour la production réellement obtenue, quantité standard autorisée Qs = production réelle × consommation standard par unité. Coût standard Cs = Qs×Ps. Coût réel Cr = Qr×Pr. Écart de prix/taux = Qr×(Pr−Ps); écart consommation/efficacité = (Qr−Qs)×Ps; total = Cr−Cs. Pour la main-d'œuvre utiliser heures et taux horaires chargés comparables. Si l'écart de prix est mesuré à l'achat et la consommation à la sortie du stock, ne pas sommer sans rapprochement des flux et des stocks.

Pour distinguer effet de production et maîtrise des coûts, rapprocher aussi le coût standard de la production prévue : (Qs−Qb)×Ps + écart direct = Cr−Qb×Ps. Ne pas ajouter cet effet à un pont de contribution déjà calculé sur les ventes si les volumes ne sont pas réconciliés (stocks, en-cours).

Mix/rendement matières (si intrants dans une unité homogène) : définir Qr total et parts standards s_i = Qs_i / ΣQs_i, puis Qr_i* = Qr total × s_i. Mix = Σ(Qr_i−Qr_i*)Ps_i; rendement = Σ(Qr_i*−Qs_i)Ps_i. Somme = écart de consommation. Ne pas additionner ce dernier aux deux composantes. Si standard total nul, unités incompatibles ou quantités négatives, ne pas calculer le mix. Ce sous-pont peut être calculé manuellement si demandé; le script livré couvre les charges directes par facteur.

## Charges indirectes (imputation de coûts standards)
Ab activité budgétée normale, Ar activité consommée, Ap activité standard autorisée pour production réelle, F charges fixes prévues, v taux variable, Cr charges réelles. Ab > 0. Coût standard unitaire cs = v + F/Ab.
- Dépenses : Cr − (F+v×Ar).
- Activité / absorption : F+v×Ar − Ar×cs.
- Rendement : (Ar−Ap)×cs.
- Total : Cr − Ap×cs.

Ce pont est un écart par rapport au coût imputé, non le simple écart au budget initial. L'absorption des coûts fixes ne mesure pas à elle seule une économie de décaissement. En pilotage marginal, préférer le budget flexible et distinguer les coûts fixes réels. Expliquer les bases choisies; ne pas combiner les deux ponts.

## Masse salariale
À effectif comparable, distinguer ETP/heures et taux chargé, analyser primes, heures supplémentaires, vacances de poste et mix de catégories si données disponibles. Les effets de taux et d'efficacité se calculent comme les charges directes lorsque les heures standard sont documentées. Sans heures, utiliser ETP moyens sur périodes comparables; un effectif de fin de mois n'est pas un ETP moyen. Ne pas déduire une responsabilité individuelle d'un écart agrégé.

Sources : [ACCA, budget flexible](https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f5/technical-articles/budgeting1.html), [ACCA, absorption des coûts fixes](https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f2/technical-articles/overhead-absorption.html), [ACCA, mix et rendement matières](https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f5/technical-articles/mat-yield.html), [DCG UE11, écarts coûts](https://innovaweb.fr/fr/kit/templates/dcg-ue11-budgets/ecarts-couts-production).
