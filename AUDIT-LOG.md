# 🧾 AUDIT-LOG — Construction du prompt de paris v11 (architecte v2)

Journal du pipeline d'agents : recherche → build → audit → contre-audit → LLM Council → itération, **plus l'arbitrage final de l'Agent 0 (orchestrateur)**.

- **Base** : prompt v10 (pièce jointe `V10_katchauou.docx`).
- **Cible** : `PROMPT-PARIS-FINAL.md` (v11).
- **Exécution** : 1 workflow, **20 agents**, ~463 k tokens, 6 escadrons de recherche (web), 6 auditeurs adversariaux, 1 contre-auditeur, 3 conseillers + 1 synthèse.
- **3 changements imposés** appliqués : (1) suppression totale bankroll/sizing/Kelly ; (2) toujours **b + a** (plaisir+combiné en avant, value pure à la fin) ; (3) base v10 améliorée, optimisée Claude (XML, logique conditionnelle, ≤ 12 règles dures).

---

## 1. Escadron RECHERCHE (R1–R6) — ce qui est ressorti

| Agent | Sujet | Apports retenus |
|---|---|---|
| **R1** | Prompt engineering Claude | Structure **XML** par blocs nommés ; **anti-sur-contrainte** (≤ ~12 règles, supprimer MAJUSCULES/« TU DOIS »/« JAMAIS », −19 % de suivi quand on empile les contraintes) ; **framing positif** (« retiens un pari si… » > « ne parie jamais sans… ») ; ancre marché = **prior explicite** (LLM surconfiants, confiance verbalisée qui sature) ; **self-check léger single-pass** (CoVe complète trop coûteuse) ; donner le **pourquoi** des règles ; few-shot diversifiés. *(Note : R1 recommandait aussi de « valoriser le no-bet » — voir §6, arbitré par l'Agent 0.)* |
| **R2** | Quant paris | **Dévig** par méthode (multiplicatif équilibré / power favori lourd & 2-issues / **Shin** 1X2) ; `EV = p×cote−1` ; seuil de value dépendant de la cote, edge dans le bruit < ~2-3 % ou < écart entre méthodes → pas de value ; **CLV** = meilleur prédicteur du process ; **combinés same-match = corrélation tax ~20-25 %, jamais p1×p2 naïf** ; Poisson/Dixon-Coles/Elo seulement comme cadre qualitatif ; Prophet Arena / Schoenegger 2024 → LLM = synthétiseur calibré, pas oracle. **Aucun sizing/Kelly** (bankroll supprimée). |
| **R3** | Sentiment & pronostiqueurs | Parsing **2 colonnes** (claim vérifiable vs pick/opinion, poids du pick = 0) ; sous-module **« suivre un prono »** avec checklist bloquante ; **test du mispricing nommable** ; biais du survivant ; dédup des sources corrélées ; juger les tipsters sur la **CLV** (> 200 paris), jamais sur les screenshots. |
| **R4** | Analyse sportive | **« Chiffre avant interprétation »** : toute tactique sans donnée = « NARRATIF — non actionnable » ; champ **« déjà price ? »** anti-double-comptage ; **grilles par sport** (foot : Press/Press & set-pieces ; tennis : surface > serve/return > fatigue > H2H filtré ; US : repos/back-to-back) ; **steelman systématique** ; divergence forte vs marché = prudence. |
| **R5** | Données & API | Ancre = **clôture Pinnacle dévigée** ; books FR = **cible de mise** (Coteur/Oddspedia), pas ancre ; stack gratuite (The Odds API, API-Football compos/blessures, Understat xG, **Sackmann** tennis Elo/surface) ; clés en variables d'env, cache CSV ; **KPI = CLV** vs clôture (football-data.co.uk colonnes *C/PSC) ; ne pas dépendre de SofaScore (API fragile). |
| **R6** | Anti-sur-contrainte | **Hiérarchie de priorité explicite** pour arbitrer les conflits de règles ; directives positives ; **rationale + exemples canoniques annotés** ; phases modulaires nettes ; self-check final léger. *(R6 poussait « plancher d'action garanti ≠ plancher de paris » — l'Agent 0 a tranché en faveur du plancher de paris plaisir, voir §6.)* |

→ Détail intégral et décisions d'intégration dans **`TOUS-LES-MEILLEURS-TRUCS.md`**.

---

## 2. Escadron AUDIT (A1–A6) — FAIL avec preuve sur le draft B1

**38 fails** levés. Les plus marquants :

- **A1 (linter adversarial)** — proposait de réduire les 11-12 règles à 6-7 *(rejeté par C1, voir §3)* ; noms d'équipes réels dans l'exemple (gardés avec tag `[FICTIF]`).
- **A2 (evidence/pricing ledger)** — `CLV attendu` **chiffré** (« +0,06 ») = **nombre prédictif halluciné** ; constantes hard-codées (CPA ~⅓ des buts, marge SGP ~20-25 %) présentées comme des faits du match ; **traçabilité cote** (book + heure) absente de `<evidence>` → CLV inauditable.
- **A3 (couverture)** — grilles limitées à foot/tennis/US → **trou** basket/rugby/hockey/MMA/e-sport ; déclencheurs RADAR à rendre **non limitatifs**.
- **A4 (maths/devig)** — **double définition incompatible du mot « edge »** (écart de proba vs ROI `p×cote−1`) : confirmée par calcul (à 2,05 elles coïncident ~+4,5 %, mais 4 pts de proba = +20 % de ROI à cote 5,0) → un seuil en points de proba **récompense mécaniquement les outsiders**, l'inverse du but. *(A4 voulait aussi des buckets EV chiffrés par tranche de cote — rejeté, voir §3.)*
- **A5 (réalisme/honnêteté)** — manque le concept de **variance** dans la philosophie ; steelman à renforcer par l'**hypothèse nulle**.
- **A6 (sécurité, bankroll supprimée)** — **aucun sizing/Kelly/% réintroduit (✔ confirmé)** ; mais « toute divergence forte = PRUDENCE » **sans porte de sortie** risquait d'étouffer toute value légitime (sur-prudence).

---

## 3. CONTRE-AUDIT (C1) — red-team de l'audit

C1 valide le draft comme **non-bloquant, sans bankroll réintroduite, b+a préservé**, et identifie **~9 fails réellement valides** + plusieurs **sur-corrections** à rejeter :

**Fails endossés (corrigés dans v11) :** CLV chiffré → **direction qualitative** ; constantes CPA/SGP → **repères heuristiques non citables comme stat du jour** ; **edge** → deux grandeurs nommées (`ECART_PROBA` vs `EV/ROI`), seuil sur l'EV ; clause d'équilibre sur la prudence (**mispricing nommable** comme porte de sortie) ; **evidence ledger** book+heure avec dégradé gracieux ; grille **fallback autres sports** + déclencheurs RADAR non limitatifs ; phrase **variance** en philosophie ; **hypothèse nulle** dans le steelman.

**Sur-corrections rejetées :** réduire à 6-7 règles (risquait de supprimer plancher d'action + anti-double-comptage) ; **buckets EV chiffrés par tranche** (réintroduisait les « nombres magiques » que A2/A5 condamnent — contradiction interne de l'audit) ; rendre le plancher entièrement dérivé via MAX() en retirant le repère ~2-3 % ; renommer les équipes de l'exemple.

---

## 4. LLM COUNCIL — note contre la rubrique

3 conseillers indépendants (lentilles : *rigueur quant & honnêteté*, *utilité parieur & couverture*, *optimisation Claude & sobriété*) + 1 synthèse.

- **Note globale consolidée : 8,6 / 10**, `pass = true` sur la version issue de l'itération.
- **26 changements consolidés** appliqués au draft (dédupliqués depuis C1 + conseillers).
- Audit final des gates : **0 BLOCKER, 0 MAJOR, 2 MINOR** (cohérence VALUE PURE↔BOÎTE ; mot « bornée » à réaligner sur règle 12) — les deux **corrigés** dans v11.

---

## 5. ⚖️ ARBITRAGE FINAL DE L'AGENT 0 — le désaccord de fond (et sa résolution)

**Ce qui résiste — et a dû être tranché par l'orchestrateur.** Le workflow a produit un prompt quant **excellent mais qui a inversé une exigence centrale et répétée du méga-prompt.** Sous l'influence de R1/R6 (guidance Anthropic anti-hallucination : « valoriser explicitement le *aucun pari* »), l'armée a érigé le **NO-BET en prior** :

- règle Top-3 du draft : *« zéro quota — le NO-BET est un résultat valide »* ;
- section plaisir/combiné reléguée en **« optionnel »** avec *« Pas de combiné plaisir défendable aujourd'hui »* ;
- BOÎTE DE DÉCISION pouvant être **« vide — NO-BET »**.
- C1 lui-même l'a noté : *« combiné plaisir 'toujours'… contredit le droit au NO-BET (règle 2) »* — preuve que **tout l'escadron avait internalisé l'inversion**.

**Or le méga-prompt est sans ambiguïté et répété :** Gate bloquant n°1 *« Plancher d'action incassable — jamais 'aucun pari' »* (test : un jour sans value → sort-il **quand même** plaisir + combiné ?) ; §1 changement n°2 *« TOUJOURS b + a… le pari plaisir + le combiné mis en avant (le cœur de ce que joue l'utilisateur) »* ; §8 *« Toujours b + a. Plaisir + combiné en avant, value pure à la fin. »*

