import { useEffect, useState } from "react";

interface Inmate {
  pin: string;
  photo_filename: string;
  status: string;
  crime: string;
  upload_date: string;
}

import { BACKEND_URL } from '../../config';

export default function MonthlyTarget() {
  const [inmate, setInmate] = useState<Inmate | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const pin = localStorage.getItem("pin") || "";
    if (!pin) {
      setError("No se ha seleccionado un PIN.");
      setLoading(false);
      return;
    }
    fetch(`${BACKEND_URL}/inmates/${pin}`)
      .then((res) => {
        if (!res.ok) throw new Error("No se encontró información del PPL para este PIN.");
        return res.json();
      })
      .then((data) => {
        setInmate(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="rounded-2xl border border-gray-200 bg-gray-50 dark:border-gray-800 dark:bg-gray-900">
      <div className="px-5 pt-5 shadow-default rounded-2xl pb-11 bg-gray-50 dark:bg-gray-900 sm:px-6 sm:pt-6">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90 mb-4">PPL Asociado al PIN</h3>
        {loading ? (
          <div className="text-center py-10 text-gray-500">Cargando información...</div>
        ) : error ? (
          <div className="text-center py-10 text-red-500">{error}</div>
        ) : inmate ? (
          <div className="flex flex-col items-center gap-4">
            {/*
              Flujo de integración de la foto de PPL:
              1. El backend sirve imágenes desde /photos/{pin}.jpg usando StaticFiles.
              2. Esta URL se construye con BACKEND_URL y el pin.
              3. Si la imagen no existe, se muestra un placeholder.
              4. En producción, actualizar este flujo para consumir imágenes de una API o tabla externa.
            */}
            <img
              src={`${BACKEND_URL}/photos/${inmate.pin}.jpg`}
              alt={`Foto PPL ${inmate.pin}`}
              className="rounded-xl shadow-md object-cover w-40 h-40 border border-gray-300 dark:border-gray-700 bg-gray-900"
              style={{ width: 160, height: 160, maxWidth: 180, maxHeight: 180 }}
              onError={e => {
                (e.target as HTMLImageElement).src = '/placeholder-user.svg';
              }}
            />
            <div className="w-full flex flex-col items-center">
              <div className="text-xl font-bold text-gray-800 dark:text-white">PIN: {inmate.pin}</div>
              <div className="text-base text-gray-700 dark:text-gray-300 mt-2">
                <span className="font-semibold">Estatus:</span> {inmate.status}
              </div>
              <div className="text-base text-gray-700 dark:text-gray-300 mt-1">
                <span className="font-semibold">Delito:</span> {inmate.crime}
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
