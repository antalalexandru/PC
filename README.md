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