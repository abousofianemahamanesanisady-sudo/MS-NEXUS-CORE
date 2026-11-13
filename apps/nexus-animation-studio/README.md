# NEXUS ANIMATION STUDIO — V0.1

Module de préproduction indépendant ajouté à MS-NEXUS-CORE.

## Déploiement
- Worker Cloudflare : `ms-nexus-animation`
- URL attendue : `https://ms-nexus-animation.msdigitalnetwork.workers.dev`
- Health check : `/health`
- Génération du découpage : `POST /api/generate`

## Fonctionnalités V0.1
- Interface responsive mobile-first en français.
- Brief de projet avec durée de 1 à 60 minutes.
- Découpage en séquences de 1 ou 2 minutes et plans de 5 à 15 secondes.
- Appel optionnel à Workers AI (modèle Llama 3.2 3B) avec fallback déterministe.
- Projets conservés dans le stockage local du navigateur.
- Export JSON, suppression et préparation d'une continuation.
- Contrôle structurel et checklist de continuité.

## Limites honnêtes
Cette version est un atelier de préproduction. Elle ne génère pas encore d'images, de modèles 3D, d'animation, de voix ni de MP4. Elle ne garantit pas zéro erreur narrative ou visuelle. Les projets restent sur l'appareil jusqu'à export; aucune base de données cloud n'est configurée. Workers AI est soumis aux quotas et conditions du compte Cloudflare; 0 F CFA ne signifie pas inférence illimitée.

## Développement suivant
1. Stockage cloud D1/R2 et authentification.
2. Références visuelles persistantes des personnages.
3. Storyboard image et validation des plans.
4. Adaptateurs vidéo/audio configurables.
5. Orchestration Blender distante (GPU externe requis).
6. Montage, sous-titres et export MP4.
