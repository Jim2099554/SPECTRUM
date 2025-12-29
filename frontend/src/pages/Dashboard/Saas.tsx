import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Saas() {
  const navigate = useNavigate();
  useEffect(() => {
    navigate("/dashboard/usuarios", { replace: true });
  }, [navigate]);
  return null;
}
