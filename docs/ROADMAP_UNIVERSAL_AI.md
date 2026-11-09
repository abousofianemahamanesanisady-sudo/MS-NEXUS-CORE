# MS NEXUS AI — Feuille de route de réalisation

**Priorité validée :** moteur d'intelligence d'abord.  
**Vision :** intelligence universelle et studio de création technologique.  
**Statut :** plan de réalisation ; les jalons ci-dessous ne sont pas déclarés terminés.

## Règle de progression

Chaque phase doit produire un livrable démontrable, des tests reproductibles et une documentation mise à jour. Ne pas démarrer plusieurs moteurs lourds simultanément. Ne pas engager de service payant sans décision budgétaire explicite.

## Phase 0 — Stabiliser la fondation existante

**Objectif :** connaître précisément ce qui fonctionne déjà.

- Cartographier les routes API, modèles de données, workers et variables de configuration.
- Exécuter les tests existants et ajouter des tests de contrats API.
- Vérifier authentification, CORS, limites de taille et erreurs.
- Vérifier les états runtime et distinguer configuré / disponible / testé.
- Documenter les limites du Worker Cloudflare de bootstrap par rapport au backend FastAPI.

**Livrable :** rapport d'état technique et tests de santé fiables.  
**Critère de sortie :** les routes principales et leurs dépendances sont couvertes par des tests automatisés.

## Phase 1 — Intelligence centrale (priorité)

**Objectif :** transformer le chat existant en moteur orchestré.

1. Définir un contrat commun de tâche : `task_id`, utilisateur, type, entrée, permissions, budget, état, résultat et erreurs.
2. Construire le registre des capacités et des modèles.
3. Construire le routeur de modèles selon tâche, disponibilité, licence, ressources et coût.
4. Ajouter un orchestrateur simple : classifier → planifier → exécuter → vérifier → répondre.
5. Ajouter des tâches asynchrones persistantes et la reprise après erreur.
6. Ajouter une mémoire de projet explicite, isolée par utilisateur/projet et contrôlable.
7. Ajouter des journaux d'audit, métriques et limites d'exécution.
8. Définir un jeu de tests en français : compréhension, instruction, raisonnement, code, refus sûr et robustesse.
9. Comparer le modèle de base sur ce jeu avant toute personnalisation.

**Livrable :** NEXUS Orchestrator v1 avec un seul moteur texte réel et au moins un workflow multi-étapes testable.  
**Critère de sortie :** une mission est planifiée, exécutée, vérifiée et restituée avec un historique fiable.

## Phase 2 — Données et personnalisation du modèle

- Construire un dataset de qualité à partir de contenus autorisés.
- Définir format, provenance, licence, langue, déduplication et critères de qualité.
- Séparer données d'entraînement et d'évaluation.
- Établir une baseline et des métriques.
- Tester un fine-tuning LoRA/QLoRA sur un petit modèle compatible avec le matériel disponible.
- Comparer avant/après ; conserver le modèle de base si le résultat régresse.
- Versionner dataset, configuration, adaptateur et rapport d'évaluation.

**Livrable :** premier adaptateur fine-tuné expérimental et rapport comparatif.  
**Critère de sortie :** amélioration mesurée sur des tâches ciblées sans régression inacceptable.

## Phase 3 — Agents et outils contrôlés

- Planner, Researcher, Coder, Reviewer et Tester.
- Workspace isolé et exécutions éphémères.
- Connecteurs GitHub et Cloudflare avec permissions minimales.
- Approbation humaine pour écrire dans les dépôts, publier, déployer ou supprimer.
- Traçabilité de chaque appel d'outil et possibilité d'annuler les changements lorsque c'est possible.

**Livrable :** agent de développement capable de proposer un patch, exécuter les tests et préparer une pull request sans déploiement automatique non autorisé.

## Phase 4 — Studio APP & WEB

- Génération d'un brief, d'une architecture et d'un plan.
- Création de fichiers dans un workspace de projet.
- Builds, tests, captures et rapport d'erreurs.
- Authentification, profils, rôles, stockage et notifications via modules réutilisables.
- Export source et préparation du déploiement après approbation.

