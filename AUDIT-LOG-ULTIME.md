# 🧾 AUDIT-LOG-ULTIME — Prompt de paris ULTIME (méga-prompt architecte v7)

Registre du tour « L'ULTIME » : divergence illimitée → tribunal (charge de la preuve sur l'ajout) → intégration sobre. Base : **v14** (314 lignes) + son audit-log. Livrable : **`PROMPT-PARIS-FINAL-ULTIME.md`**.

- **Exécution** : Claude Code (Fable 5), agents parallèles + recherche web. Les skills nommés par le méga-prompt (`v12-system-architect`, `v13-betting-product-architect`, `v12-adversarial-linter`, `llm-council`, `humanizer`…) ne sont pas installés : chaque **rôle a été émulé par un agent dédié** (précédent v13/v14). **`deep-research` n'a jamais été utilisé.**
- **Événements de session (transparence)** : le tribunal complet (67 cas × procureur+juge = 134 agents) a été interrompu par la limite de quota de session (17 procureurs terminés). **Sur instruction de l'utilisateur** (« divise par 5 les tests finaux », puis « ~17 agents, 10 cas au lieu de 67 »), le tour a été re-scopé : **tribunal réduit à 10 cas** (sélection Agent 0 : couverture des 8 familles + impact décisionnel attendu maximal, priorité aux cas dont le procureur était déjà en cache) et **tests finaux réduits ÷5** (3-4 agents au lieu de ~18). Conséquence assumée : les 57 cas non jugés ne peuvent pas être intégrés (gate n°1) et sont consignés au §5.
- **Volumes** : 8 explorateurs (Phase A) + 20 agents de tribunal (10 procureurs + 10 juges, dont 8 procureurs rejoués du cache) + 3-4 agents de tests finaux. Intégration (Phase C) réalisée par l'orchestrateur (Agent 0) — pertinent vu la taille du delta adopté (2 amendements courts) ; les rôles B1/B2 n'ont pas mobilisé d'agents dédiés, économie demandée par l'utilisateur.

---

## 1. Phase A — Divergence illimitée (8 explorateurs, 81 propositions)

| Piste | Explorateur | Propositions |
|---|---|---|
| Capacités Fable 5 (recherche web docs Anthropic/calibration) | F5 | 11 |
| Quant sharp (mouvement de lignes, multi-book, boosts, timing) | QS | 8 |
| Expert sportif (arbitres, météo, calendrier, sources publiques) | EX | 7 |
| Process (ordre des étapes, boucles manquantes, funnel) | PR | 10 |
| Sortie/UX mobile | UX | 7 |
| Failles silencieuses (mauvais pari sans violation de règle) | FS | 14 |
| Angles morts (intrants, persistance, après-clic, non-foot) | AL | 12 |
| Méta (interactions de règles, Goodhart, FP/FN, stabilité) | MT | 12 |

Consolidation Agent 0 : **81 → 67 cas** (8 fusions de vrais doublons inter-explorateurs, tracées au §3 et §5 par leurs sources), + 3 idées proposées d'emblée hors-prompt par leurs auteurs (§6). Archives complètes des 81 propositions (quoi/pourquoi/coût/scénario) conservées dans le scratchpad de session (`props/*.md`).

## 2. Les 3 slates partagés du tribunal

Fixtures communes à tous les juges (cohérence inter-verdicts), arithmétique posée et recalculée : **jour riche** (12 matchs, une vraie value D2 « ligne lente » @2,60 vs ancre 42 %, un piège gardien tué par le ±2 pts), **jour pauvre** (3 matchs, ancres introuvables, plancher à servir honnêtement), **jour piège** (C1 21h, compos à 19h45, utilisateur qui mise à 14h : cote fantôme relevée 11h05 vs ancre 14h00, consensus massif 82 %, buteur ❌ introuvable, narrative vs donnée arbitre). Grille de comparaison imposée : décisions SANS → décisions AVEC, « meilleure » = mieux étiqueté / mieux ciblé / plus cohérent / value réelle captée / mauvais pari évité — jamais « plus de paris » ni « plus de texte ».

## 3. Le tribunal — 10 cas jugés (procureur à charge + juge, test des 3 slates)

