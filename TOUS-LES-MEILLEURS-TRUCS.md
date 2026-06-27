# 🧰 TOUS-LES-MEILLEURS-TRUCS — collecte de l'escadron recherche

Toutes les meilleures méthodes / techniques / données trouvées par les 6 escadrons de recherche (web), avec la **décision d'intégration** (✅ intégré · 🟡 intégré avec prudence · ❌ écarté) et **pourquoi**. Le prompt final est `PROMPT-PARIS-FINAL.md`.

> Principe directeur : on optimise le **process** (jouer intelligemment, capter la vraie value quand elle existe), **jamais** le profit. Tout ce qui promettait un edge garanti a été écarté.

---

## R1 — Prompt engineering spécifique à Claude

| Technique | Décision | Pourquoi / où |
|---|---|---|
| **Structure XML** par blocs nommés (`<role>`, `<philosophie>`, `<regles>`, `<moteur>`, `<format>`…), données en haut, requête en bas | ✅ | Claude est entraîné à reconnaître les balises XML ; sépare consignes / data / exemples. *(Doc Anthropic — Structure prompts with XML tags / Long context)* |
| **Anti-sur-contrainte** : ≤ ~12 règles dures, supprimer MAJUSCULES / « TU DOIS » / « JAMAIS » | ✅ | Empiler les contraintes fait chuter le suivi (−19 %) ; les modèles récents **sur-déclenchent** sur « CRITICAL/You MUST ». → 12 règles priorisées, le reste en guide souple. *(arXiv 2407.03978 ; Anthropic best practices)* |
| **Framing positif** (dire quoi faire, pas quoi éviter) | ✅ | « Retiens un pari si l'edge dépasse le seuil » > « ne parie jamais sans edge » (problème de l'éléphant rose). *(Anthropic — Control the format)* |
| **Permission d'incertitude** (« je ne sais pas ») | ✅ | Réduit les fabrications ; intégré via « donnée indisponible » et NARRATIF non actionnable. **Mais** la permission d'incertitude ≠ permission de NE PAS jouer : voir l'arbitrage Agent 0 (AUDIT-LOG §5). |
| **Ancre marché = prior explicite**, écart borné + justifié | ✅ | Les LLM sont surconfiants, leur confiance verbalisée sature (0,9/1,0). → règle 1 + 12, ajustement tracé. *(arXiv 2410.09724 ; 2509.25532)* |
| **Pas de score de confiance numérique libre** | ✅ | Chiffre peu fiable → fausse précision dangereuse. → conviction **qualitative** (faible/moyenne/haute), EV dérivée des chiffres. |
| **Self-check final léger single-pass** (CoVe simplifiée) | ✅ | La CoVe complète coûte +300-400 % de tokens. → `<verification>` 6 points bornés. *(arXiv 2309.11495)* |
| **Donner le *pourquoi*** des règles + few-shot diversifiés | ✅ | Le modèle généralise depuis l'explication ; exemples dans `<exemple>` (jour normal, jour pauvre, données manquantes). |
| **Self-consistency multi-tirages** | ❌ | Coût ×5-10 ; cohérence ≠ factualité ; à faire au niveau orchestration, pas dans le prompt quotidien. |
| **Step-back prompting** (étape dédiée) | ❌ | Le prior marché joue déjà ce rôle d'ancrage haut niveau ; ajouter une étape alourdit (anti-sur-contrainte). |

## R2 — Quant paris

