import { useEffect, useState } from "react";
import PageMeta from "../../components/common/PageMeta";

// Usa variable de entorno si está definida en window, si no, usa localhost:8000
import { BACKEND_URL } from '../../config';

export default function Marketing() {
  const [inmate, setInmate] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const pin = typeof window !== "undefined" ? localStorage.getItem("pin") || "" : "";

  useEffect(() => {
    if (!pin) {
      setError("No se ha seleccionado un PIN.");
      setLoading(false);
      return;
    }
    setLoading(true);
    setError("");
    fetch(`${BACKEND_URL}/inmates/${pin}`)
      .then(res => {
        if (!res.ok) throw new Error("No se pudo obtener la información del PPL");
        return res.json();
      })
      .then(data => {
        setInmate(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [pin]);

  return (
    <>
      <PageMeta
        title="PPL info | SENTINELA"
        description="Información detallada del PPL, carpetas de investigación y delitos."
      />
      <div className="max-w-4xl mx-auto mt-8 p-6 bg-white rounded-2xl border border-gray-200 shadow-md dark:bg-gray-900 dark:border-gray-800">
        <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Información del PPL</h2>
        {loading ? (
          <div className="text-gray-600 dark:text-gray-300">Cargando...</div>
        ) : error ? (
          <div className="text-red-600 dark:text-red-400">{error}</div>
        ) : inmate ? (
          <div className="space-y-6">
            <div className="flex gap-6 items-center">
              <img
                src={`${BACKEND_URL}/photos/${inmate.pin}.jpg`}
                alt={inmate.pin}
                className="w-32 h-32 rounded-xl object-cover border border-gray-300 dark:border-gray-700"
                onError={e => (e.currentTarget.src = "/images/user/user-placeholder.png")}
              />
              <div>
                <div className="font-semibold text-lg text-gray-900 dark:text-white">{inmate.name || inmate.pin}</div>
                <div className="text-gray-500 dark:text-gray-400">PIN: {inmate.pin}</div>
                <div className="text-gray-500 dark:text-gray-400">Estatus: {inmate.status}</div>
                <div className="text-gray-500 dark:text-gray-400">Delito principal: {inmate.crime}</div>
                <div className="text-gray-500 dark:text-gray-400">Fecha de ingreso: {inmate.upload_date ? new Date(inmate.upload_date).toLocaleDateString() : "-"}</div>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">Carpetas de investigación</h3>
              {inmate.investigation_folders && inmate.investigation_folders.length > 0 ? (
                <div className="space-y-4">
                  {inmate.investigation_folders.map((folder: any, idx: number) => (
                    <div key={folder.id || idx} className="border rounded-xl p-4 bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700">
                      <div className="font-semibold text-gray-900 dark:text-white mb-1">Expediente: {folder.folder_number}</div>
                      <div className="text-gray-500 dark:text-gray-400">Centro: {folder.penitentiary_center || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Unidad: {folder.unit || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Tipo: {folder.folder_type || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Apertura: {folder.opened_at ? new Date(folder.opened_at).toLocaleDateString() : "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Lugar: {folder.place || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Hechos: {folder.description || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Participantes: {folder.participants ? JSON.stringify(folder.participants) : "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Evidencias: {folder.evidences ? JSON.stringify(folder.evidences) : "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Entrevistas: {folder.interviews ? JSON.stringify(folder.interviews) : "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Acciones: {folder.actions ? JSON.stringify(folder.actions) : "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Análisis: {folder.analysis || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Conclusiones: {folder.conclusions || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Recomendaciones: {folder.recommendations || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Resolución: {folder.resolution_type || "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Notificaciones: {folder.notifications ? JSON.stringify(folder.notifications) : "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400">Documentos extra: {folder.extra_documents ? JSON.stringify(folder.extra_documents) : "-"}</div>
                      <div className="text-gray-500 dark:text-gray-400 mt-2">
                        <span className="font-semibold">Delitos asociados:</span>
                        {folder.crimes && folder.crimes.length > 0 ? (
                          <ul className="list-disc ml-6 mt-1">
                            {folder.crimes.map((crime: any, cidx: number) => (
                              <li key={crime.id || cidx}>
                                <span className="text-gray-700 dark:text-white font-medium">{crime.crime_name}</span>: {crime.description}
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <span> Sin delitos asociados</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-gray-500 dark:text-gray-400">Sin carpetas de investigación registradas.</div>
              )}
            </div>
          </div>
        ) : null}
      </div>
    </>
  );
}