**Résolution (appliquée dans v11).** Le méga-prompt avait **déjà pré-résolu** cette tension honnêteté ↔ plancher d'action : on sert **toujours** le pari plaisir + le combiné, mais on les **étiquette honnêtement** (`🎲 plaisir — EV négative assumée`, jamais maquillés en value) ; le **seul** palier qui peut être vide est la **value pure (+EV)**. L'honnêteté n'est pas de refuser de jouer — c'est de ne jamais vendre un pari plaisir comme du +EV.

Donc, en tant qu'Agent 0, **j'ai bloqué la sortie du workflow et corrigé le framing**, en conservant **intégralement** la machinerie quant (dévig multi-méthodes, distinction `ECART_PROBA`/`EV`, anti-double-comptage « déjà price ? », steelman + hypothèse nulle, evidence ledger traçable, variance/CLV, no-bankroll, garde-fou unique) :

| Drift du workflow | Correction Agent 0 (v11) |
|---|---|
| « zéro quota — NO-BET valide » en Top-3 | **Plancher d'action sacré** en Top-3 : toujours plaisir + combiné, jamais « aucun pari » |
| Plaisir/combiné « optionnel » | Section **🎲🚀 OBLIGATOIRE en avant** (b), value pure conditionnelle à la fin (a) |
| BOÎTE « vide — NO-BET » | BOÎTE **jamais vide** (≥ le pari plaisir) ; le « rien aujourd'hui » vit dans la **section value** |
| Identité « trader qui dit rien aujourd'hui » | Restauration de l'identité **passionné + sharp**, marchés vivants, plaisir-first |
| Honnêteté = abstention | Honnêteté = **étiquetage** (plaisir ≠ value) ; variance/CLV/no-profit **conservés** |

