import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const KinePage = () => {
  // Liste des exercices enregistrés pour le kiné
  const [exercises, setExercises] = useState([
    { id: 1, name: 'Exercice 1', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_1' },
    { id: 2, name: 'Exercice 2', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_2' },
    // Ajoute d'autres exercices ici si nécessaire
  ]);

  // Liste des patients
  const [patients, setPatients] = useState([
    { id: 1, name: 'Patient 1' },
    { id: 2, name: 'Patient 2' },
    // Ajoute d'autres patients ici si nécessaire
  ]);

  const navigate = useNavigate();

  // Fonction pour ajouter un nouveau patient
  const addPatient = () => {
    const newPatient = { id: patients.length + 1, name: `Patient ${patients.length + 1}` };
    setPatients([...patients, newPatient]);
  };

  // Fonction pour naviguer vers la page d'exercices d'un patient
  const goToPatientExercises = (patientId) => {
    navigate(`/patient/${patientId}/exercises`);
  };

  // Fonction pour naviguer vers la page d'ajout d'exercice
  const goToAddExercise = () => {
    navigate('/kine/add-exercise');
  };

  return (
    <div className="d-flex flex-column align-items-center justify-content-center vh-100" style={{ backgroundColor: "#F3E5F5" }}>
      <div className="p-5 bg-white rounded shadow text-center" style={{ maxWidth: "800px", width: "100%" }}>
        <h1 className="mb-4" style={{ color: "#4B0082" }}>Vos Exercices:</h1>
        <div className="d-flex flex-wrap justify-content-center mb-4">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="m-2">
              <div className="embed-responsive embed-responsive-16by9" style={{ width: "300px" }}>
                <iframe
                  className="embed-responsive-item"
                  src={exercise.videoUrl}
                  allowFullScreen
                  title={`Exercice Video ${exercise.id}`}
                ></iframe>
              </div>
              <p className="text-center mt-2" style={{ color: "#4B0082" }}>{exercise.name}</p>
            </div>
          ))}
        </div>
        <button
          className="btn btn-lg w-100 mt-3 mb-4"
          style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
          onClick={goToAddExercise}
        >
          Ajouter un exercice
        </button>

        <h1 className="mb-4" style={{ color: "#4B0082" }}>Vos Patients:</h1>
        <div className="d-flex flex-wrap justify-content-center">
          {patients.map((patient) => (
            <div key={patient.id} className="m-2">
              <button
                className="btn btn-lg"
                style={{ backgroundColor: "#D8BFD8", color: "#4B0082", width: "150px" }}
                onClick={() => goToPatientExercises(patient.id)}
              >
                {patient.name}
              </button>
            </div>
          ))}
        </div>
        <button
          className="btn btn-lg w-100 mt-3"
          style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
          onClick={addPatient}
        >
          Ajouter un patient
        </button>
      </div>
    </div>
  );
};

export default KinePage;
