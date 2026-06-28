# 🧾 AUDIT-LOG — Prompt de paris v13 (architecte v4)

Journal court du pipeline d'agents qui a produit `PROMPT-PARIS-FINAL-v13.md` à partir de v12.

- **Base** : v12 (`PROMPT-PARIS-FINAL.md`), guidée par le **méga-prompt architecte v4**.
- **Exécution** : 1 workflow, **32 agents** (~1,65 M tokens) : 7 recherche → 1 build → 1 humanizer → 9 audit adversarial → 1 contre-audit → 5 Council → 1 itération → 8 vérification finale (linter arithmétique + forensique + re-vote Council 5 lentilles).
- **Outillage** : les skills nommés au §4 du méga-prompt (`v12-system-architect`, `v13-betting-product-architect`, `v12-bookcheck-settlement`, `humanizer`, `llm-council`…) **ne sont pas installés** dans cet environnement ; chaque **rôle a été émulé** par un agent dédié. **`deep-research` n'a JAMAIS été utilisé ni mentionné** (vérifié par le linter final).

---

## 1. Comment NP1-NP4 sont corrigés

| # | Problème v12 | Correction v13 |
|---|---|---|
| **NP1** | Le prompt ne vérifiait pas l'existence + la cote sur Betclic → tout ⚠️ proxy, abandon trop rapide, value laissée sur la table. | Section canonique `<verif_betclic>` : la vérif est un **TRAVAIL ACTIF** (on ne lâche un angle qu'après avoir consulté les **3 sources ANJ**). Ordre imposé **Flashscore.fr → Coteur → Betclic.fr, AVANT la presse US**. **BOOK_CHECK par pari** (marché exact + **période** + ligne + cote + book + source + heure), un par jambe de combiné. Statuts liés au book (**✅ exige book=Betclic** ; ✅2src/✅1src/⚠️/❌). **ANCHOR_CHECK** symétrique pour l'ancre sharp. Règle 2 : **pas de 🟢 sans ✅ Betclic** ; ⚠️/❌ **rétrograde** l'étiquette, ne vide jamais la boîte. |
| **NP2** | Sortie limitée à victoire + buteur. | Étape moteur **4a — Génération d'angles** : brainstorm **8-12 candidats sur tout le menu** (corners, cartons, tirs/props joueur, handicaps asiatiques, mi-temps, HT/FT, total d'équipe, score groupé, 1re/dernière à marquer, course aux buts…) → **filtre 2-4** sur proba/lecture/fun. Règle 6 : ≥ 1 angle **hors victoire+buteur** dès qu'un marché vivant tient ; **1X2 sec = dernier recours, à dire**. Radar : ≥ 6 angles cités/match. Garde-fou : exotiques = vig lourd → **EV « — »**, plaisir oui, value quasi jamais. |
| **NP3** | Reads génériques. | `<role>` réécrit en **voix de connaisseur** (bannit les tics d'IA et superlatifs creux). Étape **4b** : read = **chiffre → duel/situation nommé → marché → mispricing**, + bloc « traduction situationnelle » (rotation, match pour rien, désespoir, derby, gueule de bois européenne, gardien incertain). Démontré dans l'exemple (read situationnel J+3 européen → corners de 1re période). |
| **NP4** | Skills sous-utilisés. | Rôles émulés à chaque poste (architecte produit, bookcheck via BOOK_CHECK, humanizer via la section Voix, council via `<verification>`). **Jamais `deep-research`.** |

## 2. Préférences gravées (dures)
- **Le nul ne figure jamais dans la boîte** (règle 3, zéro exception ; reste au radar comme contexte). La **double chance 1X/X2 est permise** (issue couverte, pas un pari SUR le nul) ; seul le « X » sec est interdit. L'anti-pattern montre un nul refusé.
- **Combiné deux-vainqueurs : pleinement bienvenu dès cote ~2,0** (règle 7, régime « deux vainqueurs indépendants » → `p1×p2` légitime, jamais diabolisé). L'exemple sert un combo deux-vainqueurs @3,87. **Seul le combo ennuyeux à ~1,3 est proscrit.**
- **Marchés vivants préférés** + vraie proba de toucher.

## 3. Audit → contre-audit → itération
- **Audit (A1-A9)** : **43 fails** (5 BLOCKER, 19 MAJOR, 19 MINOR) sur le draft. Les plus graves : value fabriquée / edge gonflé sur un angle créatif ; base de proba d'une jambe de combiné incohérente avec sa value ; ANCHOR_CHECK manquant (edge ANJ-vs-ANJ possible) ; période absente du BOOK_CHECK.
- **Contre-audit (C1)** : `floor_intact=true`, `bankroll_reintroduced=false`, `nul_in_box=false`, `two_winner_combo_diabolized=false` ; **`value_fabricated=true` sur le draft** → fail endossé en priorité. Sur-corrections rejetées : relabelliser le combo deux-vainqueurs en défaut, headliner un marché exotique en value, fabriquer une ancre dégradée ANJ-vs-ANJ pour combler un trou.
- **Itération** : value fabriquée supprimée (le seul 🟢 est un 1X2 ✅2src qui survit aux deux bornes du test ±2 pts, mispricing nommé = forfait partiellement price) ; base de proba unique gravée (l'ajustement value +2 pts ne sert jamais à la proba de toucher d'un combiné) ; ANCHOR_CHECK + période ajoutés ; passe d'allègement appliquée.

## 4. Allègement (chaque règle une fois)
12 redondances de v12 coupées (statut de cote 4× → 1× ; sens de corrélation 3-4× → 1× ; seuil + test ±2 pts ré-écrit 2× → 1× renvoi ; dévig multi-méthodes ré-écrite dans l'étape → renvoi règle 9 ; 3 biais, tri INFO/PICK, conséquence EV « — » regroupés à leur endroit canonique ; `<exemple>` jour-pauvre/données-manquantes condensés). **Résultat : 290 lignes vs 312 (v12)** — plus court et plus tranchant, chaque section-guide **renvoyant** aux règles dures. *(La cible indicative −40-80 lignes n'est que partiellement atteinte : l'itération a regrandi le draft de 262 → 290 pour intégrer ANCHOR_CHECK + période, jugés porteurs ; le gate « plus court que v12 » est tenu et le conseiller sobriété valide à 9,7/10.)*

## 5. ⛔ Gates bloquants — statut final

| Gate | Statut |
|---|---|
| Plancher d'action + b ET a | ✅ PASS |
| Vérification Betclic active (NP1, BOOK_CHECK, pas de 🟢 sans ✅ Betclic, ANJ avant presse US) | ✅ PASS |
| Créativité marchés (NP2, brainstorm + filtre, 1X2 dernier recours) | ✅ PASS |
| Reads passionné-expert (NP3) | ✅ PASS |
| Value non fabriquée (🟢 sur ✅ + survit ±2 pts ; exotiques EV « — ») | ✅ PASS |
| Préférences gravées (nul jamais en boîte ; combo 2-vainqueurs OK ~2,0+ ; jamais ~1,3) | ✅ PASS |
| Recherche web réelle + 📣 visible et tracée | ✅ PASS |
| Zéro inventé ; zéro bankroll ; **arithmétique des exemples recalculée et exacte** | ✅ PASS |
| Anti-sur-contrainte + allègement (12 règles, plus court que v12) | ✅ PASS |
| `deep-research` jamais utilisé | ✅ PASS |

**Arithmétique vérifiée (linter final + Agent 0)** : Verdon 1X2 @2,15 → EV +9,7 % ; seuil 1,5 pt × 2,15 = 3,2 % ; bornes ±2 pts +5,4 % / +14,0 % (toutes > seuil) ; Shin 49/27/24 = 100 % ; combo deux-vainqueurs 0,49 × 0,53 = 26 %, 2,15 × 1,80 = 3,87 ; anti-pattern nul @3,40 +4,0 % → −2,8 % à −2 pts. **0 erreur, 0 nombre fabriqué, 0 contradiction.**

## 6. Verdict du Council
- Draft : moyenne **8,34/10** (5 conseillers), bloqué par les 5 BLOCKER + value fabriquée.
- **Version finale corrigée (re-vote) : 9,5/10**, `pass` unanime sur les 5 lentilles (quant 9,4 · créativité 9,4 · passionné-expert 9,4 · Betclic/provenance 9,6 · Claude/sobriété 9,7), **0 blocker, 0 major**. Linter arithmétique **PASS**, auditeur forensique **PASS** (causes racines de v12 fermées de façon structurelle). `all_pass = true`.

**Verdict final (Agent 0).** Livrable conforme au méga-prompt v4 : NP1-NP4 corrigés, préférences gravées (nul hors boîte, combo deux-vainqueurs bienvenu ~2,0+), value non fabriquée, vérification Betclic active, génération créative d'angles, reads de passionné-expert, recherche web + 📣 tracée, no bankroll, b+a, plancher d'action — le tout **plus court et plus tranchant que v12**, et **sans jamais `deep-research`**. Aucune promesse de profit ; seulement un meilleur process, honnête et ancré sur des cotes Betclic réellement vérifiées.

## 7. 📦 Livrables
1. **`PROMPT-PARIS-FINAL-v13.md`** — le prompt quotidien, collable seul.
2. **`AUDIT-LOG-v13.md`** — ce document.

*(v12 conservé dans le repo comme version précédente. Le contenu « 📣 ce que dit le net » est intégré inline dans v13 — pas de fichier séparé.)*
