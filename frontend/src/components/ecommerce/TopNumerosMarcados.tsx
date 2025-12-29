import { useEffect, useState } from "react";

interface Llamada {
  id: number;
  fecha: string;
  hora: string;
  telefono: string;
  resumen: string;
  pdf_url: string | null;
  audio_url: string | null;
}

import { BACKEND_URL } from '../../config';

export default function TopNumerosMarcados() {
  const [llamadas, setLlamadas] = useState<Llamada[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const pin = typeof window !== "undefined" ? localStorage.getItem("pin") || "" : "";

  useEffect(() => {
    setLoading(true);
    setError("");
    if (!pin) {
      setError("No se ha seleccionado un PIN.");
      setLoading(false);
      return;
    }
    fetch(`${BACKEND_URL}/llamadas?pin=${pin}`)
      .then(res => {
        if (!res.ok) throw new Error("No se pudieron obtener las llamadas");
        return res.json();
      })
      .then(data => {
        setLlamadas(data.llamadas || []);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [pin]);

  // Agrupar y contar por teléfono
  const conteo: Record<string, number> = {};
  llamadas.forEach((llamada) => {
    if (llamada.telefono) {
      conteo[llamada.telefono] = (conteo[llamada.telefono] || 0) + 1;
    }
  });
  const top10 = Object.entries(conteo)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-5 pt-5 pb-4 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6 sm:pt-6 mt-6">
      <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90 mb-2">
        Top 10 Números Más Marcados
      </h3>
      {loading ? (
        <div className="text-center py-8 text-gray-400">Cargando...</div>
      ) : error ? (
        <div className="text-center py-8 text-red-500">{error}</div>
      ) : top10.length === 0 ? (
        <div className="text-center py-8 text-gray-400">No hay llamadas registradas.</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr>
                <th className="py-2 px-3 font-medium text-gray-500 dark:text-gray-400">#</th>
                <th className="py-2 px-3 font-medium text-gray-500 dark:text-gray-400">Número</th>
                <th className="py-2 px-3 font-medium text-gray-500 dark:text-gray-400">Llamadas</th>
              </tr>
            </thead>
            <tbody>
              {top10.map(([telefono, cantidad], idx) => (
                <tr key={telefono} className="border-t border-gray-100 dark:border-gray-800">
                  <td className="py-2 px-3 text-white">{idx + 1}</td>
                  <td className="py-2 px-3 font-mono text-white">{telefono}</td>
                  <td className="py-2 px-3 font-bold text-white">{cantidad}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
