# Aplicatia de voluntariat GOAT

Scopul acestei aplicatii este usurarea muncii voluntarilor si a organizatorilor
de evenimente de voluntariat.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Get the source:
```
$ git clone https://github.com/antalalexandru/PC.git
```

### Prerequisites

Python and PostgreSQL Database.

## Important

Nu punem pe git migrarile asa ca va trebui sa rulati urmatoarele 2 comenzi pentru a va crea baza de date:

```
python manage.py makemigrations voluntariat
python manage.py migrate
```

## PYTEST

To run the tests:

```
cd src
pytest
```

To see the coverage:
```
pytest --cov
```

Alta comanda foarte utila:
```
pytest --pdb
```
se opreste la primul fail si poti scrie comenzi sa vezi contextul.
```
pytest --pdb --maxfail=cate_vrei
```
daca nu vrei sa se opreaasca decat la un anumit numar de failuri.


## shell_plus

Am adaugat o librarie ca sa lucram mai usor cu shell-ul oferit de django.
Folositi comanda asta, va importa toate modelele si tot ce aveti nevoie sa lucrati cu baza de date.

```
python manage.py shell_plus
```

## Deployment

For now:
```
git remote add origin https://github.com/antalalexandru/PC.git
...change something...
git add -A
git commit -m "My change"
git push -u origin master
```

## Authors

* Dan Ailenei - Project Manager
* Alexandru Antal
* Alexandra Boicu
* Alex Ardelean
* Ana Bosutar
* Andra Runcan
* Denis Barnutiu
* Dragos Teodor
* Iulia Baraian
