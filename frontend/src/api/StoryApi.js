const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const API_URL = `${BASE_URL}/api/stories`;

export async function getStories() {
  const cachedStories = localStorage.getItem("stories");
  const lastFetch = localStorage.getItem("storiesTimestamp");

  let url = API_URL;

  if (cachedStories && lastFetch) {
    url = `${API_URL}?since=${encodeURIComponent(lastFetch)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Error obteniendo historias");
  }

  const data = await response.json();
  const newItems = data.items || [];

  if (cachedStories && lastFetch) {
    const oldItems = JSON.parse(cachedStories);

    const merged = [
      ...newItems,
      ...oldItems.filter(
        (oldStory) => !newItems.some((newStory) => newStory.id === oldStory.id)
      ),
    ];

    localStorage.setItem("stories", JSON.stringify(merged));
    localStorage.setItem("storiesTimestamp", new Date().toISOString());

    return merged;
  }

  localStorage.setItem("stories", JSON.stringify(newItems));
  localStorage.setItem("storiesTimestamp", new Date().toISOString());

  return newItems;
}

export async function createStory(story, userId) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": userId,
    },
    body: JSON.stringify(story),
  });

  if (!response.ok) {
    throw new Error("Error creando historia");
  }

  localStorage.removeItem("stories");
  localStorage.removeItem("storiesTimestamp");

  return response.json();
}

export async function updateStory(id, story, userId) {
  const response = await fetch(`${API_URL}/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": userId,
    },
    body: JSON.stringify(story),
  });

  if (!response.ok) {
    throw new Error("Error editando historia");
  }

  localStorage.removeItem("stories");
  localStorage.removeItem("storiesTimestamp");

  return response.json();
}

export async function deleteStory(id, userId) {
  const response = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
    headers: {
      "X-User-Id": userId,
    },
  });

  if (!response.ok) {
    throw new Error("Error eliminando historia");
  }

  localStorage.removeItem("stories");
  localStorage.removeItem("storiesTimestamp");
}