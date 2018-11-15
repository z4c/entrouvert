# Entrouvert

Dans une idée de prévenir les situations de burnout des développeurs, on
voudrait produire un rapport reprenant par personne un taux de travail
"hors horaires", qu'on définirait comme le part de commits qui sont
réalisés le week-end ou avant 8h / après 20h.

L'exercice est donc l'écriture d'un script Python qui prendrait les 
données du dépôt d'une de nos applications (prenons Passerelle :
  https://git.entrouvert.org/passerelle.git) et afficherait ces taux.

# How to use
## Environment setup

Replace git repository if needed in main.py 

```
GIT_REMOTE_URL = ....
```

Then open a terminal and run

```
git clone git@github.com:z4c/entrouvert.git \
    && cd entrouvert && virtualenv -p python3 . && source bin/activate \
    && pip install -r requirements.txt && python main.py \
    || echo "Whoopsey ! let me know what's going wrong @ https://github.com/z4c/entrouvert/issues/new "
```

Cheers,