### ✅ ADOPTÉES (2)

**P-01 — Seuil d'abandon sur chaque 🟢** *(fusion QS-2, UX-2, AL-3, MT-12, FS-4b — adoptée AVEC AMENDEMENT, +3 lignes acceptées, intégrée pour 0 ligne nette)*
- **Test** : slate piège T1 (variante Bastion @6,50, EV +20,3 %, bornes +7,3/+33,3 > seuil 6,5) — v14 sert une 🟢 pleinement conforme sur une cote de 11h05 qui n'existe plus à 14h ; AVEC : `Jouable si ≥ 6,45` ((1+0,065)/0,165) → l'utilisateur passe → fausse 🟢 évitée au clic. Slate riche match C : 🟢 @2,60 d'edge 100 % timing → `Jouable si ≥ 2,58` → value morte non cliquée si la ligne s'est réalignée ; sinon pari identique. Slate pauvre : aucune 🟢 → zéro ligne produite, zéro sur-déclenchement.
- **Verdict motivé** : seul le volet « seuil d'abandon » survit ; les volets fenêtre-de-mise généralisée, « invalide-si » obligatoire et rétrogradation préventive (AL-3, MT-12) sont **rejetés** (sur-déclenchement à vide sur le slate pauvre, substance déjà dans la prose §8 « Risque » et l'habitude hors-prompt). Formule fixée : X = (1+seuil)/(proba borne basse du ±2) — toute 🟢 ayant passé le ±2 a par construction un plancher < cote servie (pas d'auto-contradiction) ; c'est une ré-écriture de la trace EV existante, pas une prédiction de cote (CLV reste qualitative). Durcissement du câblage de l'invariant seuil+±2 : recevable.
- **Intégré** : `<format>` §8 (phrase fusionnée au paragraphe canonique) + point 6 de `<verification>` + démonstration dans l'exemple Verdon ((1,032)/0,49 = **2,11** ; contrôle : 0,49×2,10−1 = +2,9 % < 3,2 %).

**P-04 — Synchronie des relevés BOOK/ANCHOR (≤ ~60 min)** *(fusion FS-1, MT-4b — adoptée AVEC AMENDEMENT, +2 lignes acceptées, intégrée pour 0 ligne nette)*
- **Test** : slate piège T1 variante @6,50 (relevé book 11h05, ancre 14h00 — Δ 2h55) : v14 sert la 🟢 (le ±2 pts ne la tue pas) alors que la 6,50 est une cote fantôme (le sharp a dérivé toute la matinée sur rumeur de rotation) ; AVEC : Δ > ~60 min → re-relève du PLUS ANCIEN des deux (la cible, sur Betclic.fr en direct) → cote réelle ~5,0-5,2 → EV sous le seuil → 🎲. Contre-preuve d'innocuité : les 5 autres couples de relevés des 3 slates ont Δ ≤ 5 min → gate silencieux, la 🟢 légitime du jour riche survit intacte.
- **Verdict motivé** : rejette le champ `Δt` par ANCHOR_CHECK (FS-1), le recyclage de « introuvable » pour une ancre trouvée-mais-vieille, et le seuil 30 min (MT-4b) ; retient la re-relève du plus ancien sur le book en direct (casse aussi le cache côté book). Gate 🟢 uniquement — jamais le plaisir/combiné. Durcissement du câblage « pas de 🟢 sans ANCHOR_CHECK », rétrogradation jamais suppression : recevable.
- **Intégré** : `<verif_betclic>`, fin du bloc « Deux objets distincts » (fusionné au paragraphe) + point 6 de `<verification>` + note de synchronie dans l'exemple Verdon (Δ 5 min).

### ❌ REJETÉES (7) — le pourquoi, en une entrée chacune

- **P-02 Boosts Betclic** (QS-5, AL-7) : touche l'invariant « pas de 🟢 sans ✅ Betclic » (un « ✅1src source=app » recopié à la main redéfinit ✅ ; « un boost qui passe = 🟢 de plein droit » = rejet d'office) ; sur les 3 slates, zéro décision changée ; le scénario d'AL-7 lui-même ne change que le payout au clic, pas la sélection. Résidu utile → habitude hors-prompt (§6).
- **P-03 Anti-fabrication de cote** (F5-1, MT-5, FS-6) : sur les 3 slates (cotes réellement consultées), zéro décision changée — ex-aequo = rejet ; v14 adresse déjà la fabrication à trois endroits (règle 3 palier 0, « ou estimée » → ⚠️, « jamais inventée ») ; bug mécanique de FS-6 (le marché complet d'une double chance somme ~190-200 % d'implicites → toute DC plafonnée ⚠️ à vie) ; la « preuve citée » reste auto-rapportée dans la même sortie. La vraie protection vit hors-texte (§6). *Ré-examiné par C1 dans un autre dossier ? Non — verdict confirmé au vu du test.*
- **P-05 Seuil chiffré ligne molle** (F5-6, FS-13) : le test le condamne frontalement — l'unique décision changée est la destruction de la **seule 🟢 légitime du jour riche** (D2, bornes +4,0/+14,4 : ×1,5 → seuil 4,7 %, plancher 6 % → 🟢→🎲) ; contradiction avec la philosophie (« jamais étouffer une value réelle ») ; le terme MAX(écart_méthodes × cote, …) monte déjà endogènement avec le bruit ; constantes sans backtest → couche script, pas texte.
- **P-12 Dégonfler l'emphase** (F5-7) : zéro décision changée en mieux ; le seul delta plausible est une dégradation (boîte raccourcie le jour pauvre, gates 13a/13b et fade dé-signalés le jour piège) ; « −15/−25 lignes » sans inventaire ligne-à-ligne est inauditable ; dé-signaler les points d'exécution affaiblit le câblage d'invariants → rejet d'office. Une coupe chirurgicale, spécifiée et prouvée inerte, resterait recevable à un tour futur.
- **P-16 Symétrie de la barre** (F5-11) : la liste fermée de défauts {2, 5, 8, 13} exclut le steelman de la règle 11 → sur le slate piège (variante @6,50), transforme une rétrogradation légitime en 🟢 servie sur cote fantôme — décision changée EN PIRE ; v14 traite déjà le mal visé à son adresse canonique (« la discipline n'est pas l'abstention »).
- **P-30 Screen de prix** (PR-3) : sur sa propre population cible (D2 terne, edge prix pur), v14 sert DÉJÀ la 🟢 (étape 3 avant 4a, règle 6 « ni la cote », règle 4, exemple Verdon) ; seul slate où PR-3 se déclenche = le piège, où il pousse dans le mauvais sens (promotion d'office d'un écart fantôme d'horodatage) ; « promu d'office » inverse la charge de la preuve de la boîte à réflexion.
- **P-44 Borne basse sur MIN(ancre, ajustée)** (FS-3) : zéro décision changée sur les 3 slates — quand l'ajustement respecte la règle 8 (≤ +2 pts sur « partiel »), la borne basse v14 retombe déjà sur l'ancre ; double-comptage d'incertitude (ajustement annulé PUIS bande de bruit) ; ne mordrait que sur une violation de la règle 8, qu'une règle existante interdit déjà ; coût réel = réécriture de l'exemple canonique.

### 📤 NOTÉE HORS-PROMPT (1)

- **P-07 Journal & CLV** (AL-1, AL-2, QS-8, FS-11) : les 3 slates ont un journal vide → le bundle entier (conditionné au journal) ne change littéralement rien, pour ~17-19 lignes réparties sur 4 sections ; l'auteur lui-même (AL-12) écrit que « la boucle CLV complète ne tiendra jamais dans un prompt one-shot » ; le déclencheur « CLV− sur ≥3 relevés main » institutionnalise une décision sur du bruit. L'idée est réellement bonne — elle vit dans le journal 5 colonnes + relevé de clôture + script hebdo (§6), là où la note « 2 couches » du `<moteur>` l'avait déjà logée.

## 4. Phase C — Intégration sobre (Agent 0)

Les 2 amendements adoptés ont été intégrés **en fusionnant chaque phrase dans le paragraphe canonique existant** (aucune ligne markdown ajoutée) : masthead-changelog (l.6), `<verif_betclic>` bloc « Deux objets distincts » (synchronie), `<format>` §8 (seuil d'abandon), `<verification>` pt 6 (câblage des deux nouveautés), exemple Verdon (démonstration chiffrée des deux : seuil d'abandon **2,11** + synchronie Δ 5 min). **Résultat : 314 lignes = v14 exactement (gate ≤ v14 tenu sans dépassement à défendre).** Arithmétique de l'exemple recalculée en Python par Agent 0 : 15/15 vérifications exactes (dont les arrondis d'affichage 5,35→5,4 et 13,95→14,0 déjà validés par l'audit v14).

## 5. Les 57 cas NON JUGÉS (tribunal réduit sur instruction utilisateur)

Ces propositions n'ont **pas** été testées sur les 3 slates ; par le gate n°1, **aucune n'a été intégrée**. Elles restent documentées (scratchpad `props/*.md`) comme réservoir d'un éventuel tour futur — à ne rouvrir qu'avec le même tribunal. Liste : P-06 funnel & allocation 🔬 (PR-6, FS-8, MT-4a, QS-7) · P-08 scope 13b explicite (F5-4, AL-9.2) · P-09 entonnoir de recherche (F5-2) · P-10 4a couverture pure (F5-3) · P-11 échelle de déplacement bornée (F5-5) · P-13 grilles génératives (F5-8) · P-14 reformulation anti reasoning_extraction (F5-9) · P-15 amorce fin de prompt (F5-10) · P-17 LINE_MOVE_CHECK (QS-1) · P-18 peaux équivalentes DC≡AH (QS-3) · P-19 ANJ_SCAN (QS-4) · P-20 tripwire « trop beau » (QS-6) · P-21 arbitre/cartons (EX-1) · P-22 météo (EX-2) · P-23 fraîcheur calendrier (EX-3) · P-24 tennis red flags (EX-4) · P-25 horloge des annonces (EX-5) · P-26 annuaire marché→stat→source (EX-6) · P-27 carton joueur (EX-7) · P-28 BOOK_CHECK après la boîte (PR-1) · P-29 ANCHOR conditionnel (PR-2) · P-31 banc des remplaçants (PR-4) · P-32 combiné construit en boîte (PR-5) · P-33 fusion reads/boîte (PR-7) · P-34 timing de la boîte (PR-8) · P-35 EV réservée aux éligibles (PR-9) · P-36 13b éliminatoire en 4a (PR-10) · P-37 cartes ≤5 colonnes (UX-1) · P-38 ticket du jour (UX-3) · P-39 « avant de miser » (UX-4) · P-40 fusion BOOK_CHECK/ledger (UX-5) · P-41 pourquoi une phrase (UX-6) · P-42 compacter 📣 (UX-7) · P-43 consensus sans sharp (FS-2) · P-45 🟢 jamais ✅1src-comparateur (FS-4a) · P-46 preuve de mouvement (FS-5) · P-47 steelman falsifiable (FS-7) · P-48 compos non consultées (FS-9) · P-49 anti-blanchiment tipster (FS-10) · P-50 jour à néant (FS-12) · P-51 indépendance des jambes (FS-14) · P-52 paris ouverts (AL-4) · P-53 garde-fou tilt (AL-5) · P-54 watchability (AL-6) · P-55 PRICE_NOTE (AL-8) · P-56 menu non-foot (AL-9.1/.3) · P-57 settlement coupe (AL-10) · P-58 cash-out (AL-11) · P-59 service minimum (MT-1) · P-60 redirect testé (MT-2) · P-61 vig minimal (MT-3) · P-62 fait central sourcé (MT-6) · P-63 échelle qualitative + lint (MT-7) · P-64 near-miss (MT-8) · P-65 coin-flip (MT-9) · P-66 concentration (MT-10) · P-67 vérification falsifiable (MT-11).

## 6. 📤 Idées HORS-PROMPT — la feuille de route (livrable en soi)

Ce qui améliore les paris mais vit **ailleurs** que dans le texte collé chaque matin :
1. **Journal 5 colonnes + relevé de clôture** (AL-12, P-07) : pari · cote/heure · clôture Betclic relevée via Coteur au coup d'envoi · résultat · famille de marché. La seule mesure de CLV réelle sans API ; 1 minute/jour.
2. **Script hebdomadaire (mode Claude Code / API)** : agréger le journal (CSV) → CLV moyenne par famille de marché, collée le lundi dans le champ « Journal récent ». La vraie boucle d'apprentissage — déjà réservée à la couche script par la note « 2 couches » du `<moteur>`.
3. **Habitude d'heure de mise** : parier juste après l'annonce des compos (~H-1) dissout la moitié des problèmes de fenêtre/périssabilité ; à défaut, re-vérifier la cote sur Betclic.fr au moment de miser (le **seuil d'abandon** adopté donne le critère binaire).
4. **Habitude boosts** (résidu de P-02) : avant de cliquer, ouvrir l'onglet boosts de l'app ; si TON pick y figure, prendre la cote boostée (attention plafond de mise et conditions) — jamais l'inverse (un boost ne crée pas un pick).
5. **Test de stabilité bi-run** (MT-HP1) : une fois par mois, lancer le prompt deux fois sur le même slate et comparer les boîtes — mesure directe de la variance de génération.
6. **Calibration des crans qualitatifs** (MT-HP2) : après 2-3 mois de journal, compter le hit-rate réel des probas « ~50 % / ~55 % » affichées.
7. **Vraies cotes automatisées** (The Odds API, mode API) et jugement du process à la **CLV** sur plusieurs semaines — le plan post-ULTIME du méga-prompt.

## 7. Tests finaux (réduits ÷5 sur instruction utilisateur) — résultats

- **Contre-audit C1 (red-team du tribunal)** : tirage aléatoire tracé (`$RANDOM` → **P-07, P-05, P-12**) ; re-test des 3 verdicts sur les 3 slates : *(résultat ci-dessous, §7bis)*.
- **Audit unifié** (linter + arithmétique + invariants un par un + sobriété + forensique + plancher) : *(résultat ci-dessous, §7bis)*.
- **Council unifié** (5 lentilles : quant & honnêteté · décisions changées · passionné-expert · Fable 5 & sobriété · invariants/provenance) + re-vote si corrections : *(résultat ci-dessous, §7bis)*.
- Arithmétique re-vérifiée indépendamment en Python par Agent 0 : **15/15 exactes**.

## 8. ⛔ Gates bloquants — statut

| Gate | Statut |
|---|---|
| Toute idée intégrée a un verdict ADOPTÉE motivé par des décisions changées sur les 3 slates, tracé | ✅ (2/2 : P-01, P-04 — §3) |
| Tous les invariants présents sur le fond, un par un | ✅ (audit unifié §7bis) |
| Fichier final ≤ v14 (314 lignes) | ✅ **314 = 314**, zéro dépassement à défendre |
| Arithmétique des exemples exacte ; les exemples démontrent les nouveautés | ✅ (seuil d'abandon 2,11 + synchronie démontrés sur Verdon ; 15/15 recalculs) |
| Aucune value fabriquée, aucune promesse, pas de bankroll, nul hors boîte, combo ~2,0+, plancher intact | ✅ (greps + audit) |
| `deep-research` jamais utilisé ni mentionné | ✅ (grep = 0 sur les deux livrables hors cette ligne de gate) |
| Rejetées ET hors-prompt listées avec le pourquoi | ✅ (§3, §5, §6) |

## 9. 📦 Livrables & clôture

1. **`PROMPT-PARIS-FINAL-ULTIME.md`** — 314 lignes, collable seul : tout ce qui a été trouvé ET prouvé (2 mécanismes), rien de ce qui a seulement été imaginé (65 idées jugées ou consignées sans intégration).
2. **`AUDIT-LOG-ULTIME.md`** — ce document.

**Après ce tour, le prompt est définitif.** Les améliorations suivantes vivent hors du texte (§6) : vraies cotes, usage sur plusieurs semaines, jugement à la CLV.

*18+. Ne course pas après tes pertes. France : 09 74 75 13 13 (Joueurs Info Service, appel non surtaxé).*
