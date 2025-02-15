import React from "react";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="d-flex justify-content-center align-items-center vh-100" style={{ backgroundColor: "#F3E5F5" }}>
      <div className="p-5 bg-white rounded shadow text-center" style={{ maxWidth: "400px", width: "100%" }}>
        <h1 className="mb-4" style={{ color: "#4B0082" }}>Bienvenue sur MediCall</h1>
        <button
          className="btn btn-lg w-100 mb-3"
          style={{ backgroundColor: "#D8BFD8", color: "#4B0082" }}
          onClick={() => navigate("/kine")}
        >
          Je suis Kiné
        </button>
        <button
          className="btn btn-lg w-100"
          style={{ backgroundColor: "#E6E6FA", color: "#4B0082" }}
          onClick={() => navigate("/patient")}
        >
          Je suis Patient
        </button>
      </div>
    </div>
  );
};

export default HomePage;
