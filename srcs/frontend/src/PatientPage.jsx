import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CameraStream from './components/CameraStream';

const PatientPage = () => {
  const [exercises, setExercises] = useState([
    { id: 1, name: 'Exercice 1', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_1' },
    { id: 2, name: 'Exercice 2', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_2' },
  ]);

  const [selectedExercise, setSelectedExercise] = useState(null);
  const [showCamera, setShowCamera] = useState(false);
  const [message, setMessage] = useState("");

  const selectExercise = (exercise) => {
    setSelectedExercise(exercise);
    setShowCamera(false);
  };

  const startExercise = () => {
    setShowCamera(true);
  };

  useEffect(() => {
    axios.get("http://localhost:8000/api/")
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch((error) => {
        console.error("Erreur lors de la récupération des données", error);
      });
  }, []);

  return (
    <div className="d-flex flex-column align-items-center justify-content-center vh-100" style={{ backgroundColor: "#F3E5F5" }}>
      <div className="p-5 bg-white rounded shadow text-center" style={{ maxWidth: "600px", width: "100%" }}>
        <h1 className="text-purple-600 mb-4">Sélectionnez votre exercice:</h1>
        <div className="d-flex flex-wrap justify-content-center">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="m-2">
              <button
                className="btn btn-lg"
                style={{ backgroundColor: "#D8BFD8", color: "#4B0082", width: "150px" }}
                onClick={() => selectExercise(exercise)}
              >
                {exercise.name}
              </button>
            </div>
          ))}
        </div>
        {selectedExercise && (
          <div className="mt-4">
            <h2>Exercice sélectionné: {selectedExercise.name}</h2>
            <div className="embed-responsive embed-responsive-16by9">
              <iframe
                className="embed-responsive-item"
                src={selectedExercise.videoUrl}
                allowFullScreen
                title="Exercice Video"
              ></iframe>
            </div>
            {/* <button className="btn btn-lg w-100 mt-3" style={{ backgroundColor: "#BA55D3", color: "white" }} onClick={startExercise}>
              Commencer l'exercice
            </button> */}

            <button
              className="btn btn-lg w-100 mt-3"
              style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
              onClick={startExercise}
            >
              Commencer l'exercice
            </button>
            {showCamera && <CameraStream />}
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientPage;
