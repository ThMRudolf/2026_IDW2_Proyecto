const BASE_URL = "http://127.0.0.1:8000";

async function getItems(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(`Error cargando ${endpoint}`);
  }

  const data = await response.json();
  return data.items || data;
}

export async function getStandings() {
  return getItems("/api/standings");
}

export async function getVenues() {
  return getItems("/api/venues?limit=20");
}

export async function getCountries() {
  return getItems("/api/countries");
}

export async function getInstagramPosts() {
  return getItems("/api/instagram");
}

// <option value={262}>Liga MX</option>
// <option value={39}>Premier League</option>
// <option value={140}>La Liga</option>
// <option value={135}>Serie A</option>
// <option value={78}>Bundesliga</option>
// <option value={61}>Ligue 1</option>
export async function getTopScorers() {
  try {
    return await getItems("/api/external/topscorers?league=39&season=2023");
  } catch {
    return [];
  }
}