**Livrable :** une petite application mobile/web complète, reproductible et testée.

## Phase 5 — Capacités multimodales

Ordre recommandé :
1. Vision : comprendre images et documents.
2. Image : générer et éditer via moteur spécialisé.
3. Audio : transcription et synthèse vocale.
4. Vidéo : jobs asynchrones, suivi et stockage des rendus.
5. 3D : assets, scènes, formats et validation dans un moteur 3D.

Chaque modalité a un adaptateur, un test de génération réel, des limites de ressources et une indication claire des coûts.

## Phase 6 — GAME & ANIMATION STUDIO

- Génération de concepts, scénarios, storyboards et fiches de personnages.
- Production d'assets 2D/3D avec cohérence visuelle.
- Intégration à un moteur de jeu existant.
- Génération de scènes, scripts, niveaux et interfaces.
- Compilation, tests de gameplay et builds exportables.
- Pipeline d'épisodes d'animation, montage, voix et sous-titres.

**Livrable :** prototype de jeu jouable et court épisode d'animation.  
**Précision :** une expérience dite « 4D » peut ajouter mouvement, son spatial, vibration ou dispositifs sensoriels ; ces effets exigent du matériel compatible.

## Phase 7 — CONSOLE LAB, ROBOTICS & INVENTOR

- Définir les exigences matérielles et les contraintes de sécurité.
- Simuler et concevoir les composants et interfaces.
- Produire schémas, nomenclatures et prototypes numériques.
- Faire examiner les conceptions par des spécialistes.
- Construire et tester des prototypes physiques avant toute affirmation de fonctionnement.

**Livrable :** dossier technique et prototype validé en laboratoire, selon les moyens disponibles.

## Phase 8 — Plateforme et écosystème

- Comptes, organisations, espaces de projets et facturation si un jour nécessaire.
- API publique, SDK et système de plugins signé.
- Catalogue de modèles et extensions avec licences vérifiées.
- Quotas, observabilité, support, sauvegardes et gouvernance.
- Déploiement multi-région seulement si la demande et les ressources le justifient.

**Livrable :** plateforme extensible avec documentation développeur et contrôles de sécurité.

## Ordre de priorité immédiat

| Priorité | Travail | Résultat attendu |
|---|---|---|
| P0 | Audit et tests de l'existant | État réel vérifié |
| P1 | Contrat de tâches + registre | Fondations de l'orchestration |
| P1 | Routeur texte + orchestrateur v1 | Intelligence centrale utilisable |
| P1 | Évaluations françaises | Qualité mesurable |
| P2 | Dataset + fine-tuning expérimental | Personnalisation vérifiée |
| P2 | Agents + workspace sécurisé | Travail multi-étapes contrôlé |
| P3 | APP/WEB Studio | Logiciels générés et testés |
| P3 | Vision, image, audio, vidéo | Création multimodale |
| P4 | Game/Animation/3D/Console | Création avancée |

## Contraintes de ressources

- Android sert de poste de pilotage, pas de serveur GPU permanent.
- Le développement documentaire, les contrats API et les tests légers peuvent commencer sans GPU.
- Un fine-tuning nécessite un dataset, un modèle compatible et une ressource de calcul adaptée.
- Image, vidéo, 3D et entraînement lourd peuvent exiger un GPU, du stockage et un budget.
- Les offres gratuites et quotas fournisseurs changent : les vérifier avant chaque déploiement.
- Aucun coût, délai ou volume de génération illimité ne doit être promis avant mesure.

## Prochaine tâche technique

Commencer par **Phase 0 : audit de l'existant**, puis implémenter le contrat de tâches et le registre des capacités avant de construire un système multi-agents complexe.


## Phase 9 — Studios spécialisés et nouveaux domaines

Cette phase étend les studios au-delà des premiers prototypes APP/WEB et GAME. Elle est réalisée par modules indépendants, selon la demande et les ressources.

