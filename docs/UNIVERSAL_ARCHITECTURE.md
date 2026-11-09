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
