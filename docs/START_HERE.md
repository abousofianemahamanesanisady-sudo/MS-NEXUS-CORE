# Bien démarrer MS NEXUS AI sans choisir un serveur coûteux

## Notre recommandation

Ne loue pas encore de serveur GPU. Commence par un test de modèle texte open source avec Ollama. Ce test sert à vérifier le fonctionnement de NEXUS et à mesurer les ressources réellement nécessaires. Ensuite seulement, décide si un serveur GPU auto-hébergé est utile.

## Quel matériel choisir ?

- **Ordinateur déjà disponible** : meilleur point de départ si tu disposes d'un PC ou serveur avec environ 8 Go de RAM ou plus pour essayer un petit modèle quantifié. 16 Go ou davantage offrent généralement plus de marge. Les performances dépendent aussi du processeur, du GPU, de la mémoire vidéo et de la taille du modèle.
- **Téléphone Android uniquement** : utilise-le pour accéder à l'interface et tester l'API distante. Il n'est pas recommandé comme serveur permanent pour le modèle, les images et les vidéos.
- **Pas d'ordinateur disponible** : ne déploie pas encore de machine payante. On peut d'abord préparer le déploiement cloud, comparer les coûts et choisir une machine seulement après validation du budget.
- **Cloud GPU auto-hébergé** : à ajouter pour les modèles plus grands, plusieurs utilisateurs simultanés et les tâches lourdes. Le serveur doit être administré par le projet; ce n'est pas une API d'assistant commercial.

Ces valeurs sont des repères de départ, pas une garantie de vitesse ou de compatibilité. Les générateurs d'images et surtout de vidéos ont des besoins matériels bien plus élevés que le chat texte.

## Premier test sur un ordinateur avec Docker

1. Installer Docker Desktop (Windows/Mac) ou Docker Engine + Docker Compose (Linux).
2. Cloner le dépôt et ouvrir un terminal dans le dossier `MS-NEXUS-CORE`.
3. Copier `.env.example` vers `.env`.
4. Remplacer `MSNEXUS_API_KEYS` et `ADMIN_API_KEY` par deux valeurs secrètes longues. Ne jamais envoyer ces secrets dans une conversation ni les committer sur GitHub.
5. Lancer : `docker compose --profile local-ai up --build -d`.
6. Télécharger le modèle de test : `docker compose exec ollama ollama pull llama3.2:3b`.
7. Consulter les journaux : `docker compose logs -f api ollama`.
8. Ouvrir `http://localhost:8000/docs` pour voir les routes disponibles.

Le premier téléchargement du modèle nécessite une connexion Internet. Ensuite, le modèle est exécuté par Ollama sur la machine qui héberge le conteneur.

## Vérifier l'état des moteurs

- `GET /health` vérifie que l'API répond.
- `GET /admin/runtime` vérifie les nœuds configurés et leur accessibilité. Envoyer l'en-tête `X-Admin-Key: VOTRE_ADMIN_API_KEY`.
- `GET /v1/models` nécessite `Authorization: Bearer VOTRE_MSNEXUS_API_KEY`.
- `POST /v1/chat/completions` permet le premier test de conversation avec la même clé Bearer.

Si `edge_reachable` est faux, vérifier que le service `ollama` tourne et que `LOCAL_TEXT_BASE_URL` vaut `http://ollama:11434` dans le réseau Docker. Si le nœud répond mais que `edge_model_available` est faux, télécharger le modèle indiqué dans `LOCAL_TEXT_MODEL`.

## Après le test

Noter le temps de réponse, la mémoire utilisée, le nombre d'utilisateurs simultanés et les limites rencontrées. Si le PC est trop lent ou indisponible, déployer un nœud cloud GPU privé compatible puis renseigner `CLOUD_TEXT_BASE_URL`, `CLOUD_TEXT_MODEL` et, si nécessaire, `CLOUD_TEXT_API_KEY` dans les variables secrètes de l'hébergeur.

## Ce que cette étape ne fait pas encore

Elle ne crée pas un modèle de fondation entraîné par MS NEXUS AI. Elle exécute un modèle open source existant dans une infrastructure contrôlée. Elle n'installe pas non plus les moteurs image, audio et vidéo. Une utilisation sans quota logiciel ne rend pas les calculs matériellement infinis : GPU, RAM, stockage, réseau, électricité et capacité du serveur restent limitants.
