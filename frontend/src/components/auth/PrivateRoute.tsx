import React from "react";
import { Navigate, Outlet } from "react-router-dom";

// Puedes ajustar esta función según cómo guardes el token/sesión
function isAuthenticated() {
  // Ahora revisa si existe 'access_token' en localStorage
  return Boolean(localStorage.getItem("access_token"));
}

const PrivateRoute: React.FC = () => {
  return isAuthenticated() ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute;
