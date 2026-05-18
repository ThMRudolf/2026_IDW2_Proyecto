from datetime import datetime
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Story, Standing

db: Session = SessionLocal()

try:
    # =========================
    # HISTORIAS
    # =========================

    existing_story = db.query(Story).first()

    if not existing_story:
        stories = [
            Story(
                title="México se prepara para inaugurar el Mundial 2026",
                section="Historias destacadas",
                body="La Ciudad de México se alista para recibir partidos históricos de la Copa Mundial 2026, con el Estadio Azteca como uno de los escenarios principales.",
                image_url="https://images.unsplash.com/photo-1518696957610-1c28c5cf1d8f?auto=format&fit=crop&w=900&q=80",
                user_id="admin",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),

            Story(
                title="Las ciudades anfitrionas se preparan para recibir al mundo",
                section="Ciudades anfitrionas",
                body="México, Estados Unidos y Canadá compartirán una edición histórica del torneo, con sedes listas para recibir a millones de aficionados.",
                image_url="https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a?auto=format&fit=crop&w=900&q=80",
                user_id="admin",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),

            Story(
                title="El escenario de la Copa Mundial está listo",
                section="Mundial 2026",
                body="La edición 2026 reunirá a 48 selecciones y se celebrará en tres países anfitriones, marcando una nueva etapa para el futbol internacional.",
                image_url="https://images.unsplash.com/photo-1486286701208-1d58e9338301?auto=format&fit=crop&w=900&q=80",
                user_id="admin",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),

            Story(
                title="Estados Unidos tendrá múltiples sedes mundialistas",
                section="Sedes",
                body="Estados Unidos contará con varias ciudades anfitrionas y estadios de gran capacidad para albergar partidos clave del torneo.",
                image_url="https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a?auto=format&fit=crop&w=900&q=80",
                user_id="admin",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),

            Story(
                title="Canadá se suma a una edición histórica",
                section="Países anfitriones",
                body="Canadá formará parte de una Copa Mundial compartida por primera vez entre tres países, fortaleciendo la presencia del futbol en Norteamérica.",
                image_url="https://images.unsplash.com/photo-1517090504586-fde19ea6066f?auto=format&fit=crop&w=900&q=80",
                user_id="admin",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]

        db.add_all(stories)
        print("Historias agregadas correctamente.")

    else:
        print("Las historias ya existen. No se duplicó información.")

    # =========================
    # CLASIFICACIÓN
    # =========================

    existing_standing = db.query(Standing).first()

    if not existing_standing:
        standings = [
            Standing(
                group_name="A",
                team="México",
                flag_url="https://flagcdn.com/w320/mx.png",
                played=3,
                wins=3,
                draws=0,
                losses=0,
                points=9,
            ),

            Standing(
                group_name="A",
                team="Canadá",
                flag_url="https://flagcdn.com/w320/ca.png",
                played=3,
                wins=2,
                draws=1,
                losses=0,
                points=7,
            ),

            Standing(
                group_name="B",
                team="Estados Unidos",
                flag_url="https://flagcdn.com/w320/us.png",
                played=3,
                wins=2,
                draws=0,
                losses=1,
                points=6,
            ),
        ]

        db.add_all(standings)
        print("Clasificación agregada correctamente.")

    else:
        print("La clasificación ya existe. No se duplicó.")

    db.commit()

except Exception as error:
    db.rollback()
    print("Error cargando datos:", error)

finally:
    db.close()