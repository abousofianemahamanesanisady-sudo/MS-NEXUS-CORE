# Rapport d'expérience — 9 novembre 2026

## Exécution vérifiée

Le notebook Deepnote **MS NEXUS PRIME — Entraînement depuis zéro** a terminé avec le statut `success`.

- Exécution : `ec2253dd-4989-469a-be2c-1a09566af63a`
- Corpus : 18 672 caractères, 70 caractères distincts
- Architecture : Transformer causal caractère-par-caractère
- Paramètres : 113 222
- Initialisation : poids aléatoires, sans poids pré-entraînés et sans API d'inférence externe
- Environnement : Python 3.13.18, PyTorch 2.12.0, CPU (CUDA indisponible)
- Étapes : 300
- Perte d'entraînement à la dernière étape : 2,4878
- Perte de validation mesurée : 2,5275
- Checkpoint sauvegardé dans l'environnement Deepnote : `nexus_tiny_checkpoint.pt`

## Échantillon de génération

La génération obtenue commence par :

> MS NEXUSen ilenens l cmitanse es s é an oven e meme us s pe es contintratutacér...

La sortie est incohérente. C'est une preuve que le pipeline d'entraînement et de génération s'exécute, pas que le modèle possède une capacité conversationnelle utile.

## Limites et prochaines étapes

1. Le corpus est un petit corpus expérimental rédigé pour tester le pipeline. Il ne constitue pas un corpus généraliste.
2. Le modèle est très petit et utilise une tokenisation par caractères.
3. Il faut construire un corpus français beaucoup plus grand, diversifié, documenté et légalement autorisé.
4. Il faut ajouter des évaluations indépendantes et comparer plusieurs configurations.
5. Le checkpoint est conservé dans le projet Deepnote ; il n'est pas encore exporté dans ce dépôt ni déployé sur Cloudflare.
6. Le Worker Cloudflare de production continue d'utiliser son moteur d'inférence existant. Il ne charge pas encore ce checkpoint.

Ne pas annoncer ce prototype comme un assistant performant ou comme un modèle de niveau ChatGPT.
