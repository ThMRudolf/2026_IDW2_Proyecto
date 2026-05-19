//api/useFutbolData.js
import { useState, useEffect } from "react";

const BASE_URL = "http://127.0.0.1:8000";

async function fetchEndpoint(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`);
  if (!response.ok) throw new Error(`Error cargando ${endpoint}`);
  const data = await response.json();
  return data.items || data;
}

export function useTopScorers(league = 26, season = 2024) {
  const [scorers, setScorers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEndpoint(`/api/external/topscorers?league=${league}&season=${season}`)
      .then(setScorers)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [league, season]);

  return { scorers, loading, error };
}