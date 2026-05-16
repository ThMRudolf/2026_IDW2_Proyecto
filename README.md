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
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed.py                 # solo primera vez
uvicorn main:app --reload

## Variables de entorno
Copiar .env.example → .env y completar los valores

## Links
- Frontend: https://...
- API Health: https://api.tu-dominio.com/health
- Live demo: [link a presentación / video]