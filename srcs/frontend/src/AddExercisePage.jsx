import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AddExercisePage = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [exerciseName, setExerciseName] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setVideoFile(event.target.files[0]);
  };

  const handleNameChange = (event) => {
    setExerciseName(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Logique pour uploader la vidéo et ajouter l'exercice
    console.log('Video file:', videoFile);
    console.log('Exercise name:', exerciseName);
    // Rediriger vers la page Kine après l'ajout
    navigate('/kine');
  };

  return (
    <div className="d-flex flex-column align-items-center justify-content-center vh-100" style={{ backgroundColor: "#F3E5F5" }}>
      <div className="p-5 bg-white rounded shadow text-center" style={{ maxWidth: "600px", width: "100%" }}>
        <h1 className="mb-4" style={{ color: "#4B0082" }}>Ajouter un Exercice</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="exerciseName" className="form-label" style={{ color: "#4B0082" }}>Nom de l'exercice:</label>
            <input
              type="text"
              className="form-control"
              id="exerciseName"
              value={exerciseName}
              onChange={handleNameChange}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="videoFile" className="form-label" style={{ color: "#4B0082" }}>Vidéo de l'exercice:</label>
            <input
              type="file"
              className="form-control"
              id="videoFile"
              onChange={handleFileChange}
              required
            />
          </div>
          <button type="submit" className="btn btn-lg w-100" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }}>
            Ajouter l'exercice
          </button>
        </form>
      </div>
    </div>
  );
};

export default AddExercisePage;
