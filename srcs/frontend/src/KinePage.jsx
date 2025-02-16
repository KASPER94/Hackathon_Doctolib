// // import React, { useState } from 'react';
// // import { useNavigate } from 'react-router-dom';
// // import "bootstrap/dist/css/bootstrap.min.css";

// // const KinePage = () => {
// //   const [exercises, setExercises] = useState([
// //     { id: 1, name: 'Exercice 1', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_1' },
// //     { id: 2, name: 'Exercice 2', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_2' },
// //   ]);

// //   const [patients, setPatients] = useState([
// //     { id: 1, name: 'X Æ A-12 Musk' },
// //     { id: 2, name: 'South West' },
// //   ]);

// //   const [showModal, setShowModal] = useState(false);
// //   const [showAddExerciseModal, setShowAddExerciseModal] = useState(false);
// //   const [videoFile, setVideoFile] = useState(null);
// //   const [exerciseName, setExerciseName] = useState('');
// //   const navigate = useNavigate();

// //   const handleFileChange = (event) => {
// //     setVideoFile(event.target.files[0]);
// //   };

// //   const handleNameChange = (event) => {
// //     setExerciseName(event.target.value);
// //   };

// //   const handleAddExercise = (event) => {
// //     event.preventDefault();
// //     // Logique pour uploader la vidéo et ajouter l'exercice
// //     console.log('Video file:', videoFile);
// //     console.log('Exercise name:', exerciseName);
// //     const newExercise = { id: exercises.length + 1, name: exerciseName, videoUrl: URL.createObjectURL(videoFile) };
// //     setExercises([...exercises, newExercise]);
// //     setShowAddExerciseModal(false);
// //     setExerciseName('');
// //     setVideoFile(null);
// //   };

// //   const handleShowModal = () => {
// //     setShowModal(true);
// //   };

// //   const handleShowAddExerciseModal = () => {
// //     setShowAddExerciseModal(true);
// //   };

// //   const closeModal = () => {
// //     setShowModal(false);
// //     setShowAddExerciseModal(false);
// //   };

// //   const goToPatientExercises = (patientId) => {
// //     navigate(`/patient/${patientId}/exercises`);
// //   };

// //   const handlePatientClick = (patient) => {
// //     if (patient.name === "South West") {
// //       handleShowModal();
// //     } else {
// //       goToPatientExercises(patient.id);
// //     }
// //   };

// //   return (
// //     <div className="container-fluid d-flex flex-column align-items-center justify-content-center" style={{ backgroundColor: "#F3E5F5", minHeight: "100vh" }}>
// //       <div className="p-4 bg-white rounded shadow w-100 text-center" style={{ maxWidth: "800px" }}>
// //         <h1 className="mb-3" style={{ color: "#4B0082" }}>Your Exercises:</h1>
// //         <div className="d-flex flex-wrap justify-content-center mb-3">
// //           {exercises.map((exercise) => (
// //             <div key={exercise.id} className="m-2">
// //               <div className="embed-responsive embed-responsive-16by9" style={{ width: "300px" }}>
// //                 <iframe
// //                   className="embed-responsive-item"
// //                   src={exercise.videoUrl}
// //                   allowFullScreen
// //                   title={`Exercice Video ${exercise.id}`}
// //                 ></iframe>
// //               </div>
// //               <p className="text-center mt-2 mb-2" style={{ color: "#4B0082" }}>{exercise.name}</p>
// //             </div>
// //           ))}
// //         </div>
// //         <button
// //           className="btn btn-lg w-100"
// //           style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
// //           onClick={handleShowAddExerciseModal}
// //         >
// //           Add an exercise
// //         </button>