| Technique | Décision | Pourquoi / où |
|---|---|---|
| **Dévig par méthode** : multiplicatif (équilibré) / **power** (favori lourd, 2-issues) / **Shin** (1X2, 3-issues) | ✅ | L'écart entre méthodes croît avec le déséquilibre/vig → sert de mesure d'incertitude. → moteur étape 2 + règle 6. *(betherosports, outlier.bet, datawisebets)* |
| **`EV = p × cote − 1`** + breakeven 52,4 % (vig std) / 50 % (no-vig) | ✅ | Formule centrale ; règle 3 + colonne EV du tableau. |
| **Seuil de value dépendant de la cote**, edge < ~2-3 % ou < écart méthodes → pas de value, **plus d'edge exigé sur outsiders** | 🟡 | Adopté **qualitativement** (le ~2-3 % est un *repère*, pas une constante). Buckets chiffrés par tranche **écartés** (réintroduisaient des « nombres magiques »). *(rebelbetting, opticodds)* |
| **CLV** = meilleur prédicteur empirique du process (battre la clôture sharp, ~300-500 paris) | ✅ | Métrique de qualité **du process, jamais une promesse de gain**. → philosophie + règle 11 + colonne « CLV attendu » (direction qualitative). *(Pinnacle / Buchdahl)* |
| **Combinés same-match (SGP)** : corrélation tax ~20-25 %, **jamais `p1×p2` naïf**, structurellement −EV | ✅ | Règle 7 ; proba réelle de toucher toujours affichée ; combiné multi-matchs 2 jambes max, indépendantes. |
| **CLV-anticipé chiffré** (« +0,06 », cote de clôture prédite) | ❌ | Nombre prédictif **halluciné** (le LLM est plus lent que le marché près de la clôture). → remplacé par une **direction** qualitative. *(fail A2, endossé C1)* |
| Modèles **Poisson / Dixon-Coles / Elo** (tennis par surface) | 🟡 | Gardés comme **cadre qualitatif** (draws/scores faibles sous-estimés, time-decay, écart Elo ≈ but), gains marginaux +1-3 % → ne pas s'écarter fortement de la ligne sharp. |
| **LLM = synthétiseur calibré, pas oracle** (Prophet Arena, Schoenegger 2024) | ✅ | Cadrage honnête de la philosophie ; estimateur faible vs marché. |
| **Sizing / Kelly** | ❌ | **Bankroll supprimée** (changement imposé n°1) — aucun montant, aucune unité, aucune fraction de Kelly. |

## R3 — Sentiment & pronostiqueurs en ligne

| Technique | Décision | Pourquoi / où |
|---|---|---|
| **Parsing 2 colonnes** : claim vérifiable vs pick/opinion (poids du pick autonome = 0) | ✅ | Moteur étape 5 + règle 8. Seul l'info vérifiable peut bouger la proba. |
| Sous-module **« suivre un prono »** (checklist a/b/c/d, rejet si a ou b échoue) | ✅ | (a) raison vérifiable ? (b) ligne encore ≤ entrée du tipster ? (c) cohérent avec le sharp ? (d) sources non corrélées ? |
| **Test du mispricing nommable** | ✅ | Nommer l'info, vérifier si la ligne a déjà bougé → si oui, déjà price → pas de value. Sert aussi de **porte de sortie** à la règle de prudence. |
| **Biais du survivant** + dédup des sources corrélées (écho-chamber = 1 source) | ✅ | Track record auto-rapporté ignoré sauf horodaté, > 200 paris, mesuré en CLV. |
| Juger les tipsters sur la **CLV**, jamais sur les screenshots | ✅ | Cohérent avec la philosophie « process > résultat ». |

## R4 — Analyse sportive profonde

| Technique | Décision | Pourquoi / où |
|---|---|---|
| **« Chiffre avant interprétation »** : tactique sans donnée = « NARRATIF — non actionnable » | ✅ | Règle 4 + moteur étape 3 (sinon « SPÉCULATIVE », exclu). |
| Champ **« déjà price ? »** (oui/partiel/non) par argument | ✅ | Anti-double-comptage (règle 5) : seuls partiel/non ajustent la proba. L'edge = écart au marché, pas force absolue. |
| **Grilles par sport** (foot : Press/Press & set-pieces ; tennis : surface > serve/return > fatigue > H2H filtré ; US : repos/back-to-back) | ✅ | Moteur étape 3, « à remplir, pas un récit ». |
| **Grille fallback autres sports** (basket/rugby/hockey/MMA/e-sport) | ✅ | Comble le trou de couverture relevé par A3 : cadre général + 2-3 drivers dominants. |
| **Steelman systématique + hypothèse nulle** | ✅ | Règle 9 + moteur étape 6 : « et si le marché price déjà juste et que mon facteur est faux/intégré ? ». |
| Constantes (CPA ~⅓ des buts, marge SGP ~20-25 %) | 🟡 | Gardées comme **repères heuristiques généraux**, explicitement **« à ne jamais ressortir comme une stat du match du jour »**. *(fail A2/A5, endossé C1)* |

## R5 — Données & API (intégration concrète)

