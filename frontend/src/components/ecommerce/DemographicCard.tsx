import { useEffect, useState } from "react";

import CountryMap from "./CountryMap";
import { getLadaInfo } from "../../lada_mx";

interface Transcripcion {
  id: number;
  fecha: string;
  hora: string;
  telefono: string;
  resumen: string;
  pdf_url: string | null;
  audio_url: string | null;
}

import { BACKEND_URL } from '../../config';

export default function DemographicCard() {

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [markers, setMarkers] = useState<any[]>([]);
  // Eliminado transcripciones y setTranscripciones

  useEffect(() => {
    const pin = localStorage.getItem("pin") || "";
    if (!pin) {
      setError("No se ha seleccionado un PIN.");
      setLoading(false);
      return;
    }
    fetch(`${BACKEND_URL}/llamadas?pin=${pin}`)
      .then(res => {
        if (!res.ok) throw new Error("No se pudieron obtener las transcripciones");
        return res.json();
      })
      .then(data => {
        const llamadas: Transcripcion[] = data.llamadas || [];
        // setTranscripciones eliminado; si necesitas usar llamadas, usa una variable local o de estado apropiada.
        // Extraer teléfonos únicos
        const telefonosUnicos = Array.from(new Set(llamadas.map(tx => tx.telefono)));
        // Mapear a ciudades/estados
        const marcadores = telefonosUnicos.map(num => {
          const info = getLadaInfo(num);
          if (info) {
            return {
              latLng: [info.lat, info.lng],
              name: `${info.ciudad}, ${info.estado}`,
              style: { fill: "#465FFF", borderWidth: 1, borderColor: "white" }
            };
          }
          return null;
        }).filter(Boolean);
        setMarkers(marcadores);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] sm:p-6">
      <div className="flex justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Lugares a donde se han realizado llamadas
          </h3>

        </div>

      </div>

      <div className="px-4 py-6 my-6 overflow-hidden border border-gary-200 rounded-2xl dark:border-gray-800 sm:px-6">
        <div
          id="mapOne"
          className="mapOne map-btn -mx-4 -my-6 h-[212px] w-[252px] 2xsm:w-[307px] xsm:w-[358px] sm:-mx-6 md:w-[668px] lg:w-[634px] xl:w-[393px] 2xl:w-[554px]"
        >
          {loading ? (
            <div className="text-center py-8 text-gray-500">Cargando mapa...</div>
          ) : error ? (
            <div className="text-center py-8 text-red-500">{error}</div>
          ) : (
            <CountryMap markers={markers} />
          )}
        </div>
      </div>
    </div>
  );
}

