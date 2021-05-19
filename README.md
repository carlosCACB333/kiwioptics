# kiwioptics
Software web en django para la gestion de prescripciones de medidas de la vista.
## Instalación en local
### Requerimientos
* Python 3.8 o 3.9
* PostgreSQL
* Git
### Procedimiento
1. Clone este proyecto, usando el comando:
> git clone url_repositorio_example
2. Instalar los packages necesarios usando el comando:
> pip install -r requirements.txt
3. Generar un secret_key para nuestro proyecto, la manera más fácil a través de [djecrety](https://djecrety.ir/)
4. Crear una base de datos en el postgresql
5. Tener un correo que tenga activado el acceso a aplicaciones poco seguras.
6. Crear un archivo ".env" en la raiz del directorio, donde pondremos las variables con sus valores por ejemplo:
```python
SECRET_KEY = secret_key
DB_HOST = dbhostexample
DB_NAME = dbnameexample
DB_PASSWORD = dbpasswordexample12345 
DB_PORT = 12345
DB_USER = userexample
MY_EMAIL = test@gmail.com
MY_EMAIL_PASSWORD = mypasswordexample12345 

GOOGLE_APPLICATION_CREDENTIALS = firebase-key.json
```
6. Migrar las tablas a la base de datos mediante el comando:
> python  manage.py migrate

7. Para hechar a andar el sistema, use el comando
> python manage.py runserver

8. Para ingresar al sistema, vaya a 127.0.0.1:8000

9. Para crear un usuario staff, use el comando
> python manage.py createsuperuser

10. Para ingresar al panel de administración vaya a 127.0.0.1:8000/admin

## Desplegar aplicacion en Heroku 
### Requerimientos
* Python 3.8 o 3.9
* PostgreSQL
* Cuenta en Heroku
* Heroku CLI
* Cuenta en Amazon AWS
* Git
### Procedimiento
1. Crear una nueva app con ayuda del [dashboard de heroku](https://dashboard.heroku.com/apps)
2. En la pestaña resources añada el add-on llamado "Heroku Postgres"
3. En settings de la bbdd mire las credenciales de la base de datos y copie el URL
4. En CONFIG_VARS deberá de añadir la variable DATABASE_URL con la url copiada.
5. En su cuenta de AWS crear un bucket de almacenamiento S3 y en los permisos añadir lo siguiente en el CORS:
```python
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "POST",
            "GET",
            "PUT"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```
6. Copiar y pegar el Access Key ID, Secret Access Key y el nombre de tu Bucket S3 en el CONFIG VARS de la app de heroku en las variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
7. Ahora las variables MY_EMAIL, MY_EMAIL_PASSWORD y SECRET_KEY del archivo ".env" lo trasladaremos al CONFIG VARS de heroku
8. Agregamos la variable DJANGO_SETTINGS_MODULE con el valor de myOptica.settings.prod
9. En buildpacks de la app, añada el buildpack de python
10. Para logearse y generar una nueva llave SSH, use el comando en el directorio de su proyecto:
> heroku login
11. Añadir el heroku remote
> heroku git:remote -a nombre_de_tu_app
12. En caso de haber cambios, usamos el comando:
> git add .
> git commit -m 'go'
13. Hacemos el push de los cambios a heroku
> git push heroku main
14. Entramos a la terminal de produccion
> heroku run bash
15. Ahora migramos las tablas a la base de datos de produccion
> python manage.py migrate
16. Creamos el superusuario o el staff
> python manage.py createsuperuser
17. Finalmente entramos al link https://nombre_de_tu_app.herokuapp.com y disfrutamos
