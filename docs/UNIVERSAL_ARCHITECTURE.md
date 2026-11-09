# MS NEXUS AI — Architecture universelle cible

**Statut :** architecture cible et proposition de réalisation. Ce document ne signifie pas que les modules décrits sont déjà implémentés ou entraînés.

## 1. Vision

MS NEXUS AI poursuit deux objectifs complémentaires :

1. **Intelligence universelle** : comprendre les demandes, raisonner, planifier, utiliser des outils autorisés, apprendre à partir de jeux de données validés et collaborer avec des agents spécialisés.
2. **Studio de création technologique** : transformer une demande en livrables vérifiables — applications mobiles, plateformes web, jeux, animations, médias, prototypes 3D, logiciels et documentation technique.

Une interface et un compte communs peuvent présenter ces capacités. En revanche, les tâches sont exécutées par des moteurs spécialisés et des services adaptés à chaque charge.

## 2. Principes non négociables

- **Architecture modulaire** : chaque capacité possède un contrat, un adaptateur, des tests et un état de disponibilité explicite.
- **Routage honnête** : ne jamais annoncer une capacité active si aucun moteur compatible n'est configuré et testé.
- **Pas de fournisseur caché** : chaque moteur indique son origine, sa licence, son mode d'hébergement, ses coûts éventuels et ses limites.
- **Données sous contrôle** : les conversations et fichiers privés ne deviennent pas automatiquement des données d'entraînement.
- **Validation humaine** : demander confirmation avant publication, dépense, suppression, accès externe ou action irréversible.
- **Sécurité par défaut** : secrets côté serveur, permissions minimales, journalisation sans données sensibles, isolation des outils et contrôle des fichiers.
- **Mesure avant promesse** : évaluer qualité, latence, coût, mémoire et fiabilité avant d'ouvrir une capacité aux utilisateurs.

## 3. Architecture logique

```text
Applications Web / Mobile / API
              |
       NEXUS Gateway
 Auth • quotas • sessions • API
              |
       NEXUS Orchestrator
 Intent • plan • permissions • tâches
       /       |        \
  Model      Tool      Project
 Router      Runtime   Workspace
    |          |          |
 Text/Code  Browser*   Files/Git
 Vision     Sandbox*   Builds/Tests
 Audio      Connectors Deploy*
 Video/3D
    |
 Model & Capability Registry
    |
 Edge Runtime | Private GPU Runtime | Managed adapters
              |
 Data Platform
 datasets • memory • evaluations • artifacts
              |
 Observability & Governance
 logs • metrics • audit • safety
```

`*` Les outils réseau, navigateur, sandbox et déploiement ne sont activés qu'avec des permissions explicites et des environnements isolés.

## 4. Composants

### 4.1 NEXUS Gateway
- Conserver FastAPI comme API backend de référence dans la première étape.
- Authentifier les utilisateurs et services, appliquer les quotas et valider les entrées.
- Versionner les contrats sous `/v1`.
- Ne jamais exposer les clés d'administration ou clés de fournisseurs aux clients.

### 4.2 NEXUS Orchestrator — priorité principale
- Classifier la demande : conversation, code, recherche, analyse, média ou création de projet.
- Décomposer les missions complexes en étapes avec dépendances et critères d'acceptation.
- Choisir les modèles et outils selon capacité, coût, latence, licence et disponibilité.
- Conserver l'état des tâches longues et reprendre après une interruption.
- Demander une approbation avant toute action sensible.
- Renvoyer un résultat structuré : réponse, fichiers, tests, erreurs et prochaines étapes.

### 4.3 Model & Capability Registry
Chaque moteur doit déclarer au minimum :
- identifiant et version ;
- modalités et tâches prises en charge ;
- fournisseur ou origine du modèle ;
- licence et conditions d'utilisation ;
- endpoint/runtime et méthode d'authentification ;
- ressources nécessaires ;
- limites, coûts et statut de santé ;
- tests d'évaluation associés.

États normalisés : `planned`, `configured`, `available`, `degraded`, `disabled`, `failed`. Une configuration seule ne prouve pas qu'une génération fonctionne.

