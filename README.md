# WebComics

### Setup

Il progetto è stato realizzato utilizzando python 3.10 e la gestione dei pacchetti è stata effettuata tramite Pipenv.

Installare Pipenv:

```
pip install pipenv
```

Usare pipenv per installare tutti i pacchetti necessari:

```
pipenv install
```

Infine aprire una shell con il comando:

```
pipenv shell
```

### Esecuzione

Per avviare il server eseguire il comando:

```
python manage.py runserver
```

Questo aprirà un server locale sulla porta 8000.
Per accedervi visitare http://localhost:8000/

Le credenziali di accesso come admin sono:
- username: admin
- password: admin


### Test

Per eseguire i test eseguire il comando:

```
python manage.py test
```
