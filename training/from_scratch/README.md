# MS NEXUS — premier modèle entraîné depuis zéro

Ce dossier contient un **prototype pédagogique réellement initialisé avec des poids aléatoires**. Il n'importe aucun poids GLM, GPT, Gemini ou autre modèle pré-entraîné et n'appelle aucune API d'IA externe.

## Ce que ce prototype est — et n'est pas

- Petit Transformer autorégressif de type décodeur, entraîné à prédire le caractère suivant.
- Tokenizer volontairement simple : vocabulaire de caractères construit depuis le corpus local.
- Poids initialisés aléatoirement au démarrage.
- Apprentissage limité aux régularités présentes dans le corpus fourni.
- Ce n'est **pas encore** un assistant conversationnel performant, un grand modèle de langage ou une preuve d'intelligence générale.
- Aucun dataset n'est téléchargé et aucun texte n'est envoyé vers un service distant.

## Conditions de données

Créer un fichier corpus.txt avec des textes que MS DIGITAL NETWORK possède, a rédigés ou a le droit d'utiliser. Ne pas copier des conversations privées, des données personnelles, des livres protégés ou des contenus sans licence. Le prototype réserve les derniers 10 % du fichier à la validation.

Le corpus doit contenir au moins 1 000 caractères pour démarrer, mais un corpus aussi petit ne produira que des résultats très limités. La qualité et la diversité des données sont plus importantes que le simple nombre de caractères.

## Installation

Python 3.10+ et PyTorch sont nécessaires. Installer PyTorch selon les instructions officielles adaptées au système et au matériel, puis exécuter :

    python -m pip install torch

Sur Android, l'installation de PyTorch et l'entraînement peuvent être difficiles ou incompatibles selon l'appareil. Le téléphone peut servir à modifier les fichiers et piloter GitHub ; il n'est pas considéré comme un serveur d'entraînement fiable.

## Entraîner depuis zéro

Depuis la racine du dépôt, créer le corpus autorisé dans training/from_scratch/corpus.txt, puis lancer :

    python training/from_scratch/train.py --steps 2000

Le checkpoint est écrit dans artifacts/nexus-tiny.pt. Ce fichier de poids n'est pas commité par défaut. Il faut le sauvegarder de façon sécurisée.

## Générer un échantillon

    python training/from_scratch/generate.py --prompt "MS NEXUS" --tokens 200

Le prompt ne peut contenir que des caractères présents dans le corpus d'entraînement.

## Prochaines étapes scientifiques

1. Vérifier l'exécution et conserver les logs de perte train/validation.
2. Constituer un corpus français autorisé, documenté et dédupliqué.
3. Passer du tokenizer caractère à un tokenizer sous-mots documenté.
4. Ajouter des jeux de tests séparés : compréhension, grammaire, connaissances, raisonnement et code.
5. Augmenter progressivement la taille du modèle seulement si le matériel le permet.
6. Étudier l'entraînement distribué et les besoins GPU avant de viser un modèle conversationnel utile.
7. Publier les poids, le tokenizer, les données autorisées et les rapports avec versions et provenance vérifiables.

## Principe d'indépendance

Le prototype est entraîné à partir d'une initialisation aléatoire. Il est donc indépendant des poids d'un fournisseur tiers. En revanche, un modèle utile à grande échelle demande beaucoup plus de données, de calcul, d'évaluations et de travail scientifique. Aucun résultat d'entraînement n'est revendiqué tant que la commande n'a pas été exécutée et ses métriques vérifiées.
