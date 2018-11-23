Nu punem pe git migrarile asa ca va trebui sa rulati urmatoarele 2 comenzi pentru a va crea baza de date:

python manage.py makemigrations voluntariat

python manage.py migrate

```angular2html
PYTEST
```
Trebuie rulata comanda "pytest" din linia de comanda din src pentru a rula testele

Pentru a vedea coverage-ul: pytest --cov

Alta comanda foarte utila: pytest --pdb, se opreste la primul fail si poti scrie comenzi sa vezi contextul.
pytest --pdb --maxfail=cate_vrei daca nu vrei sa se opreaasca decat la un anumit numar de failuri.


```angular2html
python manage.py shell_plus
```

Am adaugat o librarie ca sa lucram mai usor cu shell-ul oferit de django.
Folositi comanda asta, va importa toate modelele si tot ce aveti nevoie sa lucrati cu baza de date.

```angular2html
POSTGRES
```

Cand instalati postgres, alegeti parola "parola", rulati urmatoarele comenzi in linia de comanda DIN PYCHARM!
Trebuie neaparat sa aveti virtualenvironmentul activat.
Acesta este linkul de download: 
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows

setx PATH "%PATH%;C:\Program Files\PostgreSQL\9.3\bin"

psql -U postgres #introduceti parola "parola"

CREATE DATABASE proiectcolectiv OWNER postgres;

easy_install psycopg2.exe # .exe-ul este in rootul proiectului nostru
