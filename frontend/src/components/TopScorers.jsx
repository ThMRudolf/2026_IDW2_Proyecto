// components/TopScorers.jsx
import { useTopScorers } from "../api/useFutbolData";

export default function TopScorers() {
  const { scorers, loading, error } = useTopScorers(262, 2026); // liga mexicana

  if (loading) return <p>Cargando...</p>;
  if (error)   return <p>Error: {error.message}</p>;

  return (
    <ul>
      {scorers.map((s) => (
        <li key={s.id}>
          <img src={s.avatar_url} alt={s.name} width={40} />
          {s.name} — {s.goals} goles ({s.team})
        </li>
      ))}
    </ul>
  );
}