# Déploiement du modèle indépendant MS NEXUS — portes de validation

## État actuel (9 novembre 2026)

- Le Worker de production `ms-nexus-ai` reste un gateway Cloudflare Workers AI utilisant `@cf/zai-org/glm-4.7-flash`.
- Le prototype entraîné depuis zéro est un petit Transformer PyTorch au niveau caractère, avec un checkpoint `.pt` conservé dans Deepnote.
- La génération du prototype est encore incohérente. Il n'est donc pas acceptable de l'utiliser pour répondre aux utilisateurs.
- Le fichier `.pt` n'est pas directement exécutable dans un Worker JavaScript. Il faut une conversion et un runtime compatibles, puis des tests de parité.
- Aucun changement n'a été appliqué au Worker de production dans cette étape.

## Étapes obligatoires avant une mise en service

1. **Données** — augmenter le corpus avec des textes dont les droits autorisent explicitement l'entraînement ; documenter provenance, licences, langue, déduplication et séparation entraînement/validation/test.
2. **Entraînement reproductible** — conserver le code, la configuration, les graines aléatoires, les versions des bibliothèques et le hash du checkpoint.
3. **Évaluation** — mesurer la perte sur validation et test, comparer à une baseline aléatoire, vérifier la génération sur des invites fixes et tester les sorties nuisibles ou inventées.
4. **Export** — choisir un format d'inférence réellement pris en charge par le runtime cible. Vérifier que l'export reproduit les logits et les sorties du modèle PyTorch sur des entrées de test.
5. **Staging isolé** — déployer sous un nom de Worker distinct, sans remplacer `ms-nexus-ai`, sans clé de production et sans trafic utilisateur.
6. **Tests réseau** — vérifier `/health`, authentification, limites de taille, latence, erreurs, observabilité et comportement en cas de surcharge.
7. **Validation humaine** — comparer les réponses sur un jeu de tests français et obtenir l'accord explicite du propriétaire avant toute bascule de trafic.

## Pourquoi le Worker de production n'est pas remplacé

Un checkpoint sauvegardé ne constitue pas à lui seul un service d'inférence. Le modèle actuel produit encore du texte incohérent et n'a pas de runtime JavaScript validé. Le déployer maintenant dégraderait le service. Le Worker existant est donc préservé.

## Coût et sécurité

- Ne pas activer de machine GPU payante, de service hébergé payant ou de ressources facturées sans accord explicite.
- Ne jamais placer de secrets dans le dépôt, les corpus, les journaux ou les sorties de notebook.
- Ne pas entraîner sur des conversations privées ou des données personnelles.
- Conserver le checkpoint et le manifeste avec leurs empreintes cryptographiques.
