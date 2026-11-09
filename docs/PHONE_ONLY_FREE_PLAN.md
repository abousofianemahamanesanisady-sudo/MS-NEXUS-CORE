# MS NEXUS AI — démarrage avec Android uniquement et 0 FCFA

## Décision

Le téléphone Android sert de poste de pilotage et de test. Il ne doit pas être considéré comme un serveur GPU permanent. À 0 FCFA, nous pouvons préparer et publier gratuitement une interface et une petite passerelle, mais nous ne pouvons pas promettre un moteur IA auto-hébergé 24 h/24, une génération vidéo illimitée ou un entraînement de modèle propriétaire.

## Ce qui est réaliste sans payer

1. **Code et versions** : conserver le code dans le dépôt GitHub.
2. **Interface web mobile** : publier une interface statique sur Cloudflare Pages (offre gratuite soumise aux limites du fournisseur).
3. **Petite passerelle** : utiliser Cloudflare Workers pour des routes légères, après adaptation du backend FastAPI actuel. Le plan gratuit indique notamment 100 000 requêtes par jour et 10 ms de temps CPU par invocation; ce n'est pas un hébergement Docker/Python permanent.
4. **Données** : envisager Cloudflare D1 ou un stockage objet gratuit pour un prototype, en vérifiant les quotas et la sauvegarde avant d'y placer des données importantes.
5. **Prototype IA facultatif** : Workers AI annonce une allocation gratuite de 10 000 Neurons par jour. C'est de l'inférence hébergée par Cloudflare, pas un modèle entraîné ou hébergé par MS NEXUS. Les requêtes s'arrêtent lorsque le quota gratuit est épuisé; certains modèles exigent un plan payant.

## Limite importante concernant l'objectif d'autonomie

L'architecture actuelle du dépôt prévoit Ollama et un nœud cloud privé vLLM/llama.cpp. Elle ne peut pas fonctionner telle quelle sur Cloudflare Workers : le service Docker Ollama, le worker vidéo persistant et l'API FastAPI nécessitent un environnement serveur adapté.

Deux voies sont donc possibles :

- **Prototype sans frais** : interface gratuite + petite passerelle adaptée à Workers + éventuellement un moteur d'inférence hébergé avec quota. Cela permet de tester le produit, mais ce n'est pas encore une IA entièrement auto-hébergée par MS NEXUS.
- **Autonomie stricte** : garder les modèles open source sur une machine contrôlée par MS NEXUS. Il faudra un ordinateur/serveur accessible ou un budget d'hébergement; un téléphone seul ne fournit pas les ressources nécessaires pour un service permanent de génération texte, image, audio et vidéo.

## Étapes proposées depuis le téléphone

1. Ouvrir le dépôt GitHub dans le navigateur Android.
2. Créer ou utiliser un compte Cloudflare gratuit.
3. Publier d'abord une interface statique de démonstration, sans secret dans le code client.
4. Adapter séparément une passerelle Workers; ne pas essayer de lancer le Docker Compose complet dans Workers.
5. Ajouter les données et les capacités IA une par une, avec suivi des quotas.
6. Ne jamais mettre une clé secrète, un mot de passe ou un jeton privé dans GitHub, dans le JavaScript public ou dans une capture d'écran.

## Liens officiels à consulter

- Cloudflare Workers : https://developers.cloudflare.com/workers/platform/limits/
- Cloudflare Workers AI et quotas : https://developers.cloudflare.com/workers-ai/platform/pricing/
- Cloudflare Pages : https://developers.cloudflare.com/pages/
- GitHub : https://github.com/abousofianemahamanesanisady-sudo/MS-NEXUS-CORE

## Ce qui n'est pas encore réalisé

Ce document est un plan d'architecture. Il ne signifie pas qu'un compte Cloudflare a été connecté, qu'un site a été déployé, que Workers AI est activé ou que le backend a été porté vers Workers. Ces étapes devront être effectuées et testées séparément.

## Première ressource Cloudflare créée

Le 9 novembre 2026, le Worker `ms-nexus-ai` a été créé dans le compte Cloudflare et déployé sur le sous-domaine workers.dev :

- URL : https://ms-nexus-ai.msdigitalnetwork.workers.dev
- Contrôle de santé : https://ms-nexus-ai.msdigitalnetwork.workers.dev/health
- Runtime : Cloudflare Workers
- Binding Workers AI : `AI`
- Modèle prévu pour le chat : `@cf/zai-org/glm-4.7-flash`
- Secret d'API : `NEXUS_API_KEY`, stocké comme secret Cloudflare (sa valeur n'est pas affichée dans le dépôt ni dans cette documentation).
- Routes prévues : `GET /health`, `GET /v1/models`, `POST /v1/chat/completions`.

Le déploiement et l'activation du sous-domaine ont été confirmés par l'API Cloudflare. La lecture externe de `/health) n'a pas pu être confirmée dans cette session : ouvrir l'URL depuis un navigateur pour effectuer le test HTTP réel.

### Clé d'accès à l'API

Le secret initial a été généré et enregistré côté Cloudflare. Pour utiliser l'API depuis une autre application, remplace-le par une clé que tu génères et conserves toi-même dans Cloudflare Dashboard > Workers & Pages > ms-nexus-ai > Settings > Variables and Secrets, puis utilise cette même clé comme en-tête `Authorization: Bearer ...` dans ton application. Ne l'envoie jamais dans le chat et ne la commite pas sur GitHub.

### Limites

Le Worker est un premier point d'entrée, pas le backend FastAPI complet du dépôt et pas un modèle de fondation entraîné par MS NEXUS. Workers AI est un service d'inférence géré par Cloudflare. Vérifier les quotas et modèles accessibles au compte avant un usage régulier. Les routes de chat sont protégées par la clé secrète.
