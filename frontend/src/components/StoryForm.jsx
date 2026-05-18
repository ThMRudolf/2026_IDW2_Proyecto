import { useEffect, useState } from "react";

function StoryForm({ selectedStory, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    title: "",
    section: "",
    body: "",
    image_url: "",
  });

  useEffect(() => {
    if (selectedStory) {
      setFormData({
        title: selectedStory.title || "",
        section: selectedStory.section || "",
        body: selectedStory.body || "",
        image_url: selectedStory.image_url || "",
      });
    }
  }, [selectedStory]);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit(formData);

    setFormData({
      title: "",
      section: "",
      body: "",
      image_url: "",
    });
  }

  return (
    <form className="card p-4 shadow-sm border-0" onSubmit={handleSubmit}>
      <h3 className="mb-3">
        {selectedStory ? "Editar historia" : "Crear historia"}
      </h3>

      <div className="mb-3">
        <label className="form-label">Título</label>
        <input
          type="text"
          name="title"
          className="form-control"
          value={formData.title}
          onChange={handleChange}
          required
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Sección</label>
        <input
          type="text"
          name="section"
          className="form-control"
          value={formData.section}
          onChange={handleChange}
          required
        />
      </div>

      <div className="mb-3">
        <label className="form-label">URL de imagen</label>
        <input
          type="url"
          name="image_url"
          className="form-control"
          value={formData.image_url}
          onChange={handleChange}
          required
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Cuerpo de la noticia</label>
        <textarea
          name="body"
          className="form-control"
          rows="4"
          value={formData.body}
          onChange={handleChange}
          required
        />
      </div>

      <div className="d-flex gap-2">
        <button type="submit" className="btn btn-success">
          {selectedStory ? "Guardar cambios" : "Crear historia"}
        </button>

        {selectedStory && (
          <button type="button" className="btn btn-secondary" onClick={onCancel}>
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}

export default StoryForm;