### 4.4 Runtime et adaptateurs
- **Texte/raisonnement** : Ollama edge aujourd'hui ; runtime privé compatible vLLM/llama.cpp à ajouter selon le matériel.
- **Code** : modèle de code spécialisé et exécution dans un bac à sable sans secrets ni accès réseau par défaut.
- **Vision/image** : adaptateurs distincts pour compréhension, génération et édition.
- **Audio** : adaptateurs distincts pour transcription, synthèse et éventuellement parole temps réel.
- **Vidéo** : jobs asynchrones, stockage d'artefacts, suivi de progression et récupération du résultat.
- **3D/jeux/animation** : intégration de moteurs et formats existants, génération d'assets et de scripts, compilation et tests dans des workers dédiés.

Les capacités image, audio, vidéo et 3D ne doivent pas être simulées par le modèle texte. Elles exigent des moteurs adaptés.

### 4.5 Project Workspace / Creator Engine
Chaque projet généré possède :
- un identifiant, un propriétaire et des permissions ;
- un brief et des exigences versionnés ;
- un plan et une liste de tâches ;
- des fichiers et artefacts ;
- des builds, tests, journaux et rapports ;
- un historique des modifications ;
- des actions de publication soumises à approbation.

Les générateurs APP, WEB, GAME, ANIMATION, CONSOLE et INVENTOR réutilisent ce socle commun. Ils ne deviennent pas des systèmes indépendants.

### 4.6 Data, Memory & Training
Séparer strictement :
1. mémoire de projet et préférences autorisées ;
2. fichiers privés et données opérationnelles ;
3. jeux de données d'entraînement explicitement sélectionnés ;
4. jeux d'évaluation non utilisés pour l'entraînement.

Prévoir provenance, consentement, nettoyage, déduplication, versionnement, licences, suppression et traçabilité. Commencer par évaluer un modèle de base avant de lancer un fine-tuning QLoRA/LoRA sur un petit jeu de données validé.

### 4.7 Agents spécialisés
Les agents sont des rôles orchestrés, pas nécessairement des modèles distincts :
- Planner : planifie et vérifie les dépendances.
- Researcher : collecte des sources et les cite.
- Coder : modifie le code dans un workspace isolé.
- Reviewer : relit et détecte les risques.
- Tester : lance les tests et rapporte les résultats.
- Designer : prépare les spécifications visuelles.
- Media Producer : orchestre les moteurs image/audio/vidéo.
- Release Agent : prépare une publication, mais exige approbation.

Chaque agent reçoit des permissions limitées et un budget de temps/tokens/outils.

## 5. Sécurité et gouvernance

- Authentification forte et autorisation par rôle/projet.
- Secrets stockés uniquement dans le gestionnaire de secrets de l'hébergeur.
- Bac à sable éphémère pour code, builds et outils.
- Pas d'accès réseau sortant par défaut depuis le bac à sable.
- Limites CPU, RAM, durée, taille de fichiers et concurrence.
- Analyse antivirus/type MIME et limites d'upload.
- Protection contre prompt injection dans les fichiers et pages externes.
- Journal d'audit des actions, approbations et déploiements.
- Sauvegardes et procédure de restauration testées.
- Tests de sécurité avant ouverture publique.

## 6. Déploiement progressif

- **API légère / edge** : authentification, routage simple, statut et tâches courtes.
- **Backend persistant** : FastAPI, base de données, orchestration et workers.
- **Stockage objet** : datasets, fichiers de projet, médias et artefacts.
- **Queues** : génération vidéo, builds, entraînement et autres tâches longues.
- **Nœuds GPU** : modèles lourds texte, vision, audio, vidéo et 3D.
- **Cloudflare** : peut fournir la passerelle edge, le stockage et certains services gérés ; Workers AI est une inférence gérée, pas l'entraînement d'un modèle propriétaire.

Le Worker Cloudflare de bootstrap existant reste un point d'entrée séparé. Il ne remplace pas automatiquement le backend FastAPI, les workers persistants ou les nœuds GPU.

## 7. Contrat de disponibilité

Une capacité n'est considérée opérationnelle que si :
1. un adaptateur est configuré ;
2. le moteur répond à un contrôle de santé ;
3. un test fonctionnel réel réussit ;
4. les erreurs et limites sont observables ;
5. la documentation précise les ressources et coûts.

