# rest-api-with-keycloak

## Introduccion

Este proyecto intenta demostrar como podemos integrar Keycloak en un REST API, delegando la responsabilidad de la autenticacion a otro servicio.

## Como esta compuesto este proyecto?

Si es tu deseo recorrer el codigo, dejame guiarte un poco.
Dentro del directorio `src/` es donde ocurre la magia. Ahi vas a encontrar dos directorios mas: `apps` y `modules`
El directorio de `apps` esta conformado por el siguiente arbol:

- `books`
  - `dto`: contiene los modelos de Data Transfer Object
  - `mock`: contiene un solo archivo con datos "hardcodeados"
  - `router.py`: contiene todas las rutas con sus respectivos metodos

Mientras que el directorio `modules` esta conformado asi:

- `auth`
  - `auth`: contiene los metodos y dependencias necesarias para la Autenticacion

El REST API contiene dos rutas: una publica (`/books`) y una privada (`/books/loans`)

## Como configurar y poner a funcionar el proyecto?

Bueno, hay una serie de cosas que hacer primero.
Inicialmente vas a tener que configurar Keycloak. Asi que podemos arrancar con el siguiente comando:

```bash
docker-compose up db keycloak -d
```

Luego vas a acceder a `localhost:8081` que es donde va a estar corriendo el servicio de Keycloak. Una vez en el panel de Inicio de Sesion solo tenes que colocar las credenciales indicadas en `keycloak.env`.

Cuando hayas iniciado sesion, vas a tener que hacer tres cosas:

1. Crear un Realm
2. Crear un Client
3. Crear un User.

### Como crear un "Realm"?

En el menu desplegable vas a encontrar un boton para crearlo

![keycloak - crear realm](/docs/img/image.png)

En el formulario solo tenes que indicar un nombre y darle en "Create"

![keycloak - crear realm - formulario](/docs/img/image-1.png)

Vas a ver que ahora en el menu desplegable ya aparece el Realm y ademas se encuentra seleccionado.

### Como crear un "client"?

En el mismo menu de antes, vamos a encontrar la opcion de "Clients"

![keycloak - crear cliente](/docs/img/image-2.png)

Vamos al boton de "Create client"

![keycloak - crear cliente - boton](/docs/img/image-3.png)

Rellenamos tal cual en las capturas (si conoces sobre Keycloak podes saltarte todos estos pasos)

![configuraciones generales - crear cliente](/docs/img/image-4.png)

![configuracion de capacidad - crear cliente](/docs/img/image-5.png)

![configuracion de inicio de sesion - crear cliente](/docs/img/image-6.png)

De aca debemos retener dos datos: el primero es el client_id que es el que indicamos en la captura 1 del formulario; el segundo es el client_secret que lo conseguimos aca

![obtener secreto - crear cliente](/docs/img/image-7.png)

### Como crear un Usuario?

Para crear un usuario nos dirigimos al menu y seleccionamos "Users" y damos en "Create new user"

![formulario - crear usuario](/docs/img/image-8.png)

Aca podes jugar con los datos del usuario. El unico obligatorio es el "username".

Le damos a "Save" y nos va a llevar a una vista nueva. Una vez que estemos ahi, vamos a "Credentials" y configuramos las credenciales nuevas. Para este caos de prueba, conviene desactivar la opcion de "Temporary".

![credenciales - crear usuario](/docs/img/image-9.png)

![configurar contraseña - crear usuario](/docs/img/image-10.png)

Listo! Ya tenemos configurado Keycloak

## Configuramos el REST API

Para que la aplicacion funcione es importante que rellenemos los valores de las keys vacias en `app.env`. Los datos los obtuvimos en los pasos anteriores.

Una vez que tenemos eso listo, solo ejecutamos `docker-compose up api -d`

Si todo esta bien, deberiamos poder acceder a `localhost:8080/docs` sin problemas.

## Como interactuar con el proyecto?

Obtener un token es sencillo:

```bash
# Usando httpie
http POST :8081/realms/$OIDC_REALM_NAME/protocol/openid-connect/token grant_type=client_credentials client_id=$OIDC_CLIENT_ID client_secret=$OIDC_CLIENT_SECRET username=$USERNAME password=$PASSWORD --form

# Usando cURL
curl -X POST \
  http://localhost:8081/realms/$OIDC_REALM_NAME/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials&client_id=$OIDC_CLIENT_ID&client_secret=$OIDC_CLIENT_SECRET&username=$USERNAME&password=$PASSWORD'
```

> Recorda reemplazar esas variables con los valores correspondientes.

Una vez que tenemos el Token, enviamos una peticion a la ruta protegida de la siguiente forma:

```bash
# Usando httpie
http :8000/books/loans --auth $TOKEN --auth-type bearer

# Usando cURL
curl -X GET \
  http://localhost:8000/books/loans \
  -H "Authorization: Bearer $TOKEN"
```
