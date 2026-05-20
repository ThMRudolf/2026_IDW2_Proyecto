# FIFA 2026 — Imitación

## Resumen del producto
FIFA 2026 -Imitación es un proyecto web inspirado en la Copa Mundial de la FIFA de 2026. La pagina le permite al usuario consultar y mostrar información relacionada con los diferentes partidos a jugar. Se tienen varios apartados para los paises anfitriones, las sedes, los grupos, historias de aficionados y contenido de tipo red social.

El sistema se diseñó a base de React y Vite para el frontend, mientras que el backend con FastAPI. El frontend consume los servicios de backend mediante una API REST, mientras que el backend administra la lógica del negocio, la conexión a la base de datos y la integración con fuentes externas como API-Football v3.

## Autores
- Natalia Fernandez Mendez
- Ana Lucia Ladron
- Thomas M. Rudolf

## Levantar el frontend
cd frontend
npm install
npm run dev

## Tecnologías usadas
### Frontend 
- React 
- Vite
- Bootstrap
- JavaScript
- HTML
- CSS

### Backend 
- Pyhton 
- FastAPI
- SQLAlchemy
- UVicorn
- Base de datos relacional
- CORS Middleware

## Herramientas adicionales 
- Github y Git
- API-Football v3 
- Variables de entorno mediante archivo .env

## Descripción del fronend 
El frontend es la parte visual de la aplicación. Está construido con React y configurado con Vite, lo cual permite levantar un servidor de desarrollo rápido.
El archivo index.html contiene el punto de entrada principal de la aplicación:<div id="root"></div>
<script type="module" src="/src/main.jsx"></script>
React se monta sobre el elemento con id root, y desde ahí se renderizan los componentes principales de la aplicación.

## Descripción del backend
El backend está desarrollado con FastAPI. Su función principal es exponer una API REST para que el frontend pueda consultar, crear y administrar información del proyecto.
El archivo principal del backend es main.py. Este archivo se encarga de:
- Crear la aplicación de FastAPI.
- Crear las tablas de la base de datos al iniciar el servidor.
- Configurar CORS para permitir que el frontend se comunique con el backend.
- Registrar los routers principales de la API.

## Levantar el backend
# Windows:
p2env\Scripts\activate 
# Linux / Mac
# source p2env/bin/activate 


# or if not exist yet p2env
# python -m venv 2penv
# pip install -r requirements.txt
# p2env\Scripts\activate  or  source p2env/bin/activate 

cd backend
python seed.py                 # solo primera vez
uvicorn main:app --reload

## Variables de entorno
Para configurar el proyecto se debe crear el archivo .env y definir el API-KEY de API-Football v3 entre otros: .env
Después, completar los valores necesarios.
Ejemplo de variables de entorno:
ALLOWED_ORIGINS=http://localhost:5173
API_FOOTBALL_KEY=tu_api_key

Variable ALLOWED_ORIGINS

Esta variable indica qué frontend tiene permiso de llamar al backend desde el navegador.
En desarrollo local normalmente se usa:
ALLOWED_ORIGINS=http://localhost:5173
En producción se debe cambiar por la URL real del frontend desplegado.

## Flujo general del funcionamiento 
1. El usuario abre el frontend desde el navegador.
2. React renderiza la interfaz principal del proyecto.
3. El frontend realiza peticiones HTTP al backend.
4. FastAPI recibe las solicitudes en sus endpoints.
5. El backend consulta la base de datos o servicios externos.
6. La información regresa al frontend y se muestra en pantalla.

## Comando utiles 
# Frontend
npm install	--> Instala las dependencias del frontend.
npm run dev	--> Levanta el servidor de desarrollo de Vite.
npm run build	--> Genera la versión de producción del frontend.
npm run preview	--> Previsualiza la versión de producción.

## Estado del proyecto
Actualmente el proyecto cuenta con la estructura base del frontend y backend, configuración de Vite, configuración principal de FastAPI, routers separados por funcionalidad y preparación para conexión con datos internos y externos.

## Links
- Frontend: https://...
- API Health:
- Live demo: 19.05.2026, 9:30 via Teams
