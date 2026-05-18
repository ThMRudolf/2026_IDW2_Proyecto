import { useEffect, useState } from "react";
import StoryCard from "./components/StoryCard";
import StoryForm from "./components/StoryForm";
import {
  getStories,
  createStory,
  updateStory,
  deleteStory,
} from "./api/StoryApi";

function App() {
  const [stories, setStories] = useState([]);
  const [selectedStory, setSelectedStory] = useState(null);
  const [currentUser, setCurrentUser] = useState(
    sessionStorage.getItem("currentUser") || "demo"
  );

  useEffect(() => {
    loadStories();
  }, []);

  async function loadStories() {
    try {
      const data = await getStories();
      setStories(data);
    } catch (error) {
      console.error(error);
    }
  }

  function handleUserChange(event) {
    setCurrentUser(event.target.value);
    sessionStorage.setItem("currentUser", event.target.value);
  }

  async function handleSubmitStory(storyData) {
    try {
      if (selectedStory) {
        await updateStory(selectedStory.id, storyData, currentUser);
        setSelectedStory(null);
      } else {
        await createStory(storyData, currentUser);
      }

      await loadStories();
    } catch (error) {
      console.error(error);
      alert("No se pudo guardar la historia.");
    }
  }

  async function handleDeleteStory(id) {
    const confirmDelete = window.confirm(
      "¿Seguro que quieres eliminar esta historia?"
    );

    if (!confirmDelete) return;

    try {
      await deleteStory(id, currentUser);
      await loadStories();
    } catch (error) {
      console.error(error);
      alert("No se pudo eliminar la historia. Revisa que seas el usuario que la creó.");
    }
  }

  const hostCities = [
    {
      id: 1,
      city: "Ciudad de México",
      country: "México",
      stadium: "Estadio Azteca",
      imageUrl: "https://images.unsplash.com/photo-1518659526054-190340b32735",
    },
    {
      id: 2,
      city: "Toronto",
      country: "Canadá",
      stadium: "BMO Field",
      imageUrl: "https://images.unsplash.com/photo-1517090504586-fde19ea6066f",
    },
    {
      id: 3,
      city: "Los Ángeles",
      country: "Estados Unidos",
      stadium: "SoFi Stadium",
      imageUrl: "https://images.unsplash.com/photo-1534190760961-74e8c1c5c3da",
    },
  ];

  const countries = [
    {
      id: 1,
      name: "México",
      description:
        "País con una gran tradición futbolera y sede de partidos históricos.",
    },
    {
      id: 2,
      name: "Estados Unidos",
      description:
        "Recibirá múltiples sedes y una gran cantidad de aficionados internacionales.",
    },
    {
      id: 3,
      name: "Canadá",
      description:
        "Será parte de una edición compartida e histórica del torneo.",
    },
  ];

  const instagramPosts = [
    {
      id: 1,
      username: "@mundialfans",
      caption: "La emoción ya se siente en las calles.",
      imageUrl: "https://images.unsplash.com/photo-1522778119026-d647f0596c20",
    },
    {
      id: 2,
      username: "@footballworld",
      caption: "Nuevas generaciones listas para brillar.",
      imageUrl: "https://images.unsplash.com/photo-1518091043644-c1d4457512c6",
    },
    {
      id: 3,
      username: "@stadiumlife",
      caption: "Los estadios se preparan para recibir al mundo.",
      imageUrl: "https://images.unsplash.com/photo-1577223625816-7546f13df25d",
    },
  ];

  const players = [
    { id: 1, name: "Jugador destacado 1", team: "Selección A", goals: 7 },
    { id: 2, name: "Jugador destacado 2", team: "Selección B", goals: 5 },
    { id: 3, name: "Jugador destacado 3", team: "Selección C", goals: 4 },
  ];

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark custom-navbar sticky-top">
        <div className="container">
          <a className="navbar-brand fw-bold" href="#">
            Mundial 2026
          </a>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#mainNavbar"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="mainNavbar">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <a className="nav-link" href="#historias">
                  Historias
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#administrar-historias">
                  Administrar
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#clasificacion">
                  Clasificación
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#ciudades">
                  Ciudades
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#paises">
                  Países
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <main>
        <section className="hero-section">
          <div className="container">
            <div className="row align-items-center">
              <div className="col-12 col-lg-7">
                <p className="hero-label">Copa Mundial 2026</p>
                <h1>El futbol une a tres países en una sola celebración</h1>
                <p className="hero-text">
                  Explora historias, ciudades anfitrionas, clasificación y
                  contenido destacado rumbo al torneo más esperado del mundo.
                </p>

                <div className="d-flex gap-3 flex-wrap">
                  <a href="#historias" className="btn btn-primary custom-btn">
                    Ver historias
                  </a>
                  <a href="#ciudades" className="btn btn-outline-light">
                    Explorar sedes
                  </a>
                </div>
              </div>

              <div className="col-12 col-lg-5 mt-4 mt-lg-0">
                <div className="stage-card">
                  <p className="mb-1">Próximo destino</p>
                  <h3>Mundial 2026</h3>
                  <p>México · Estados Unidos · Canadá</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="container my-5" id="historias">
          <div className="section-header">
            <p className="section-label">Noticias</p>
            <h2>Historias destacadas</h2>
            <p>Explora las noticias principales rumbo a la Copa Mundial 2026.</p>
          </div>

          <div className="row g-4">
            {stories.map((story) => (
              <StoryCard
                key={story.id}
                story={story}
                onEdit={setSelectedStory}
                onDelete={handleDeleteStory}
              />
            ))}
          </div>
        </section>

        <section className="container my-5" id="administrar-historias">
          <div className="section-header">
            <p className="section-label">Administración</p>
            <h2>Administrar historias destacadas</h2>
            <p>
              Crea, edita o elimina historias usando el usuario actual guardado
              en sessionStorage.
            </p>
          </div>

          <div className="mb-4">
            <label className="form-label">Usuario actual</label>
            <input
              type="text"
              className="form-control"
              value={currentUser}
              onChange={handleUserChange}
            />
          </div>

          <StoryForm
            selectedStory={selectedStory}
            onSubmit={handleSubmitStory}
            onCancel={() => setSelectedStory(null)}
          />
        </section>

        <section className="container my-5" id="clasificacion">
          <div className="section-header">
            <p className="section-label">Rumbo al torneo</p>
            <h2>Clasificación</h2>
            <p>Tabla de ejemplo que después vendrá desde PostgreSQL.</p>
          </div>

          <div className="table-responsive">
            <table className="table table-hover align-middle">
              <thead className="table-dark">
                <tr>
                  <th>Selección</th>
                  <th>Grupo</th>
                  <th>Puntos</th>
                  <th>Estatus</th>
                </tr>
              </thead>

              <tbody>
                <tr>
                  <td>México</td>
                  <td>A</td>
                  <td>9</td>
                  <td>
                    <span className="badge text-bg-primary">Clasificado</span>
                  </td>
                </tr>
                <tr>
                  <td>Canadá</td>
                  <td>A</td>
                  <td>7</td>
                  <td>
                    <span className="badge text-bg-primary">Clasificado</span>
                  </td>
                </tr>
                <tr>
                  <td>Estados Unidos</td>
                  <td>B</td>
                  <td>8</td>
                  <td>
                    <span className="badge text-bg-primary">Clasificado</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="worldcup-stage my-5">
          <div className="container">
            <div className="row align-items-center g-4">
              <div className="col-12 col-lg-6">
                <p className="section-label">Mundial 2026</p>
                <h2>El escenario de la Copa Mundial está listo</h2>
                <p>
                  La edición 2026 reunirá a tres países anfitriones, nuevas
                  ciudades sede y una experiencia global para millones de
                  aficionados.
                </p>
                <button className="btn btn-light">Ver más</button>
              </div>

              <div className="col-12 col-lg-6">
                <div className="stage-card">
                  <h3>48</h3>
                  <p>Selecciones participantes</p>
                  <hr />
                  <h3>3</h3>
                  <p>Países anfitriones</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="container my-5" id="ciudades">
          <div className="section-header">
            <p className="section-label">Sedes</p>
            <h2>Ciudades anfitrionas</h2>
            <p>Conoce algunas ciudades que recibirán partidos del torneo.</p>
          </div>

          <div className="row g-4">
            {hostCities.map((city) => (
              <div className="col-12 col-md-4" key={city.id}>
                <article className="city-card">
                  <img src={city.imageUrl} alt={city.city} />
                  <div className="p-4">
                    <p className="text-success fw-bold mb-1">{city.country}</p>
                    <h3>{city.city}</h3>
                    <span>{city.stadium}</span>
                  </div>
                </article>
              </div>
            ))}
          </div>
        </section>

        <section className="container my-5" id="instagram">
          <div className="section-header">
            <p className="section-label">Social</p>
            <h2>Feed Instagram</h2>
            <p>Simulación de publicaciones relacionadas con el torneo.</p>
          </div>

          <div className="row g-4">
            {instagramPosts.map((post) => (
              <div className="col-12 col-md-4" key={post.id}>
                <div className="instagram-card">
                  <img src={post.imageUrl} alt={post.caption} />
                  <div className="p-3">
                    <strong>{post.username}</strong>
                    <p>{post.caption}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="container my-5" id="paises">
          <div className="section-header">
            <p className="section-label">Anfitriones</p>
            <h2>Países anfitriones</h2>
            <p>México, Estados Unidos y Canadá comparten la organización.</p>
          </div>

          <div className="row g-4">
            {countries.map((country) => (
              <div className="col-12 col-md-4" key={country.id}>
                <div className="country-card">
                  <h3>{country.name}</h3>
                  <p>{country.description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="container my-5" id="api-football">
          <div className="section-header">
            <p className="section-label">API externa</p>
            <h2>Lo nuevo en la plataforma</h2>
            <p>
              Esta sección después se conectará al backend, y el backend llamará
              a API-FOOTBALL.
            </p>
          </div>

          <div className="external-box">
            <div className="row g-4">
              {players.map((player) => (
                <div className="col-12 col-md-4" key={player.id}>
                  <div className="player-card">
                    <p>{player.team}</p>
                    <h3>{player.name}</h3>
                    <span className="badge text-bg-success">
                      {player.goals} goles
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="container">
          <p className="mb-0">
            Proyecto integrador · Introducción al Desarrollo Web · Mundial 2026
          </p>
        </div>
      </footer>
    </>
  );
}

export default App;