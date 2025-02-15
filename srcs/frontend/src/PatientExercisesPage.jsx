import React, { useState } from 'react';
import { useParams } from 'react-router-dom';

const PatientExercisesPage = () => {
  const { patientId } = useParams();
  const [exercises, setExercises] = useState([
    // Liste des exercices pour le patient
  ]);

  const addExercise = () => {
    const newExercise = { id: exercises.length + 1, name: `Exercice ${exercises.length + 1}` };
    setExercises([...exercises, newExercise]);
  };

  return (
    <div className="d-flex flex-column align-items-center justify-content-center vh-100" style={{ backgroundColor: "#F3E5F5" }}>
      <div className="p-5 bg-white rounded shadow text-center" style={{ maxWidth: "600px", width: "100%" }}>
        <h1 className="mb-4" style={{ color: "#4B0082" }}>Exercices pour {patientId}</h1>
        <ul className="list-group">
          {exercises.map((exercise) => (
            <li key={exercise.id} className="list-group-item" style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}>
              {exercise.name}
            </li>
          ))}
        </ul>
        <button
          className="btn btn-lg w-100 mt-3"
          style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }}
          onClick={addExercise}
        >
          Ajouter un exercice
        </button>
      </div>
    </div>
  );
};

export default PatientExercisesPage;
