# MS NEXUS AI — Hybrid Autonomous Runtime 2.2

MS NEXUS AI évolue vers une plateforme autonome **edge + cloud auto-hébergé**. Par défaut, le chat utilise un modèle open source exécuté sur un nœud contrôlé par le projet. Un nœud cloud GPU auto-hébergé peut prendre le relais. Aucun endpoint GPT, Gemini, Claude ou autre API commerciale n'est appelé par défaut.

## Architecture

- **NEXUS Gateway** : API FastAPI, authentification et contrats d'API.
- **NEXUS Runtime** : registre des capacités et routage edge-first.
- **Edge** : Ollama sur machine locale ou serveur privé.
- **Cloud** : endpoint vLLM/llama.cpp auto-hébergé et privé, activable comme secours.
- **Media Workers** : moteurs auto-hébergés distincts pour image, audio et vidéo.
- **MS CONNECT** : premier adaptateur HMAC pour MS DIGITAL NETWORK.
- **Training/Data** : future couche de jeux de données, évaluation et fine-tuning contrôlés.

Voir [docs/HYBRID_ARCHITECTURE.md](docs/HYBRID_ARCHITECTURE.md).

## Choisir l'infrastructure sans dépenser tout de suite

Commencer par le guide [docs/START_HERE.md](docs/START_HERE.md). La recommandation est de tester d'abord un petit modèle open source sur un ordinateur/serveur disponible, puis de mesurer les besoins avant de louer un GPU cloud. Un téléphone Android seul n'est pas recommandé pour héberger le runtime complet.

## Premier Worker Cloudflare déployé

Le Worker de démarrage `ms-nexus-ai` est déployé sur [ms-nexus-ai.msdigitalnetwork.workers.dev](https://ms-nexus-ai.msdigitalnetwork.workers.dev). Son contrôle de santé est disponible sur `/health`. Le déploiement et l'activation du sous-domaine ont été confirmés par l'API Cloudflare; le test HTTP externe reste à effectuer. Voir le guide [PHONE_ONLY_FREE_PLAN.md](docs/PHONE_ONLY_FREE_PLAN.md) pour les limites et la configuration de la clé secrète.

## Démarrer depuis un téléphone avec 0 FCFA

Consulter le guide [docs/PHONE_ONLY_FREE_PLAN.md](docs/PHONE_ONLY_FREE_PLAN.md). Il distingue clairement un prototype gratuit (interface et passerelle légère) d'un runtime IA entièrement auto-hébergé, qui nécessite des ressources serveur. Le backend Docker/FastAPI actuel ne se déploie pas directement sur Cloudflare Workers.

## Démarrer le runtime texte local

1. Copier `.env.example` vers `.env` et remplacer les clés MS NEXUS d'exemple.
2. Démarrer l'API et le nœud edge : `docker compose --profile local-ai up --build -d`.
3. Télécharger un modèle open source : `docker compose exec ollama ollama pull llama3.2:3b`.
4. Vérifier `http://localhost:8000/health` et appeler `/v1/chat/completions` avec la clé MS NEXUS.
5. Vérifier l'état des moteurs avec `GET /admin/runtime` et l'en-tête `X-Admin-Key`.

Le modèle est exécuté par Ollama sur le matériel choisi. Pour un vrai cloud GPU auto-hébergé, déployer vLLM/llama.cpp sur une machine contrôlée par le projet, puis renseigner `CLOUD_TEXT_BASE_URL`, `CLOUD_TEXT_MODEL` et éventuellement `CLOUD_TEXT_API_KEY`. Le routage essaie d'abord Edge puis Cloud.

## Capacités multimédia

`/v1/images/generations` et `/v1/audio/speech` attendent des nœuds auto-hébergés compatibles avec les routes correspondantes. `/v1/videos/generations` conserve une file persistante; `VIDEO_API_URL` doit pointer vers le worker vidéo auto-hébergé, avec une clé facultative si le service est privé. Une capacité vide est annoncée comme non configurée et retourne HTTP 503 : aucune bascule silencieuse vers un fournisseur commercial.

L'absence de quota cumulatif applicatif ne signifie pas une capacité infinie : la limite réelle dépend du GPU/CPU, de la RAM, du stockage, de l'électricité et du nombre de workers.

## Connecteur MS DIGITAL NETWORK

Configurer `MS_DN_BASE_URL` et `MS_DN_WEBHOOK_SECRET` côté serveur. L'API `POST /v1/connectors/ms-digital-network/events` relaie les événements vers `/api/integrations/ms-nexus/events` avec une signature HMAC SHA-256 et un horodatage. Le backend MS DIGITAL NETWORK doit implémenter la vérification de signature et cette route avant que la connexion soit opérationnelle.

## Sécurité

- Ne jamais committer les fichiers `.env` ou les clés.
- Exposer les nœuds d'inférence uniquement via réseau privé/VPN et TLS.
- Les données utilisateur ne sont pas automatiquement utilisées pour l'entraînement.
- Les routes `/v1` exigent `Authorization: Bearer VOTRE_CLE`.

## État de cette phase

La fondation edge-first, le registre de modèles, le fallback vers un nœud cloud auto-hébergé et le premier connecteur signé sont ajoutés. Cela ne constitue pas encore un modèle propriétaire entraîné, ni des moteurs locaux image/audio/vidéo prêts à l'emploi. Les tests et le déploiement matériel restent à faire.

## Vision universelle et feuille de route

La vision cible associe une intelligence centrale à des studios spécialisés (applications, web, jeux, animation, médias, 3D et conception technologique). Lire [l'architecture universelle](docs/UNIVERSAL_ARCHITECTURE.md) et la [feuille de route intelligence d'abord](docs/ROADMAP_UNIVERSAL_AI.md). Ces documents décrivent une cible et des étapes à réaliser ; ils ne déclarent pas ces capacités déjà opérationnelles.