| Source | Décision | Usage recommandé |
|---|---|---|
| **Clôture Pinnacle dévigée** (via Oddspedia / Coteur en France) | ✅ ancre | La proba « vérité » ; books FR = **cible de mise**, jamais ancre. |
| **The Odds API** (cotes) | ✅ | Requêtes ciblées (1 marché / 1-2 régions) pour économiser les crédits. |
| **API-Football** (compos, blessures, sidelined) | ✅ | Gratuit, ~100 req/jour, officiel. Clé en variable d'env, cache CSV. |
| **Understat** (xG, 5 grandes ligues) | ✅ | Cache local. |
| **Sackmann `tennis_atp/wta`** (Elo par surface) | ✅ | `git pull`, Elo surface-spécifique pour le tennis. |
| **football-data.co.uk** (colonnes *C / PSC) | ✅ | Mesure du **CLV** hebdomadaire vs clôture Pinnacle — KPI honnête du process. |
| **Architecture 2 couches** (script déterministe calcule no-vig/Elo/CLV ; le LLM ne fait que tactique + go/no-go) | 🟡 | **Recommandée pour un usage avancé/automatisé** (réduit le risque de calcul no-vig hallucineé). Hors périmètre du prompt collable seul, mais documentée ici comme la meilleure intégration data. |
| **SofaScore en pipeline** | ❌ | API non officielle, fragile, risque de ban. Consultation manuelle d'appoint au plus. |

> **Note d'usage pour ce projet (repo `newbet`)** : aucune clé d'API n'est présente dans le repo. Le prompt v11 fonctionne **dès aujourd'hui** en mode « recherche web activée » (l'utilisateur relève les cotes Betclic/Winamax + sharp via Oddspedia/Coteur). L'architecture 2 couches ci-dessus est la voie d'industrialisation si on veut plus tard automatiser le relevé des cotes et le calcul no-vig hors LLM.

## R6 — Anti-sur-contrainte & graceful degradation

| Technique | Décision | Pourquoi / où |
|---|---|---|
| **Hiérarchie de priorité explicite** des règles (conflit → la règle la plus haute gagne) | ✅ | En-tête de `<regles>` + Top-3 non-négociables. Évite les paires d'ordres absolus qui se contredisent. |
| **Directives positives** ; négatif réservé aux vraies barrières (no-profit) | ✅ | Cohérent avec R1. |
| **Rationale + exemples canoniques annotés** (pari retenu, jour pauvre, données manquantes) | ✅ | `<exemple>` couvre les 3 cas, indispensable car la carte change chaque jour. |
| **Phases modulaires nettes** + self-check léger | ✅ | Moteur 6 étapes + `<verification>`. |
| **« Plancher d'ACTION garanti, jamais plancher de PARIS »** (no-bet = résultat valide) | ❌ (arbitré) | **Écarté par l'Agent 0.** R6 (et R1) poussaient à valoriser le no-bet ; c'est défendable en pur +EV mais **contredit frontalement** le méga-prompt (gate n°1 « plancher d'action incassable, jamais 'aucun pari' » + « toujours b + a »). Résolution : honnêteté **par l'étiquetage** (plaisir ≠ value), pas par l'abstention. Voir **AUDIT-LOG §5**. |

---

## 🎁 Synthèse — les « meilleurs trucs » réellement embarqués dans v11

1. **Ancre marché dévigué comme prior** ; le LLM nuance, ne remplace pas.
2. **Dévig multi-méthodes** (mult/power/Shin) + l'écart entre méthodes comme mesure d'incertitude.
3. **Deux grandeurs séparées** : `ECART_PROBA` (diagnostic) vs `EV = p×cote−1` (porte le seuil) — corrige un vrai bug de définition.
4. **Anti-double-comptage** systématique (« déjà price ? ») — l'edge est l'écart au marché, pas la force absolue.
5. **Lecture tactique grounded** (« chiffre avant interprétation », grilles par sport, fallback générique).
6. **Steelman + hypothèse nulle** avant toute conclusion.
7. **Sentiment discipliné** : claim vérifiable vs pick brut, checklist « suivre un prono », mispricing nommable, biais du survivant.
8. **Combinés honnêtes** : pas de `p1×p2` naïf, corrélation tax assumée, proba réelle de toucher toujours affichée.
9. **Traçabilité** : evidence ledger (cote + book + heure), CLV en **direction** qualitative (jamais un nombre halluciné).
10. **Honnêteté** : variance assumée, process jugé sur la CLV, **aucune promesse de profit ni de pari « sûr »**.
11. **Anti-sur-contrainte** : XML, ≤ 12 règles priorisées, framing positif, guides souples.
12. **Couverture large + radar** : toute la carte, compétitions discrètes incluses, rien de silencieusement jeté.
13. **Sans bankroll** : qualité/proba/value uniquement, mises libres, un seul garde-fou (ne pas courser + ligne d'aide).
14. **Plancher d'action + toujours b + a** : un pari plaisir + un combiné servis chaque jour, étiquetés honnêtement ; la value pure peut être vide et on le dit.
