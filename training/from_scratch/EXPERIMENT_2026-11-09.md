# Rapport d'expérience — 9 novembre 2026

## Entraînement du notebook indépendant

Le notebook Deepnote **MS NEXUS PRIME — Entraînement depuis zéro** a terminé avec le statut `success`.

- Exécution : `619c254e-aaed-46ed-803f-cfc0147d3797`
- Corpus : 18 672 caractères, 70 caractères distincts
- Architecture : Transformer causal caractère-par-caractère
- Paramètres : 113 222
- Initialisation : poids aléatoires, sans poids pré-entraînés et sans API d'inférence externe
- Environnement : Python 3.13.18, PyTorch 2.12.0, CPU (CUDA indisponible)
- Étapes : 300
- Perte à la dernière étape d'entraînement : 2,4201
- Perte de validation à la dernière étape : 2,5953
- Moyenne sur 64 lots : entraînement 2,488535 ; validation 2,624087
- Baseline uniforme : 4,248495
- Checkpoint : 498 583 octets
- SHA-256 : `faa8e4c4c7571d9e81118cb4aa6782d73f6f39ce104ce0729c3f00fc60024331`

Le manifeste de cette exécution est dans [experiment-manifest.json](experiment-manifest.json).

## Test indépendant des scripts du dépôt

Le script CLI `train.py` et le nouvel évaluateur `evaluate.py` ont également été exécutés dans Deepnote sur CPU, avec une configuration de test courte :

- Exécution : `1a9cfe9b-1938-4673-afa4-16b87361b5e8`
- 20 étapes, batch 8, contexte 64, largeur 64, 4 têtes, 2 couches
- Paramètres : 108 672
- Perte d'entraînement finale : 3,67297
- Perte de validation finale : 3,67929
- Évaluation sur 8 lots : entraînement 3,670894 ; validation 3,694797
- Baseline uniforme : 4,248495
- Checkpoint de test : 479 593 octets
- SHA-256 : `862571b204b6f74c521775b6c03f0957bb80ba33bacd0270e9ad8838eb32e214`
- Résultat : `SMOKE TEST CLI: SUCCESS`

Ce test valide l'exécution des scripts et la sauvegarde/relecture d'un checkpoint. Il ne mesure pas une compétence conversationnelle.

## Échantillon de génération

La génération du notebook commence par des fragments de mots et des phrases mal formées. La sortie reste incohérente. C'est une preuve que le pipeline d'entraînement et de génération s'exécute, pas que le modèle possède une capacité conversationnelle utile.

## Limites et prochaines étapes

1. Le corpus est un petit corpus expérimental rédigé pour tester le pipeline. Il ne constitue pas un corpus généraliste.
2. Le modèle est très petit et utilise une tokenisation par caractères.
3. Il faut construire un corpus français beaucoup plus grand, diversifié, documenté et légalement autorisé.
4. Il faut ajouter des évaluations indépendantes de compréhension, de connaissances, de raisonnement et de sécurité.
5. Le checkpoint est conservé dans le projet Deepnote ; seuls le manifeste et les rapports sont publiés dans GitHub. Les poids ne sont pas encore exportés dans un format d'inférence compatible.
6. Le Worker Cloudflare de production continue d'utiliser GLM-4.7-Flash via Workers AI. Il ne charge pas encore ce checkpoint.

Ne pas annoncer ce prototype comme un assistant performant ou comme un modèle de niveau ChatGPT.