### 9A — Création et médias
- Documents, livres numériques, présentations et traduction.
- Design, image et identité visuelle.
- Audio : transcription, synthèse, voix et composition originale.
- Cinéma, animation, storyboard, montage et effets visuels.
- 3D, scènes, assets et préparation à l'impression 3D.

**Sortie :** une chaîne de production média avec fichiers exportables, licences et provenance documentées.

### 9B — Expériences immersives et jeux avancés
- Jeux 2D/3D, simulation et multijoueur.
- Pipeline de scènes, assets, scripts, builds et tests.
- VR/AR et visualisation spatiale.
- Expériences 4D avec accessoires haptiques, mouvement, vibration, vent ou audio spatial selon le matériel disponible.

**Sortie :** prototype jouable testé ; prototype immersif/4D validé sur matériel compatible.

### 9C — Ingénierie, appareils et monde physique
- OS, logiciels systèmes, pilotes et embarqué.
- Conception de consoles, contrôleurs et électronique.
- Robotique simulée puis test sur banc sécurisé.
- Drones, véhicules, énergie, bâtiments et infrastructures.
- Inventeur : CAO, schémas, nomenclatures, prototypes et dossiers de fabrication.
- Jumeaux numériques et simulations.

**Sortie :** dossiers techniques vérifiés et prototypes seulement lorsque des spécialistes, équipements et moyens de test sont disponibles.

### 9D — Sciences et services utiles
- Mathématiques, recherche, visualisation et calcul.
- Agriculture, irrigation et analyse de cultures.
- Éducation et apprentissage personnalisé.
- Santé/bien-être à visée informative et administrative, sous contrôle professionnel.
- Business, comptabilité assistée et analyse de données.
- Informations juridiques générales avec contexte de juridiction.
- Climat, environnement, transport et logistique.
- Accessibilité, traduction et langues locales.

**Sortie :** modules évalués sur des cas réels représentatifs, avec limites et validation humaine explicites.

### 9E — Écosystème et confiance
- API/SDK, plugins signés et catalogue de capacités.
- Mode local/hors ligne lorsque possible.
- Collaboration, espaces d'équipe et classe virtuelle.
- Centre de validation humaine et journal de provenance.
- Gestion des versions, restauration, coûts et ressources.
- Sécurité défensive et évaluations de robustesse.

**Sortie :** écosystème extensible, auditable et contrôlable.

## Nouvelles idées à garder dans le portefeuille de recherche

- **NEXUS Digital Twin** : jumeaux numériques d'usines, bâtiments, réseaux et produits.
- **NEXUS Earth** : tableaux de bord eau, agriculture, climat et environnement.
- **NEXUS Local Languages** : corpus validés et outils vocaux pour langues locales, sans inventer de qualité linguistique non mesurée.
- **NEXUS Accessibility** : assistant de lecture, sous-titrage, simplification et interfaces inclusives.
- **NEXUS Lab Simulator** : laboratoires virtuels pour apprendre et tester des expériences sans danger.
- **NEXUS Maker** : préparation de fichiers pour impression 3D, découpe et fabrication, avec contrôle des dimensions.
- **NEXUS Knowledge Graph** : relier les connaissances et sources avec dates, citations et niveaux de confiance.
- **NEXUS Team OS** : gestion de projets, tâches, fichiers, rôles et collaboration.
- **NEXUS Quality Gate** : aucun livrable ne passe en « prêt » sans critères et tests définis.
- **NEXUS Personal Cloud** : espace privé de projets et sauvegardes, soumis aux quotas et au budget.

## Séquencement et garde-fous

Les phases 9A à 9E ne doivent pas être développées en bloc. Choisir un seul module après les fondations, réaliser un prototype, mesurer la qualité et les ressources, puis décider de la suite. Les fonctions médicales, juridiques, financières, de sécurité et de contrôle physique requièrent des contrôles spécialisés et une supervision humaine. Les domaines spatiaux, véhicules, drones et énergie commencent par la simulation et l'analyse, jamais par le pilotage réel autonome.

