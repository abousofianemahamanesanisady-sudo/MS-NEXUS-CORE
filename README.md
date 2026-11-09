# MS NEXUS CORE — v2.1

Backend FastAPI de MS NEXUS AI : chat, images, synthèse vocale et génération vidéo via fournisseur externe.

## Vidéo : file sans quota applicatif
L'API n'impose pas de limite cumulative au nombre de demandes vidéo. Chaque demande est enregistrée dans SQLite avec l'état `queued`, puis le service `video-worker` la transmet au fournisseur. Les demandes peuvent donc s'accumuler dans la file et être traitées au rythme des ressources disponibles.

**Cela ne signifie pas une génération gratuite ou matériellement infinie.** Le fournisseur vidéo peut imposer des quotas, des frais, des limites de durée ou des limites de concurrence. Le débit dépend aussi du compte fournisseur et de l'infrastructure. Le worker fourni soumet les tâches et conserve l'identifiant retourné ; le suivi du rendu final côté fournisseur peut nécessiter un adaptateur de polling propre à ce fournisseur.

## Installation
1. Copier `.env.example` vers `.env`.
2. Ajouter les clés et URL réelles du fournisseur IA et vidéo.
3. Lancer `docker compose up --build -d`.
4. Ouvrir `http://localhost:8000/docs`.

API : `http://localhost:8000` — Santé : `/health`.

Les routes `/v1` exigent `Authorization: Bearer VOTRE_CLE`. Vidéo : configurer `VIDEO_API_URL` et `VIDEO_API_KEY`. Le fournisseur doit accepter un POST JSON avec `prompt`, `model` et `duration`, et répondre avec `id` ou `job_id`.

## Vérifier une vidéo
Envoyer un POST à `/v1/videos/generations`, puis consulter `GET /v1/jobs/{id}` avec la même clé API. États : `queued`, `processing`, `submitted` ou `failed`.

## Sécurité et limites
Ce backend orchestre des modèles externes ; il ne contient pas de modèle vidéo entraîné. Changez les clés d'exemple, activez HTTPS, gardez `.env` secret et utilisez un stockage persistant. Les intégrations nécessitent des clés fournisseur valides et des tests réels.
