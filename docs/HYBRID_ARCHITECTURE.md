# MS NEXUS AI — Architecture hybride autonome (phase 1)

## Principe

MS NEXUS AI utilise en priorité des modèles open source exécutés sur des machines contrôlées par le projet. Aucun fournisseur commercial d'IA n'est appelé par défaut. Le cloud désigne ici des nœuds d'inférence auto-hébergés, pas une API GPT/Gemini/Claude.

## Couches

1. **NEXUS Gateway** : API FastAPI, authentification, routage et contrats d'API.
2. **NEXUS Runtime** : registre des modèles et adaptateurs par modalité.
3. **Edge Runtime** : Ollama sur un ordinateur ou serveur local.
4. **Cloud Runtime** : nœuds GPU auto-hébergés (par exemple vLLM pour le texte), configurables derrière le réseau privé.
5. **Media Workers** : nœuds séparés pour diffusion d'images, audio et vidéo. Ils ne sont annoncés comme configurés que si leur URL existe.
6. **MS CONNECT** : connecteurs signés vers les applications autorisées, dont MS DIGITAL NETWORK.
7. **Data & Training** : stockage des conversations autorisées, jeux de données versionnés, évaluation et fine-tuning. Les données privées ne deviennent jamais automatiquement des données d'entraînement.

## Chemin d'une requête texte

Client → API Key MS NEXUS → Runtime local Ollama → réponse. La future étape ajoutera un routage explicite vers un nœud cloud GPU auto-hébergé si le nœud edge est indisponible ou si la charge le justifie.

## Déploiement progressif

- API seule : démarre sans fournisseur commercial, mais le chat renvoie 503 tant qu'aucun runtime local n'est relié.
- Profil `local-ai` : lance Ollama dans Docker ; télécharger ensuite un modèle avec `docker compose exec ollama ollama pull llama3.2:3b`.
- Pour le cloud/edge : définir `LOCAL_TEXT_BASE_URL` vers le nœud Ollama accessible depuis l'API. Utiliser un VPN ou réseau privé, TLS et une authentification forte entre machines.
- Image, audio et vidéo : déployer des workers auto-hébergés compatibles avec les routes documentées. Ces modules restent non configurés tant que leurs moteurs ne sont pas installés.

## MS CONNECT

Le premier adaptateur envoie des événements à `/api/integrations/ms-nexus/events` sur MS DIGITAL NETWORK avec HMAC SHA-256 et horodatage. Le service destinataire doit implémenter et vérifier ce contrat avant que la connexion puisse être considérée comme opérationnelle. Configurer les secrets uniquement dans les variables d'environnement du serveur.

## Limites honnêtes

Cette phase fournit la structure et le premier adaptateur de texte local, pas un modèle entraîné par MS NEXUS, ni un moteur local image/audio/vidéo complet. Les performances et le volume dépendent du matériel, du stockage, de la mémoire GPU et de la concurrence. Aucune génération infinie ou gratuite n'est promise.