Les réponses API doivent distinguer `not_configured`, `unavailable`, `overloaded` et `failed`, plutôt que renvoyer un succès fictif.

## 8. Décisions d'architecture à préserver

- Une seule expérience utilisateur, plusieurs moteurs spécialisés.
- Un orchestrateur central, des agents à permissions limitées.
- Un workspace commun pour tous les types de créations.
- Le texte et le routage constituent la première fondation.
- L'image, l'audio, la vidéo, la 3D et les consoles sont des étapes distinctes.
- Les consoles physiques, robots et inventions matérielles nécessitent conception humaine, composants, fabrication et essais réels : le logiciel seul ne les fabrique pas.

## 9. Définition du succès

MS NEXUS AI progresse lorsque l'utilisateur peut décrire une mission, obtenir un plan, suivre son exécution, examiner des artefacts, voir les tests réellement exécutés, corriger le résultat et approuver sa livraison — sans que le système prétende avoir réalisé ce qui n'a pas été vérifié.


## 10. Catalogue étendu des domaines de création

Les domaines ci-dessous sont des **modules cibles** à intégrer au registre des capacités. Ils ne sont actifs que lorsqu'un moteur, un adaptateur, des permissions et des tests existent.

### 10.1 Studios numériques
- **APP & WEB Studio** : applications Android/iOS, applications desktop, sites, plateformes SaaS, commerce électronique, réseaux sociaux, API et outils métiers.
- **GAME Studio** : jeux 2D/3D, simulations, mondes ouverts, jeux multijoueurs, outils de niveaux, personnages, animation et tests automatisés.
- **4D Experience Lab** : expériences immersives combinant rendu 3D temps réel, audio spatial, vibration, sièges ou accessoires à retour haptique, mouvement et autres effets sensoriels. Le matériel compatible est indispensable ; « 4D » ne désigne pas une quatrième dimension physique créée par le logiciel.
- **CINEMA & ANIMATION Studio** : scénarios, storyboards, bandes dessinées, anime, films, séries, montage, doublage, sous-titres et effets visuels.
- **IMAGE & DESIGN Studio** : illustration, retouche, identité visuelle, maquettes, affiches, interfaces et assets cohérents.
- **AUDIO & MUSIC Studio** : voix, transcription, synthèse, bruitages, composition originale, mixage et spatialisation, avec respect des droits.
- **3D & SPATIAL Studio** : objets, scènes, architecture, visualisation, impression 3D et formats d'échange.
- **DOCUMENT & KNOWLEDGE Studio** : PDF, livres numériques, présentations, rapports, traduction et gestion documentaire.

### 10.2 Ingénierie et monde physique
- **OS & SOFTWARE Lab** : systèmes d'exploitation, pilotes, logiciels, outils de développement et tests de compatibilité.
- **CONSOLE Lab** : conception de consoles, architecture matérielle, contrôleurs, systèmes embarqués, prototypes et bancs de test.
- **ROBOTICS Lab** : simulation robotique, perception, planification de mouvement, contrôle et intégration de capteurs/actionneurs.
- **INVENTOR Lab** : conception assistée, électronique, circuits, pièces mécaniques, nomenclatures, schémas et dossiers de fabrication.
- **DRONE & MOBILITY Lab** : simulation, conception de drones, véhicules et systèmes de mobilité ; essais physiques et conformité réglementaire obligatoires.
- **SMART WORLD Lab** : jumeaux numériques, bâtiments, villes, infrastructures, réseaux et simulations urbaines.
- **ENERGY Lab** : modélisation de systèmes solaires, stockage, efficacité énergétique et réseaux électriques.
- **SPACE & ASTRONOMY Lab** : visualisation astronomique, analyse de données publiques, simulation orbitale éducative et outils scientifiques ; aucune commande réelle de véhicule spatial sans infrastructure autorisée.

