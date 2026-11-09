# MS NEXUS CORE — v2

Backend FastAPI modulaire pour MS NEXUS AI : chat, images, synthèse vocale et adaptateur vidéo configurable.

## Installation
1. Copier `.env.example` vers `.env`.
2. Renseigner les clés et URL des fournisseurs IA.
3. Exécuter `docker compose up --build`.
4. Ouvrir `http://localhost:8000/docs`.

API : `http://localhost:8000` — Santé : `/health`.

Les routes `/v1` exigent `Authorization: Bearer VOTRE_CLE`. La vidéo nécessite un fournisseur configuré dans `VIDEO_API_URL` et `VIDEO_API_KEY`.

**Limite importante :** ce backend orchestre des modèles externes ; il ne contient pas de modèle entraîné. Les intégrations doivent être testées avec de vraies clés et le fournisseur vidéo doit respecter le contrat documenté. Ne publiez jamais le fichier `.env`.