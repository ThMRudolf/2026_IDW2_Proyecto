# FIFA 2026 — Imitación

## Resumen del producto
[Descripción del proyecto]

## Autores
- Natalia Fernandez Mendez
- Ana Lucia Ladron
- Thomas M. Rudolf

## Levantar el frontend
cd frontend
npm install
npm run dev

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
Copiar .env.example → .env y completar los valores

## Links
- Frontend: https://...
- API Health: https://api.tu-dominio.com/health
- Live demo: [link a presentación / video]