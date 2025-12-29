import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const INACTIVITY_LIMIT = 10 * 60 * 1000; // 10 minutos en ms

/**
 * Hook que cierra la sesión tras 10 minutos de inactividad (mouse, teclado, touch).
 * Borra access_token y user_email, muestra alerta y redirige a /login.
 */
export default function useSessionTimeout() {
  const navigate = useNavigate();
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Limpia sesión y redirige
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
    alert('Sesión cerrada por inactividad. Por favor, inicia sesión de nuevo.');
    navigate('/login');
  };

  // Reinicia el temporizador
  const resetTimer = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(logout, INACTIVITY_LIMIT);
  };

  useEffect(() => {
    // Eventos que cuentan como actividad
    const events = ['mousemove', 'keydown', 'mousedown', 'touchstart'];
    events.forEach(event => window.addEventListener(event, resetTimer));
    resetTimer(); // Inicia temporizador al montar
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      events.forEach(event => window.removeEventListener(event, resetTimer));
    };
    // eslint-disable-next-line
  }, []);
}