→ Les exemples « jour pauvre » et « données manquantes » de v11 démontrent que le **plancher tient** tout en disant franchement « aucune value pure aujourd'hui ».

---

## 6. ✅ GATES BLOQUANTS — statut final (v11)

| Gate | Statut | Où |
|---|---|---|
| Plancher d'action incassable (jamais « aucun pari ») | ✅ | Règle 2 + Top-3 + format §3 + exemple jour pauvre |
| b ET a toujours présents | ✅ | Règle 10 + format §3 (b) / §4 (a) + vérif. point 2 |
| Zéro bankroll / sizing prescriptif réintroduit | ✅ | `<ce_que_je_te_donne>` + règle « mises libres » + vérif. point 6 (A6 confirmé) |
| Zéro nombre/cote/match sans trace ou source | ✅ | Règles 4 & 12 + evidence ledger + CLV en direction qualitative |
| No-vig : value vs dévigé, jamais cote brute | ✅ | Règles 3 & 6 + moteur étape 2 (mult/power/Shin) |
| Couverture : balayage large + radar | ✅ | Moteur étape 1 + format §1 (compétitions discrètes, déclencheurs non limitatifs) |
| Anti-sur-contrainte (≤ ~12 règles, logique conditionnelle, pas de contradiction) | ✅ | 12 règles priorisées + guides souples + framing positif/XML |
| Honnêteté (aucune promesse d'edge garanti / pari « sûr ») | ✅ | Philosophie + règle 11 + variance + étiquetage plaisir |

**Verdict final Agent 0 :** livrable conforme au méga-prompt après arbitrage. Le prompt v11 est exceptionnel sur le process (rigueur quant, anti-hallucination, lecture tactique grounded, couverture large) **et** fidèle au cœur de l'utilisateur (passionné qui joue pour le plaisir, toujours servi b + a, sans bankroll). Aucune promesse de profit — seulement un raisonnement honnête, chiffré et ancré.
