Nu punem pe git migrarile asa ca va trebui sa rulati urmatoarele 2 comenzi pentru a va crea baza de date:

python manage.py makemigrations voluntariat

python manage.py migrate


Cand instalati postgres, alegeti parola "parola", rulati urmatoarele comenzi in linia de comanda DIN PYCHARM!
Trebuie neaparat sa aveti virtualenvironmentul activat.
Acesta este linkul de download: 
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows

setx PATH "%PATH%;C:\Program Files\PostgreSQL\9.3\bin"

psql -U postgres #introduceti parola "parola"

CREATE DATABASE proiectcolectiv OWNER postgres;

easy_install psycopg2.exe # .exe-ul este in rootul proiectului nostru