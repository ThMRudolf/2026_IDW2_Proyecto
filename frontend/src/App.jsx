import { useEffect, useState } from "react";
import StoryCard from "./components/StoryCard";
import StoryForm from "./components/StoryForm";
import { getStories, createStory, updateStory, deleteStory } from "./api/StoryApi";
import {
  getStandings,
  getVenues,
  getCountries,
  getInstagramPosts,
  getTopScorers,
} from "./api/FifaApi";

function App() {
  const [stories, setStories] = useState([]);
  const [standings, setStandings] = useState([]);
  const [venues, setVenues] = useState([]);
  const [countries, setCountries] = useState([]);
  const [instagramPosts, setInstagramPosts] = useState([]);
  const [players, setPlayers] = useState([]);
  const [selectedStory, setSelectedStory] = useState(null);
  const [currentUser, setCurrentUser] = useState(sessionStorage.getItem("currentUser") || "admin");

  useEffect(() => {
    sessionStorage.setItem("currentUser", currentUser);
    loadStories();
    loadPageData();
  }, []);

  async function loadStories() {
    const data = await getStories();
    setStories(data);
    localStorage.setItem("stories", JSON.stringify(data));
    localStorage.setItem("storiesTimestamp", new Date().toISOString());
  }

  async function loadPageData() {
    try { setStandings(await getStandings()); } catch (e) { console.error(e); }
    try { setVenues(await getVenues()); } catch (e) { console.error(e); }
    try { setCountries(await getCountries()); } catch (e) { console.error(e); }
    try { setInstagramPosts(await getInstagramPosts()); } catch (e) { console.error(e); }
    try { setPlayers(await getTopScorers()); } catch (e) { console.error(e); }
  }

  async function handleSubmitStory(storyData) {
    if (selectedStory) {
      await updateStory(selectedStory.id, storyData, currentUser);
      setSelectedStory(null);
    } else {
      await createStory(storyData, currentUser);
    }

    await loadStories();
  }

  async function handleDeleteStory(id) {
    if (!window.confirm("¿Seguro que quieres eliminar esta historia?")) return;
    await deleteStory(id, currentUser);
    await loadStories();
  }

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark sticky-top" style={{ backgroundColor: "#061f33" }}>
        <div className="container">
          <a className="navbar-brand fw-bold" href="#">Mundial 2026</a>
          <div className="navbar-nav ms-auto">
            <a className="nav-link" href="#historias">Historias</a>
            <a className="nav-link" href="#administrar">Administrar</a>
            <a className="nav-link" href="#clasificacion">Clasificación</a>
            <a className="nav-link" href="#ciudades">Ciudades</a>
            <a className="nav-link" href="#paises">Países</a>
            <a className="nav-link" href="#instagram">Instagram</a>
            <a className="nav-link" href="#api">API Football</a>
          </div>
        </div>
      </nav>

      <section style={{ background: "#0b2239", color: "white", padding: "90px 0" }}>
        <div className="container">
          <p style={{ color: "#d4af37", letterSpacing: "3px", fontWeight: "bold" }}>COPA MUNDIAL 2026</p>
          <h1 style={{ fontSize: "64px", fontWeight: "800", maxWidth: "800px" }}>
            El fútbol une a tres países en una sola celebración
          </h1>
          <p style={{ fontSize: "22px", maxWidth: "700px" }}>
            Explora historias, ciudades anfitrionas, clasificación y contenido destacado rumbo al torneo más esperado del mundo.
          </p>
        </div>
      </section>

      <section className="container my-5" id="historias">
        <p className="text-uppercase fw-bold" style={{ color: "#d4af37", letterSpacing: "3px" }}>Noticias</p>
        <h2 className="display-5 fw-bold">Historias destacadas</h2>

        <div className="row g-4 mt-3">
          {stories.map((story) => (
            <StoryCard
              key={story.id}
              story={story}
              onEdit={(story) => setSelectedStory(story)}
              onDelete={handleDeleteStory}
            />
          ))}
        </div>
      </section>

      <section className="container my-5" id="administrar">
        <p className="text-uppercase fw-bold" style={{ color: "#d4af37", letterSpacing: "3px" }}>Administración</p>
        <h2 className="display-5 fw-bold">Administrar historias destacadas</h2>

        <label className="form-label mt-3">Usuario actual</label>
        <input
          className="form-control mb-4"
          value={currentUser}
          onChange={(e) => {
            setCurrentUser(e.target.value);
            sessionStorage.setItem("currentUser", e.target.value);
          }}
        />

        <StoryForm
          selectedStory={selectedStory}
          onSubmit={handleSubmitStory}
          onCancel={() => setSelectedStory(null)}
        />
      </section>

      <section className="container my-5" id="clasificacion">
        <p className="text-uppercase fw-bold" style={{ color: "#d4af37", letterSpacing: "3px" }}>Clasificación</p>
        <h2 className="display-5 fw-bold">Tabla de posiciones</h2>

        <table className="table table-hover mt-4">
          <thead className="table-dark">
            <tr>
              <th>Selección</th>
              <th>Grupo</th>
              <th>Jugados</th>
              <th>Ganados</th>
              <th>Empates</th>
              <th>Perdidos</th>
              <th>Puntos</th>
            </tr>
          </thead>
          <tbody>
            {standings.map((team) => (
              <tr key={team.id}>
                <td>{team.team}</td>
                <td>{team.group_name}</td>
                <td>{team.played}</td>
                <td>{team.wins}</td>
                <td>{team.draws}</td>
                <td>{team.losses}</td>
                <td>{team.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="container my-5" id="ciudades">
        <p className="text-uppercase fw-bold" style={{ color: "#d4af37", letterSpacing: "3px" }}>Sedes</p>
        <h2 className="display-5 fw-bold">Ciudades anfitrionas</h2>

        <div className="row g-4 mt-3">
          {venues.map((venue) => (
            <div className="col-12 col-md-4" key={venue.id}>
              <div className="card h-100 shadow-sm">
                <img src={venue.image_url} className="card-img-top" alt={venue.name} style={{ height: "230px", objectFit: "cover" }} />
                <div className="card-body">
                  <h4>{venue.name}</h4>
                  <p>{venue.city}</p>
                  <p><strong>Capacidad:</strong> {venue.capacity.toLocaleString("es-MX")}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="container my-5" id="instagram">
        <p className="text-uppercase fw-bold" style={{ color: "#d4af37", letterSpacing: "3px" }}>Social</p>
        <h2 className="display-5 fw-bold">Feed Instagram</h2>

        <div className="row g-4 mt-3">
          {instagramPosts.map((post) => (
            <div className="col-12 col-md-4" key={post.id}>
              <div className="card h-100 shadow-sm">
                <img src={post.image_url} className="card-img-top" alt={post.caption} style={{ height: "230px", objectFit: "cover" }} />
                <div className="card-body">
                  <p>{post.caption}</p>
                  <a href={post.link} target="_blank" rel="noreferrer" className="btn btn-outline-dark btn-sm">Ver publicación</a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="container my-5" id="paises">
        <p className="text-uppercase fw-bold" style={{ color: "#d4af37", letterSpacing: "3px" }}>Anfitriones</p>
        <h2 className="display-5 fw-bold">Países anfitriones</h2>

        <div className="row g-4 mt-3">
          {countries.map((country) => (
            <div className="col-12 col-md-4" key={country.id}>
              <div className="card h-100 shadow-sm p-4">
                <img src={country.flag_url} alt={country.name} style={{ width: "90px" }} />
                <h3 className="mt-3">{country.name}</h3>
                <p>{country.description}</p>
                <strong>Continente: {country.continent}</strong>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="container my-5" id="api">
        <p className="text-uppercase fw-bold" style={{ color: "#d4af37", letterSpacing: "3px" }}>API externa</p>
        <h2 className="display-5 fw-bold">Top goleadores</h2>

        {players.length === 0 ? (
          <div className="alert alert-warning mt-4">No se pudieron cargar jugadores desde API-FOOTBALL.</div>
        ) : (
          <div className="row g-4 mt-3">
            {players.map((player) => (
              <div className="col-12 col-md-4" key={player.id}>
                <div className="card p-4 h-100">
                  <h3>{player.name}</h3>
                  <p>{player.team}</p>
                  <strong>{player.goals} goles</strong>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </>
  );
}

export default App;