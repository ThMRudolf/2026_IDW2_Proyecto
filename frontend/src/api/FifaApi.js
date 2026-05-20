const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

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

export async function getTopScorers(league = 782, season = 2024) {
  try {
    return await getItems(`/api/external/topscorers?league=${league}&season=${season}`);
  } catch {
    return [];
  }
}