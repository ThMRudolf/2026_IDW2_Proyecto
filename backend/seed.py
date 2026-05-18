from datetime import datetime
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Story, Standing, HostCountry, Venue, InstagramPost

Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

try:
    db.query(InstagramPost).delete()
    db.query(Venue).delete()
    db.query(HostCountry).delete()
    db.query(Standing).delete()
    db.query(Story).delete()
    db.commit()

    stories = [
        Story(
            title="México se prepara para inaugurar el Mundial 2026",
            section="Historias destacadas",
            body="La Ciudad de México se alista para recibir partidos históricos de la Copa Mundial 2026.",
            image_url="https://images.unsplash.com/photo-1518659526054-190340b32735?auto=format&fit=crop&w=900&q=80",
            user_id="admin",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        Story(
            title="Estados Unidos tendrá múltiples sedes mundialistas",
            section="Sedes",
            body="Estados Unidos contará con varias ciudades anfitrionas y estadios de gran capacidad.",
            image_url="https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=900&q=80",
            user_id="admin",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        Story(
            title="Canadá se suma a una edición histórica",
            section="Países anfitriones",
            body="Canadá será parte de una Copa Mundial compartida por primera vez entre tres países.",
            image_url="https://images.unsplash.com/photo-1517090504586-fde19ea6066f?auto=format&fit=crop&w=900&q=80",
            user_id="admin",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
    ]

    standings = [
        Standing(group_name="A", team="México", flag_url="https://flagcdn.com/w320/mx.png", played=3, wins=3, draws=0, losses=0, points=9),
        Standing(group_name="A", team="Canadá", flag_url="https://flagcdn.com/w320/ca.png", played=3, wins=2, draws=1, losses=0, points=7),
        Standing(group_name="B", team="Estados Unidos", flag_url="https://flagcdn.com/w320/us.png", played=3, wins=2, draws=0, losses=1, points=6),
    ]

    countries = [
        HostCountry(name="México", flag_url="https://flagcdn.com/w320/mx.png", description="México será anfitrión con sedes en Ciudad de México, Guadalajara y Monterrey.", continent="América"),
        HostCountry(name="Estados Unidos", flag_url="https://flagcdn.com/w320/us.png", description="Estados Unidos tendrá la mayor cantidad de sedes del Mundial 2026.", continent="América"),
        HostCountry(name="Canadá", flag_url="https://flagcdn.com/w320/ca.png", description="Canadá participará como anfitrión con sedes en Toronto y Vancouver.", continent="América"),
    ]

    db.add_all(stories)
    db.add_all(standings)
    db.add_all(countries)
    db.commit()

    mexico = db.query(HostCountry).filter_by(name="México").first()
    usa = db.query(HostCountry).filter_by(name="Estados Unidos").first()
    canada = db.query(HostCountry).filter_by(name="Canadá").first()

    venues = [
        Venue(name="Estadio Azteca", city="Ciudad de México", capacity=87000, image_url="https://images.unsplash.com/photo-1518659526054-190340b32735?auto=format&fit=crop&w=900&q=80", host_country_id=mexico.id),
        Venue(name="Estadio Akron", city="Guadalajara", capacity=48000, image_url="https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=900&q=80", host_country_id=mexico.id),
        Venue(name="Estadio BBVA", city="Monterrey", capacity=53500, image_url="https://images.unsplash.com/photo-1577223625816-7546f13df25d?auto=format&fit=crop&w=900&q=80", host_country_id=mexico.id),

        Venue(name="MetLife Stadium", city="Nueva York / Nueva Jersey", capacity=82500, image_url="https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="SoFi Stadium", city="Los Ángeles", capacity=70000, image_url="https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="AT&T Stadium", city="Dallas", capacity=80000, image_url="https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="NRG Stadium", city="Houston", capacity=72000, image_url="https://images.unsplash.com/photo-1577223625816-7546f13df25d?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="Mercedes-Benz Stadium", city="Atlanta", capacity=71000, image_url="https://images.unsplash.com/photo-1560272564-c83b66b1ad12?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="Hard Rock Stadium", city="Miami", capacity=65000, image_url="https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="Lincoln Financial Field", city="Filadelfia", capacity=69000, image_url="https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="Lumen Field", city="Seattle", capacity=68000, image_url="https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="Levi's Stadium", city="San Francisco Bay Area", capacity=68500, image_url="https://images.unsplash.com/photo-1518091043644-c1d4457512c6?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="Gillette Stadium", city="Boston", capacity=65000, image_url="https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),
        Venue(name="GEHA Field at Arrowhead Stadium", city="Kansas City", capacity=76000, image_url="https://images.unsplash.com/photo-1505842465776-3f6d9b39c6d9?auto=format&fit=crop&w=900&q=80", host_country_id=usa.id),

        Venue(name="BMO Field", city="Toronto", capacity=45000, image_url="https://images.unsplash.com/photo-1517090504586-fde19ea6066f?auto=format&fit=crop&w=900&q=80", host_country_id=canada.id),
        Venue(name="BC Place", city="Vancouver", capacity=54500, image_url="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80", host_country_id=canada.id),
    ]

    posts = [
        InstagramPost(image_url="https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=900&q=80", caption="La emoción ya se siente rumbo al Mundial 2026.", link="https://www.fifa.com", posted_at=datetime.utcnow()),
        InstagramPost(image_url="https://images.unsplash.com/photo-1518091043644-c1d4457512c6?auto=format&fit=crop&w=900&q=80", caption="Aficionados de todo el mundo se preparan para vivir una edición histórica.", link="https://www.fifa.com", posted_at=datetime.utcnow()),
        InstagramPost(image_url="https://images.unsplash.com/photo-1577223625816-7546f13df25d?auto=format&fit=crop&w=900&q=80", caption="Los estadios anfitriones se preparan para recibir al mundo.", link="https://www.fifa.com", posted_at=datetime.utcnow()),
    ]

    db.add_all(venues)
    db.add_all(posts)
    db.commit()

    print("Base de datos reiniciada y cargada correctamente.")

except Exception as error:
    db.rollback()
    print("ERROR:", error)

finally:
    db.close()