function StoryCard({ story, onEdit, onDelete }) {
  function handleEdit() {
    onEdit(story);

    setTimeout(() => {
      document
        .getElementById("administrar-historias")
        ?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  }

  return (
    <div className="col-12 col-md-4">
      <article className="card story-card h-100">
        <img
          src={story.image_url}
          className="card-img-top"
          alt={story.title}
        />

        <div className="card-body">
          <span className="badge text-bg-success mb-2">
            {story.section}
          </span>

          <h5 className="card-title">{story.title}</h5>

          <p className="card-text">{story.body}</p>
        </div>

        <div className="card-footer bg-white border-0 d-flex gap-2">
          <button type="button" className="btn btn-outline-dark btn-sm">
            Leer más
          </button>

          <button
            type="button"
            className="btn btn-outline-primary btn-sm"
            onClick={handleEdit}
          >
            Editar
          </button>

          <button
            type="button"
            className="btn btn-outline-danger btn-sm"
            onClick={() => onDelete(story.id)}
          >
            Eliminar
          </button>
        </div>
      </article>
    </div>
  );
}

export default StoryCard;