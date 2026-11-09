# MS NEXUS — premier modèle entraîné depuis zéro

Ce dossier contient un **prototype pédagogique initialisé avec des poids aléatoires**. Il n'importe aucun poids GLM, GPT, Gemini ou autre modèle pré-entraîné et n'appelle aucune API d'IA externe.

## Ce que ce prototype est — et n'est pas

- Petit Transformer autorégressif de type décodeur, entraîné à prédire le caractère suivant.
- Tokenizer simple : vocabulaire de caractères construit depuis le corpus local.
- Poids initialisés aléatoirement.
- Apprentissage limité aux régularités présentes dans le corpus fourni.
- Ce n'est **pas encore** un assistant conversationnel performant, un grand modèle de langage ou une preuve d'intelligence générale.
- Aucun dataset externe n'est téléchargé et aucun texte n'est envoyé vers un service d'IA distant.

## Corpus fourni

Le fichier `corpus.example.txt` est un petit corpus original en français, créé pour valider le pipeline. Il est inclus à titre d'exemple uniquement et ne constitue pas un corpus généraliste. Pour un entraînement sérieux, ajouter des textes dont les droits autorisent explicitement l'usage.

Ne pas copier de conversations privées, de données personnelles, de livres protégés ou de contenus sans licence. Les derniers 10 % du fichier sont réservés à la validation.

## Installation et entraînement

Python 3.10+ et PyTorch sont nécessaires :

    python -m pip install torch

Depuis la racine du dépôt, copier le corpus exemple ou fournir un autre corpus autorisé :

    cp training/from_scratch/corpus.example.txt training/from_scratch/corpus.txt
    python training/from_scratch/train.py --steps 2000

Le checkpoint est écrit dans `artifacts/nexus-tiny.pt`. Ce fichier de poids n'est pas commité par défaut.

## Génération et évaluation

    python training/from_scratch/generate.py --prompt "MS NEXUS" --tokens 200
    python training/from_scratch/evaluate.py --data training/from_scratch/corpus.txt --checkpoint artifacts/nexus-tiny.pt

L'évaluateur calcule une perte moyenne sur des lots d'entraînement et de validation, la compare à une baseline uniforme, et produit le SHA-256 du checkpoint. Le prompt ne peut contenir que des caractères présents dans le corpus d'entraînement.

## Expérience vérifiée le 9 novembre 2026

Le notebook Deepnote distinct **MS NEXUS PRIME — Entraînement depuis zéro** a terminé 300 étapes avec 113 222 paramètres, sur CPU, avec 18 672 caractères et 70 caractères distincts. Perte finale d'entraînement : 2,4878 ; perte de validation : 2,5275. Un checkpoint a été sauvegardé dans l'environnement Deepnote.

La génération obtenue reste incohérente. Cette expérience valide le fonctionnement technique du pipeline, pas une capacité conversationnelle utile. Le rapport complet est dans [EXPERIMENT_2026-11-09.md](EXPERIMENT_2026-11-09.md).

**Important :** le notebook d'expérience et le script `train.py` du dépôt ont des configurations distinctes. Les métriques du rapport correspondent au notebook Deepnote, pas à une exécution de ce script CLI.

## Préparation Cloudflare

Les conditions et les étapes obligatoires avant d'utiliser le checkpoint sur Cloudflare sont décrites dans [INDEPENDENT_MODEL_CLOUDFLARE_DEPLOYMENT.md](../../docs/INDEPENDENT_MODEL_CLOUDFLARE_DEPLOYMENT.md). Le fichier PyTorch `.pt` n'est pas directement exécutable dans un Worker JavaScript. Le Worker de production reste séparé et ne charge pas ce prototype.

## Prochaines étapes scientifiques

1. Constituer un corpus français beaucoup plus grand, autorisé, documenté et dédupliqué.
2. Passer du tokenizer caractère à un tokenizer sous-mots documenté.
3. Ajouter des jeux de tests séparés : compréhension, grammaire, connaissances, raisonnement et code.
4. Augmenter progressivement la taille du modèle seulement si le matériel le permet.
5. Étudier l'entraînement distribué et les besoins GPU avant de viser un modèle conversationnel utile.
6. Publier les poids, le tokenizer, les données autorisées et les rapports avec versions et provenance vérifiables.

## Principe d'indépendance

Le prototype est entraîné à partir d'une initialisation aléatoire et reste indépendant des poids d'un fournisseur tiers. Un modèle utile à grande échelle demande beaucoup plus de données, de calcul, d'évaluations et de travail scientifique. Ne pas le présenter comme un assistant performant tant que des évaluations solides ne le démontrent pas.
