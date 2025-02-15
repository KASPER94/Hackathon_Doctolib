import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './HomePage';
import KinePage from './KinePage';
import PatientPage from './PatientPage';
import PatientExercisesPage from './PatientExercisesPage';
import AddExercisePage from './AddExercisePage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/kine" element={<KinePage />} />
        <Route path="/patient" element={<PatientPage />} />
        <Route path="/patient/:patientId/exercises" element={<PatientExercisesPage />} />
        <Route path="/kine/add-exercise" element={<AddExercisePage />} />
      </Routes>
    </Router>
  );
};

export default App;