// //         <h1 className="mt-5 mb-3" style={{ color: "#4B0082" }}>Your patients:</h1>
// //         <div className="d-flex flex-wrap justify-content-center">
// //           {patients.map((patient) => (
// //             <div key={patient.id} className="m-2">
// //               <button
// //                 className="btn btn-lg px-3"
// //                 style={{ backgroundColor: "#D8BFD8", color: "#4B0082", whiteSpace: "nowrap" }}
// //                 onClick={() => handlePatientClick(patient)}
// //               >
// //                 {patient.name}
// //               </button>
// //             </div>
// //           ))}
// //         </div>
// //         <button
// //           className="btn btn-lg w-100 mt-2"
// //           style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
// //           onClick={handleShowModal}
// //         >
// //           Add a patient
// //         </button>
// //       </div>

// //       {showAddExerciseModal && (
// //         <div className="modal fade show d-block" tabIndex="-1" role="dialog">
// //           <div className="modal-dialog modal-dialog-centered" role="document">
// //             <div className="modal-content text-center" style={{ backgroundColor: "#E6E6FA", color: "#4B0082", borderRadius: "15px" }}>
// //               <div className="modal-body p-4">
// //                 <h1 className="mb-4" style={{ color: "#4B0082" }}>Add an exercise</h1>
// //                 <form onSubmit={handleAddExercise}>
// //                   <div className="mb-3">
// //                     <label htmlFor="exerciseName" className="form-label" style={{ color: "#4B0082" }}>Name of the exercise:</label>
// //                     <input
// //                       type="text"
// //                       className="form-control"
// //                       id="exerciseName"
// //                       value={exerciseName}
// //                       onChange={handleNameChange}
// //                       required
// //                     />
// //                   </div>
// //                   <div className="mb-3">
// //                     <label htmlFor="videoFile" className="form-label" style={{ color: "#4B0082" }}>Video of the exercise:</label>
// //                     <input
// //                       type="file"
// //                       className="form-control"
// //                       id="videoFile"
// //                       onChange={handleFileChange}
// //                       required
// //                     />
// //                   </div>
// //                   <button type="submit" className="btn btn-lg w-100" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }}>
// //                     Add the exercise
// //                   </button>
// //                 </form>
// //               </div>
// //               <div className="modal-footer border-0">
// //                 <button className="btn btn-lg" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }} onClick={closeModal}>
// //                   Close
// //                 </button>
// //               </div>
// //             </div>
// //           </div>
// //         </div>
// //       )}

// //       {showModal && (
// //         <div className="modal fade show d-block" tabIndex="-1" role="dialog">
// //           <div className="modal-dialog modal-dialog-centered" role="document">
// //             <div className="modal-content text-center" style={{ backgroundColor: "#E6E6FA", color: "#4B0082", borderRadius: "15px" }}>
// //               <div className="modal-body d-flex flex-column justify-content-center" style={{ minHeight: "200px" }}>
// //                 <p className="fs-4 fw-bold">This is a demo version, this feature is not yet available.</p>
// //               </div>
// //               <div className="modal-footer border-0">
// //                 <button className="btn btn-lg" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }} onClick={closeModal}>
// //                   Close
// //                 </button>
// //               </div>
// //             </div>
// //           </div>
// //         </div>
// //       )}

// //       {(showModal || showAddExerciseModal) && <div className="modal-backdrop fade show" onClick={closeModal}></div>}
// //     </div>
// //   );
// // };

// // export default KinePage;

// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import "bootstrap/dist/css/bootstrap.min.css";

// const KinePage = () => {
//   const [exercises, setExercises] = useState([
//     { id: 1, name: 'Exercice 1', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_1' },
//     { id: 2, name: 'Exercice 2', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_2' },
//   ]);

//   const [patients, setPatients] = useState([
//     { id: 1, name: 'X Æ A-12 Musk' },
//     { id: 2, name: 'South West' },
//   ]);

//   const [showModal, setShowModal] = useState(false);
//   const [showAddExerciseModal, setShowAddExerciseModal] = useState(false);
//   const [videoFile, setVideoFile] = useState(null);
//   const [documentFile, setDocumentFile] = useState(null);
//   const [exerciseName, setExerciseName] = useState('');
//   const navigate = useNavigate();

//   const handleFileChange = (event) => {
//     setVideoFile(event.target.files[0]);
//   };

//   const handleDocumentChange = (event) => {
//     setDocumentFile(event.target.files[0]);
//   };

