# 🧾 AUDIT-LOG — Construction du prompt de paris v12 (architecte v3)

Journal du pipeline d'agents : recherche → build → audit → contre-audit → LLM Council → itération → **vérification finale (re-vote sur la version corrigée)**.

- **Base** : fusion v10 (`promptparissportifsv10FINALE`) + v11 (`v11PROMPTPARISFINAL`), guidée par le **méga-prompt architecte v3**.
- **Cible** : `PROMPT-PARIS-FINAL.md` (v12) + `CE-QUE-DIT-LE-NET.md` (modèle).
- **Exécution** : 2 workflows, **23 agents** (~1,17 M tokens). Workflow principal : 6 escadrons de recherche + 1 architecte + 7 auditeurs adversariaux + 1 contre-auditeur + 3 conseillers + 1 itération finale. Workflow de vérification : 1 linter arithmétique + 3 conseillers (re-vote sur la version corrigée).
- **Mission** : produire un prompt quotidien exceptionnel (passionné + sharp, recherche web/pronostiqueurs poussée et visible, tout le menu marchés vivants d'abord, cotes réelles vérifiées, combinés qui paient, toujours b + a, sans bankroll) **et corriger les 6 problèmes P1-P6** observés sur le run v11.

> Le `deep-research` (skill) **n'a pas été utilisé** (consigne explicite). Le travail est un travail de prompt-engineering : fusion + correction + audit adversarial, pas une recherche profonde longue.

---

## 1. Escadron RECHERCHE (R1-R6) — directives retenues

| Agent | Sujet | Apports pour v12 |
|---|---|---|
| **R1** | Prompt engineering Claude | XML par blocs nommés ; anti-sur-contrainte (≤ 12 règles, framing positif, pas d'ordres absolus en majuscules) ; ancre = prior explicite ; permission d'incertitude **sans** permission de no-bet ; self-check léger single-pass ; donner le *pourquoi* des règles. |
| **R2** | Quant paris | Dévig mult/power/Shin + quand utiliser chacun ; `EV = p×cote−1` ; **seuil sur l'EV** = MAX(écart méthodes × cote, marge liquidité) ; **test ±2 pts** pour tuer l'edge dans le bruit (P2) ; distinction `ECART_PROBA`/`EV` ; corrélation des combinés ; CLV qualitative ; **aucun sizing/Kelly**. |
| **R3** | Pronostiqueurs & sentiment *(renforcé P3)* | Scan large (Forebet, Dimers, Pronosoft, Coteur, Reddit, OLBG, bettingexpert, Covers, X) ; tri **INFO vérifiable** vs **PICK brut** (poids 0) ; **fade du consensus public** ; 3 biais (survivant, écho-chamber, récence) ; checklist « suivre un prono » ; **format exact d'une section visible « 📣 Ce que dit le net »**. |
| **R4** | Analyse sportive *(renforcé P5, nourrit P4/P6)* | Grilles foot (PPDA×xG, ligne haute/vitesse, set-pieces, game-state) ; tennis (surface > serve/return > fatigue > H2H filtré) ; **grilles de lecture des marchés vivants** (BTTS, buteur, victoire+BTTS, over, handicap) ; autres sports ; « chiffre avant interprétation » ; reads vivants + grounded. |
| **R5** | Données & cotes RÉELLES *(clé P1)* | Protocole de relevé des **vrais prix** (book FR + ancre sharp via Pinnacle/Oddspedia/Coteur, book/source + heure) ; statut de cote ✅/⚠️/❌ ; gate « pas de 🟢 sur cote non vérifiée » ; evidence ledger ; architecture 2 couches en MODE API ; MODE WEB par défaut (le repo n'a pas de clés). |
| **R6** | Anti-sur-contrainte & couverture | Hiérarchie de priorité (paliers) ; directives positives ; **menu complet exploré** (P4, pas de repli 1X2) ; déclencheurs RADAR non limitatifs ; pièges à éviter (réduire < 12 règles casse le plancher ; buckets EV chiffrés = nombres magiques). |

---

## 2. Escadron AUDIT (A1-A7) — 24 fails avec preuve sur le draft

**2 BLOCKER, 9 MAJOR, 13 MINOR.** Les plus marquants :

- **A1 (linter)** — **arithmétique fabriquée dans l'exemple value phare** : « robustesse ±2 pts : +2,6 % / +6,6 % » alors que le calcul exact à cote 2,05 donne +0,45 % / +8,65 %. Hallucination numérique **dans le prompt anti-hallucination**. (BLOCKER)
- **A1 (conséquence)** — une fois l'arithmétique corrigée, la borne basse réelle (+0,45 %) passe **sous le seuil de bruit** que le draft dérive lui-même (écart méthodes 1,5 pt × 2,05 ≈ 3,07 %) → l'exemple « 🟢 robuste » **échouait à son propre gate** et enseignait l'inverse de la règle 5. (BLOCKER)
- **A4** — combiné « victoire + BTTS » étiqueté **corrélation positive** mais chiffré à l'envers (naïf 0,33 → ajusté 0,26 = baisse = négative). (MAJOR)
- **A2 / A5** — repère buteur « ~45-55 % » sans la clause « jamais ressorti comme stat du jour » ; prose « EV ≈ borderline » fausse (50 % × 2,10 = +5,0 %). (MAJOR)
- **A2** — jambes du combiné chiffrées (produit naïf) sans ligne au ledger ; stats tactiques décisives (PPDA, xG) jamais traçables. (MAJOR)
- **A3** — l'**énumération complète du menu** de marchés (double chance, handicaps EU + asiatiques, totals 1,5/2,5/3,5, props) présente en v11 avait **disparu** au profit de « ≥ 3 familles ». (MAJOR — P4)
- **A7** — la vérif ne contrôlait que la présence de la section 📣, **pas son rattachement** au ledger sentiment horodaté (un tableau 📣 halluciné passait). (MAJOR — P3)
- **Fichier manquant** — le draft renvoyait à un `CE-QUE-DIT-LE-NET.md` **inexistant** → référence morte. (MAJOR)

---

## 3. CONTRE-AUDIT (C1) — red-team de l'audit

C1 valide la majorité des fails et **rejette les sur-corrections** :

**Fails endossés (corrigés en v12) :** arithmétique Verdon recalculée ; exemple 🟢 relevé pour survivre réellement au seuil aux deux bornes ; corrélation combinée remise dans le bon sens + **règle directionnelle explicite** ; garde-fou étendu au repère buteur ; jambes de combiné + stats tactiques décisives **tracées au ledger** ; énumération du menu **réintroduite** ; 📣 **rattachée au ledger horodaté** (vérif 8b) ; référence morte **retirée** (contenu inline) ; vocabulaire de statut **unifié** ✅/⚠️/❌.

**Sur-corrections rejetées :** forcer un chiffre d'EV sur tout 🎲 plaisir (le §0 autorise EV = « — ») ; rétrograder en « NARRATIF » **toute** stat non tracée (assécherait la couleur des compétitions discrètes — limité aux chiffres qui *portent* une décision 🟢) ; traiter les bornes BTTS « 6/7 & > 1,2/match » comme un gate dur (ce sont des **repères de lecture**) ; réécrire le freebet sur le fond.

**Contrôles de sécurité :** `floor_intact = true`, `bankroll_reintroduced = false`.

---

## 4. LLM COUNCIL — note contre la rubrique

- **Sur le draft (avant itération)** : 3 conseillers indépendants (rigueur quant & honnêteté · utilité parieur/marchés vivants/fun · Claude & sobriété) → moyenne **6,33/10**, `pass = false` les trois, à cause des 2 BLOCKER d'arithmétique + corrélation à l'envers + fichier manquant.
- **Itération** : l'architecte applique les fails endossés + minors du Council, garde le plancher + b + a + zéro bankroll, n'applique pas les sur-corrections rejetées.
- **Vérification finale (re-vote sur la version corrigée)** : 1 linter arithmétique (recalcul de **chaque** nombre de l'exemple) + 3 conseillers re-notent.
  - **Linter : `gate_pass = true`**, 0 erreur d'arithmétique, 0 nombre fabriqué, 0 contradiction, 0 blocker ouvert — « PRÊT À EXPÉDIER ».
  - **Council : 9,3 · 9,4 · 8,7 → moyenne 9,13/10**, `pass = true` les trois, **0 blocker, 0 major** (sauf un major de **sobriété** non bloquant, voir §6).
  - **`all_pass = true`.**

---

## 5. Comment chaque problème P1-P6 est corrigé

| # | Problème v11 | Correction v12 |
|---|---|---|
| **P1** | Cotes non vérifiées → no-vig faux, 🟢 sur du sable | Règle 2 (PALIER 0) + `<cotes_reelles>` : book/source + **heure** obligatoires pour tout 🟢 ; statut **✅/⚠️/❌ unifié** de bout en bout ; cote ⚠️/❌ **interdit le 🟢** et force EV = « — » ; vérif point 7 rétrograde tout 🟢 sans cote ✅. L'incertitude **rétrograde l'étiquette, ne vide jamais la boîte** (plancher préservé). |
| **P2** | Pari peu probable headliné comme value, edge dans le bruit | Règle 6 : pas de headline d'un simple à faible proba (< ~35-40 %) sur cote non vérifiée/edge dans le bruit. Règle 5 + Étape 5 : **seuil sur l'EV** = MAX(écart méthodes × cote, marge liquidité) + **test ±2 pts**. L'exemple value survit désormais aux deux bornes ; l'anti-pattern « nul @3,40 » est conservé comme **contre-modèle annoté** (arithmétique exacte). |
| **P3** | Recherche web + pronostiqueurs insuffisants/invisibles | `<recherche_web>` (≥ 5 familles, tri INFO/PICK poids 0, fade du public, 3 biais, checklist suivre-un-prono) + Étape moteur 2 + **section de sortie OBLIGATOIRE « 📣 Ce que dit le net »** (3 blocs) **tracée au ledger sentiment horodaté** (vérif 8b). Modèle détaillé dans `CE-QUE-DIT-LE-NET.md`. |
| **P4** | Limité au 1X2 | Étape 1 : **énumération complète du menu** (double chance, handicaps EU + asiatiques, totals 1,5/2,5/3,5, BTTS, scorers, buteurs, props, combinés) + ≥ 3 familles/match. Règle 6 ancre le tier plaisir/combiné dans les **marchés vivants** (1X2 sec = dernier recours, à dire). Étape 4 : grille de lecture par marché vivant. |
| **P5** | Manque de passion / profondeur tactique | `<role>` exige des reads de connaisseur (duel concret, détail tactique juste, pas de superlatifs). Étape 4 : 6 lignes foot + grilles marchés vivants/tennis/autres sports ; « chiffre avant interprétation » ; connexion obligatoire marché + mispricing. |
| **P6** | Combinés ennuyeux à payout ridicule | Règle 7 + Étape 7 : cote **excitante ~2,0-4,0**, **bet builder à corrélation positive préféré** (proba ajustée > produit naïf), produit naïf + proba réelle + **sens de la corrélation** affichés, chaque jambe tracée. Exemple corrigé en « victoire + Over » (vraie corrélation positive, 0,275 → 0,32, cote ~3,1). |

---

## 6. ⛔ GATES BLOQUANTS — statut final (v12)

| Gate | Statut | Où |
|---|---|---|
| Plancher d'action incassable (jamais « aucun pari ») + b ET a | ✅ PASS | Règle 1 (PALIER 0) + format §4/§5 + vérif 1, 2 + exemples jour pauvre & données manquantes |
| Cotes vérifiées : pas de 🟢 sur cote non confirmée, book + heure (P1) | ✅ PASS | Règle 2 + `<cotes_reelles>` + colonne « Statut cote » + ledger + vérif 7 |
| Pas d'edge-dans-le-bruit en 🟢 : seuil sur l'EV, test ±2 pts (P2) | ✅ PASS | Règle 5 + règle 12 + Étape 5 — **vérifié au calcul** (Verdon +5,4 %/+14,0 % > seuil 3,2 % ; nul @3,40 conservé en anti-pattern) |
| Marchés vivants : menu complet exploré, tier plaisir/combiné en priorité (P4) | ✅ PASS | Étape 1 (menu réintroduit) + règle 6 + Étape 4 (grille par marché) + vérif 8a |
| Recherche web + section « ce que dit le net » obligatoires (P3) | ✅ PASS | `<recherche_web>` + Étape 2 + format §2 + vérif 8b + ledger sentiment §6 |
| Combinés qui paient (pas ennuyeux) (P6) | ✅ PASS | Règle 7 + Étape 7 + format §4 (exemple victoire+Over @3,1, corrélation positive) |
| Zéro nombre/cote/match inventé ; zéro bankroll/sizing | ✅ PASS | Règle 3 + ledger §6 (cotes + sentiment + données tactiques) + vérif 4, 6 ; arithmétique recalculée |
| Anti-sur-contrainte (≤ 12 règles, logique conditionnelle, pas de contradiction) + honnêteté | ✅ PASS | 12 règles en 4 paliers + guides souples + framing positif ; aucune promesse de profit |

**Observation non bloquante (sobriété).** Le conseiller « Claude & sobriété » (pass = true, 8,7/10) note que v12 est dense (~310 lignes) avec une **redondance structurelle assumée** (statut de cote, règle de corrélation, test ±2 pts répétés à plusieurs endroits) et un `<exemple>` long (4 scénarios). Le linter et les deux autres conseillers jugent cette redondance **acceptable et intentionnelle** : un prompt collé à neuf chaque jour gagne en fiabilité à rappeler la règle au point d'usage, et la priorisation en 4 paliers + le marquage « règle dure vs guide souple » rendent la densité gérable. La longueur supplémentaire vs v11 est portée par les **nouvelles exigences réelles** (P1 `<cotes_reelles>`, P3 `<recherche_web>`/📣). Aucun gate §6 n'est en cause (les 12 règles dures sont respectées, sans contradiction). Piste d'allègement future possible (−40-60 lignes) : transformer les sections-guides en pures procédures qui *renvoient* aux règles dures au lieu de les ré-énoncer — à faire seulement si chaque fix reste présent une fois à son endroit canonique.

---

## 7. 📦 LIVRABLES

1. **`PROMPT-PARIS-FINAL.md`** (v12) — le prompt quotidien : passionné + sharp, recherche web + pronostiqueurs poussée et **visible** (📣), tout le menu (marchés vivants d'abord), **cotes réelles vérifiées** (gate), **combinés qui paient**, toujours b + a, sans bankroll, optimisé Claude. 3 exemples (jour normal / jour pauvre / données manquantes) + contre-modèle anti-pattern P2.
2. **`AUDIT-LOG.md`** — ce document.
3. **`CE-QUE-DIT-LE-NET.md`** — le modèle (format exact) de la section pronostiqueurs/consensus produite chaque jour ; copie de référence d'un contenu **déjà inline** dans le prompt (qui reste autonome et collable seul).

**Verdict final (Agent 0).** Livrable conforme au méga-prompt v3 : les 6 problèmes P1-P6 sont corrigés, les 8 gates bloquants sont verts, le Council re-vote la version corrigée à **9,13/10** (`pass` unanime) et le linter arithmétique confirme **0 erreur, 0 nombre fabriqué, 0 contradiction**. Le prompt conserve intégralement la machinerie quant de v11 (dévig multi-méthodes, `ECART_PROBA`/`EV`, anti-double-comptage, steelman + hypothèse nulle, evidence ledger, variance/CLV, no-bankroll) et restaure la chaleur et l'amplitude de menu de v10. Aucune promesse de profit — seulement un process honnête, chiffré, ancré sur des cotes réelles, qui sert toujours le pari plaisir + le combiné de l'utilisateur.