### 10.3 Sciences, société et services
- **SCIENCE & MATH Lab** : calcul symbolique, simulations, visualisation, analyse reproductible et aide à la recherche.
- **AGRI Lab** : planification agricole, diagnostic assisté à partir d'images, irrigation, météo et suivi des cultures ; les recommandations doivent être validées localement.
- **HEALTH & WELLBEING Assistant** : éducation générale, organisation de dossiers et préparation de questions médicales ; ne remplace pas un professionnel et ne pose pas de diagnostic autonome.
- **EDUCATION Studio** : parcours d'apprentissage, exercices, examens blancs, explications multilingues et suivi des progrès.
- **BUSINESS & FINANCE Studio** : gestion, comptabilité assistée, tableaux de bord, études de marché et prévisions avec hypothèses explicites ; aucune transaction sans approbation.
- **LAW & CIVIC Information** : explication générale de documents et informations publiques, avec indication du pays, de la date et de la nécessité d'un avis professionnel.
- **LANGUAGE & ACCESSIBILITY** : traduction, transcription, sous-titrage, lecture à voix haute, simplification, interfaces accessibles et langues locales.
- **CLIMATE & ENVIRONMENT Lab** : analyse de données climatiques, eau, biodiversité, déchets et scénarios environnementaux.
- **TRANSPORT & LOGISTICS Lab** : planification d'itinéraires, stocks, flottes et simulations logistiques ; aucune commande de véhicule réel sans contrôles.
- **CYBER DEFENSE Lab** : audit autorisé, analyse de dépendances, détection de vulnérabilités, durcissement et réponse défensive ; pas d'opérations offensives non autorisées.

### 10.4 Intelligence et collaboration
- **NEXUS MEMORY** : mémoire contrôlée par projet, provenance, rétention configurable et suppression vérifiable.
- **NEXUS RESEARCH** : recherche sourcée, comparaison des preuves, dates, incertitudes et bibliographies.
- **NEXUS MULTI-AGENT** : agents de planification, recherche, création, revue, tests et livraison, coordonnés par un orchestrateur.
- **NEXUS DIGITAL TWIN** : représentation simulée d'un produit ou processus, calibrée avec des données fiables et des limites documentées.
- **NEXUS PERSONAL ASSISTANT** : tâches, calendrier, rappels et workflows avec consentement explicite.
- **NEXUS PLUGIN MARKET** : extensions signées, permissions visibles, provenance, versionnement et révocation.
- **NEXUS API & SDK** : interfaces développeur, documentation, exemples et environnement de test.
- **NEXUS LOCAL MODE** : fonctions hors ligne ou locales quand le modèle et l'appareil le permettent.

## 11. Capacités transversales supplémentaires

1. **Project-to-Product** : convertir une idée en cahier des charges, prototype, tests, documentation et paquet livrable.
2. **Self-Testing** : chaque artefact généré reçoit des tests pertinents et un rapport ; les tests non exécutés sont signalés.
3. **Visual Debugger** : analyser captures, journaux, traces et erreurs pour proposer une correction.
4. **Version & Rollback Manager** : versions de projets, comparaisons, sauvegardes et retour arrière.
5. **Cost & Resource Planner** : estimer CPU/GPU, mémoire, stockage, temps et coûts avant les tâches lourdes.
6. **Offline Knowledge Packs** : bases de connaissances téléchargeables avec source, date et version.
7. **Multilingual Niger-first** : expérience française et préparation progressive de langues locales, avec validation par locuteurs compétents.
8. **Collaboration & Classroom** : espaces d'équipe, partage contrôlé, rôles, commentaires et apprentissage collectif.
9. **Accessibility-by-design** : navigation clavier, contraste, lecteurs d'écran, sous-titres et commandes vocales.
10. **Provenance & Trust Center** : indiquer quels modèles, données, outils et versions ont produit chaque résultat.
11. **Simulation Sandbox** : tester logiciels, robots, véhicules et infrastructures dans des environnements virtuels avant tout essai réel.
12. **Human Approval Center** : boîte de validation des publications, dépenses, transactions, déploiements et opérations physiques.

## 12. Conditions spéciales pour les domaines à risque

Les fonctions santé, finance, droit, cybersécurité, robotique, drones, mobilité, énergie et systèmes physiques doivent avoir des politiques spécifiques, des tests dédiés, des limites d'usage, des avertissements pertinents et une validation humaine qualifiée. Une simulation réussie ne prouve pas la sécurité d'un système réel.