//   const handleNameChange = (event) => {
//     setExerciseName(event.target.value);
//   };

//   const handleAddExercise = async (event) => {
//     event.preventDefault();
//     const formData = new FormData();
//     formData.append('video', videoFile);
//     if (documentFile) {
//       formData.append('document', documentFile);
//     }

//     try {
//       const response = await fetch('http://localhost:8000/upload/', {
//         method: 'POST',
//         body: formData,
//       });

//       if (!response.ok) {
//         const errorData = await response.json();
//         throw new Error(errorData.detail);
//       }

//       const result = await response.json();
//       console.log('Upload successful:', result);

//       // Update the exercise list
//       const newExercise = { id: exercises.length + 1, name: exerciseName, videoUrl: `http://localhost:8000/videos/${result.id}/download` };
//       setExercises([...exercises, newExercise]);
//       setShowAddExerciseModal(false);
//       setExerciseName('');
//       setVideoFile(null);
//       setDocumentFile(null);
//     } catch (error) {
//       console.error('Error uploading video:', error);
//     }
//   };

//   const handleShowAddExerciseModal = () => {
//     setShowAddExerciseModal(true);
//   };

//   const closeModal = () => {
//     setShowModal(false);
//     setShowAddExerciseModal(false);
//   };

//   const goToPatientExercises = (patientId) => {
//     navigate(`/patient/${patientId}/exercises`);
//   };

//   const handlePatientClick = (patient) => {
//     if (patient.name === "South West") {
//       setShowModal(true);
//     } else {
//       goToPatientExercises(patient.id);
//     }
//   };

//   return (
//     <div className="container-fluid d-flex flex-column align-items-center justify-content-center" style={{ backgroundColor: "#F3E5F5", minHeight: "100vh" }}>
//       <div className="p-4 bg-white rounded shadow w-100 text-center" style={{ maxWidth: "800px" }}>
//         <h1 className="mb-3" style={{ color: "#4B0082" }}>Your Exercises:</h1>
//         <div className="d-flex flex-wrap justify-content-center mb-3">
//           {exercises.map((exercise) => (
//             <div key={exercise.id} className="m-2">
//               <div className="embed-responsive embed-responsive-16by9" style={{ width: "300px" }}>
//                 <iframe
//                   className="embed-responsive-item"
//                   src={exercise.videoUrl}
//                   allowFullScreen
//                   title={`Exercice Video ${exercise.id}`}
//                 ></iframe>
//               </div>
//               <p className="text-center mt-2 mb-2" style={{ color: "#4B0082" }}>{exercise.name}</p>
//             </div>
//           ))}
//         </div>
//         <button
//           className="btn btn-lg w-100"
//           style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
//           onClick={handleShowAddExerciseModal}
//         >
//           Add an exercise
//         </button>

//         <h1 className="mt-5 mb-3" style={{ color: "#4B0082" }}>Your patients:</h1>
//         <div className="d-flex flex-wrap justify-content-center">
//           {patients.map((patient) => (
//             <div key={patient.id} className="m-2">
//               <button
//                 className="btn btn-lg px-3"
//                 style={{ backgroundColor: "#D8BFD8", color: "#4B0082", whiteSpace: "nowrap" }}
//                 onClick={() => handlePatientClick(patient)}
//               >
//                 {patient.name}
//               </button>
//             </div>
//           ))}
//         </div>
//         <button
//           className="btn btn-lg w-100 mt-2"
//           style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
//           onClick={() => setShowModal(true)}
//         >
//           Add a patient
//         </button>
//       </div>

