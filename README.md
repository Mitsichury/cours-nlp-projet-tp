# Projet YNOV pour le cours de NLP : TicTacToe

L'objectif du projet est de jouer au TicTacToe contre un bot par commande vocale. Un échange sera, par exemple :

  - Utilisateur : "I want to play in the middle cell."
  - Bot : "Alright, I just played top-left."
  - Utilisateur : "For this turn, I choose left."
  - Bot : "Well done, you won the game !"
  - Utilisateur : "Thank you, now please start a new game."
  - Bot : "Ok, I restarted the game."
  - ...

Pour cela, nous nous appuierons sur les services suivants :

  - [AWS Lex](https://aws.amazon.com/fr/lex/) : L'agent conversationnel d'AWS
  - [AWS Lambda](https://aws.amazon.com/fr/lambda/features/) : Le FaaS d'AWS, qui nous permettra d'introduire de la logique dans la discussion.
  - [EC2](https://aws.amazon.com/fr/ec2/) : Le IaaS d'AWS, qui nous servira à heberger la logique du jeu.

## Lex : L'agent conversationnel

Allez sur la page du service Lex et créez un **Bot Custom**. Vous aurez besoin :

  - d'un **intent** pour comprendre quand l'utilisateur formulera une demande pour jouer une case.
  - d'un **slot** sur l'intent pour savoir quelle case l'utilisateur a joué.

Les réponses seront gérées par une fonction Lambda qu'il vous faudra définir.

## Lambda : La logique de discussion

Cette fonction sera en charge de récupérer les élements de la phrase de l'utilisateur, de les traiter et de retourner une réponse au Bot. Un exemple de code vous est fourni dans le fichier `nlp/lambda_function.py`.

Vous pouvez aller dans le service Lambda sur AWS et créer une nouvelle fonction. J'ai choisi python3.6 dans mon exemple, mais vous pouvez prendre le langage que vous préférez.

Dans un premier temps, occupez-vous simplement de sa création et assurez-vous qu'elle puisse envoyer une réponse qui sera prononcée par le Bot. Vous pouvez utiliser le module `requests` pour interroger l'API implémentant dans la logique du jeu.

## EC2 : La logique du jeu

Il va falloir créer une instance EC2 (J'ai pris une **Ubuntu 18.04**, une **t2.micro** sera suffisante pour notre usage.) contenant le code du fichier `app.py`. Ce code est une base exposant une API pour la logique du jeu, il gère :

  - Le maintien du tableau de jeu
  - La possibilité pour l'utilisateur de jouer un coup
  - La possibilité pour le robot de jouer un coup
  - La possibilité de réinitialiser le tableau.

Nous utilisons la librairie **Flask** en **Python**. Encore une fois, vous pouvez choisir d'utiliser un autre langage pour cela. 

Il faudra donc mettre le code sur l'instance, ouvrir le port et lancer le service d'API. Si vous choisissez de partir en python, voici les instructions pour parametrer l'instance.

Le code expose l'API sur le port 5001, il faudra donc l'ouvrir vers l'exterieur dans les **security-group** de l'EC2. Une autre possibilité est de placer un **role IAM** sur votre Lambda lui autorisant à utiliser les services EC2.

Puis parametrer l'environnement :

```bash
sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install -y python3-pip python3-dev
pip3 install --user pipenv
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc

git clone https://gitlab.com/r_queraud_catie/cours-nlp-2-projet  # Ce projet
cd cours-nlp-2-projet/  # Ce projet

pipenv install
pipenv run python app.py
```

Pour développer directement sur l'EC2, vous pouvez utiliser le plugin `ssh fs` de Visual Studio Code. Vous pouvez également utiliser directement `nano` ou n'importe quel autre editeur directement sur l'EC2 si vous êtes à l'aise.

## Raccorder les différents élements

Maintenant que tout est en place, vous pouvez faire en sorte que le Chatbot fonctionne et qu'on puisse jouer au TicTacToe. Il y a du code à trou pour :

  - La fonction Lambda.
  - La logique du jeu sur le service Flask.

## Amélioration : un bot intelligent

Le bot joue au hasard sur les cases de tableau. Un des avantages du TicTacToe est qu'il est simple de ne perdre aucune partie et d'arriver sur des égalités.

Votre bot jouant au hasard, pour le moment, il est facile de gagner. Vous pouvez trouver une solution pour qu'il y ait toujours égalité si les deux entités jouent parfaitement ! Certaines familles d'algorithmes peuvent vous aider :

  - L'algorithme du [min-max](https://fr.wikipedia.org/wiki/Algorithme_minimax) et ses variantes négamax, élagage alpha-beta, ... efficace bien que long et couteux !
  - Les algorithmes génétiques
  - L'apprentissage par renforcement