//       {showAddExerciseModal && (
//         <div className="modal fade show d-block" tabIndex="-1" role="dialog">
//           <div className="modal-dialog modal-dialog-centered" role="document">
//             <div className="modal-content text-center" style={{ backgroundColor: "#E6E6FA", color: "#4B0082", borderRadius: "15px" }}>
//               <div className="modal-body p-4">
//                 <h1 className="mb-4" style={{ color: "#4B0082" }}>Add an exercise</h1>
//                 <form onSubmit={handleAddExercise}>
//                   <div className="mb-3">
//                     <label htmlFor="exerciseName" className="form-label" style={{ color: "#4B0082" }}>Name of the exercise:</label>
//                     <input
//                       type="text"
//                       className="form-control"
//                       id="exerciseName"
//                       value={exerciseName}
//                       onChange={handleNameChange}
//                       required
//                     />
//                   </div>
//                   <div className="mb-3">
//                     <label htmlFor="videoFile" className="form-label" style={{ color: "#4B0082" }}>Video of the exercise:</label>
//                     <input
//                       type="file"
//                       className="form-control"
//                       id="videoFile"
//                       onChange={handleFileChange}
//                       accept=".mp4,.mov"
//                       required
//                     />
//                   </div>
//                   <div className="mb-3">
//                     <label htmlFor="documentFile" className="form-label" style={{ color: "#4B0082" }}>Document (optional):</label>
//                     <input
//                       type="file"
//                       className="form-control"
//                       id="documentFile"
//                       onChange={handleDocumentChange}
//                       accept=".pdf,.doc,.docx"
//                     />
//                   </div>
//                   <button type="submit" className="btn btn-lg w-100" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }}>
//                     Add the exercise
//                   </button>
//                 </form>
//               </div>
//               <div className="modal-footer border-0">
//                 <button className="btn btn-lg" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }} onClick={closeModal}>
//                   Close
//                 </button>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}

//       {showModal && (
//         <div className="modal fade show d-block" tabIndex="-1" role="dialog">
//           <div className="modal-dialog modal-dialog-centered" role="document">
//             <div className="modal-content text-center" style={{ backgroundColor: "#E6E6FA", color: "#4B0082", borderRadius: "15px" }}>
//               <div className="modal-body d-flex flex-column justify-content-center" style={{ minHeight: "200px" }}>
//                 <p className="fs-4 fw-bold">This is a demo version, this feature is not yet available.</p>
//               </div>
//               <div className="modal-footer border-0">
//                 <button className="btn btn-lg" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }} onClick={closeModal}>
//                   Close
//                 </button>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}

//       {(showModal || showAddExerciseModal) && <div className="modal-backdrop fade show" onClick={closeModal}></div>}
//     </div>
//   );
// };

// export default KinePage;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";

const KinePage = () => {
  const [exercises, setExercises] = useState([
    { id: 1, name: 'Exercice 1', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_1' },
    { id: 2, name: 'Exercice 2', videoUrl: 'https://www.youtube.com/embed/VIDEO_ID_2' },
  ]);

  const [patients, setPatients] = useState([
    { id: 1, name: 'X Æ A-12 Musk' },
    { id: 2, name: 'South West' },
  ]);

  const [showModal, setShowModal] = useState(false);
  const [showAddExerciseModal, setShowAddExerciseModal] = useState(false);
  const [videoFile, setVideoFile] = useState(null);
  const [documentFile, setDocumentFile] = useState(null);
  const [exerciseName, setExerciseName] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setVideoFile(event.target.files[0]);
  };

  const handleDocumentChange = (event) => {
    setDocumentFile(event.target.files[0]);
  };

  const handleNameChange = (event) => {
    setExerciseName(event.target.value);
  };

  const handleAddExercise = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('exercise_name', exerciseName);

    try {
      const response = await fetch('http://localhost:8000/upload/', {
        method: 'POST',
        body: formData,
      });
      console.log("ICI")

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }

      const result = await response.json();
      console.log('Upload successful:', result);

      // Update the exercise list
      // const newExercise = { id: exercises.length + 1, name: exerciseName, videoUrl: `http://localhost:8000/videos/${result.video_id}/download` };
      const newExercise = {
        id: result.video_id,
        name: exerciseName,
        videoUrl: `http://localhost:8000/videos/${result.video_id}`
    };
      setExercises([...exercises, newExercise]);
      setShowAddExerciseModal(false);
      setExerciseName('');
      setVideoFile(null);
      setDocumentFile(null);
    } catch (error) {
      console.error('Error uploading video:', error);
      alert('Error uploading video');
    }
  };

  const handleShowAddExerciseModal = () => {
    setShowAddExerciseModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setShowAddExerciseModal(false);
  };

  const goToPatientExercises = (patientId) => {
    navigate(`/patient/${patientId}/exercises`);
  };

  const handlePatientClick = (patient) => {
    if (patient.name === "South West") {
      setShowModal(true);
    } else {
      goToPatientExercises(patient.id);
    }
  };

  return (
    <div className="container-fluid d-flex flex-column align-items-center justify-content-center" style={{ backgroundColor: "#F3E5F5", minHeight: "100vh" }}>
      <div className="p-4 bg-white rounded shadow w-100 text-center" style={{ maxWidth: "800px" }}>
        <h1 className="mb-3" style={{ color: "#4B0082" }}>Your Exercises:</h1>
        <div className="d-flex flex-wrap justify-content-center mb-3">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="m-2">
              <div className="embed-responsive embed-responsive-16by9" style={{ width: "300px" }}>
                <iframe
                  className="embed-responsive-item"
                  src={exercise.videoUrl}
                  allowFullScreen
                  title={`Exercise Video ${exercise.id}`}
                ></iframe>
              </div>
              <p className="text-center mt-2 mb-2" style={{ color: "#4B0082" }}>{exercise.name}</p>
            </div>
          ))}
        </div>
        <button
          className="btn btn-lg w-100"
          style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
          onClick={handleShowAddExerciseModal}
        >
          Add an exercise
        </button>

        <h1 className="mt-5 mb-3" style={{ color: "#4B0082" }}>Your patients:</h1>
        <div className="d-flex flex-wrap justify-content-center">
          {patients.map((patient) => (
            <div key={patient.id} className="m-2">
              <button
                className="btn btn-lg px-3"
                style={{ backgroundColor: "#D8BFD8", color: "#4B0082", whiteSpace: "nowrap" }}
                onClick={() => handlePatientClick(patient)}
              >
                {patient.name}
              </button>
            </div>
          ))}
        </div>
        <button
          className="btn btn-lg w-100 mt-2"
          style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
          onClick={() => setShowModal(true)}
        >
          Add a patient
        </button>
      </div>

      {showAddExerciseModal && (
        <div className="modal fade show d-block" tabIndex="-1" role="dialog">
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content text-center" style={{ backgroundColor: "#E6E6FA", color: "#4B0082", borderRadius: "15px" }}>
              <div className="modal-body p-4">
                <h1 className="mb-4" style={{ color: "#4B0082" }}>Add an exercise</h1>
                <form onSubmit={handleAddExercise}>
                  <div className="mb-3">
                    <label htmlFor="exerciseName" className="form-label" style={{ color: "#4B0082" }}>Name of the exercise:</label>
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
                    <label htmlFor="videoFile" className="form-label" style={{ color: "#4B0082" }}>Video of the exercise:</label>
                    <input
                      type="file"
                      className="form-control"
                      id="videoFile"
                      onChange={handleFileChange}
                      accept=".mp4,.mov"
                      required
                    />
                  </div>
                  <button type="submit" className="btn btn-lg w-100" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }}>
                    Add the exercise
                  </button>
                </form>
              </div>
              <div className="modal-footer border-0">
                <button className="btn btn-lg" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }} onClick={closeModal}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {showModal && (
        <div className="modal fade show d-block" tabIndex="-1" role="dialog">
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content text-center" style={{ backgroundColor: "#E6E6FA", color: "#4B0082", borderRadius: "15px" }}>
              <div className="modal-body d-flex flex-column justify-content-center" style={{ minHeight: "200px" }}>
                <p className="fs-4 fw-bold">This is a demo version, this feature is not yet available.</p>
              </div>
              <div className="modal-footer border-0">
                <button className="btn btn-lg" style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }} onClick={closeModal}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {(showModal || showAddExerciseModal) && <div className="modal-backdrop fade show" onClick={closeModal}></div>}
    </div>
  );
};

export default KinePage;
