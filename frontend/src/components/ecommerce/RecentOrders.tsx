import {
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from "../ui/table";

import { useEffect, useState } from "react";

// Define the TypeScript interface para una transcripción
interface Transcripcion {
  id: number;
  fecha: string;
  hora: string;
  telefono: string;
  resumen: string;
  pdf_url: string | null;
  audio_url: string | null;
  // Nuevos campos para IA/inteligencia (simulados por ahora)
  palabras_clave?: string[];
  resumen_automatico?: string;
  emocion?: string;
  nota_analista?: string;
  idioma?: string; // Nuevo campo para idioma detectado
}

import { BACKEND_URL } from '../../config';

function extractContacto(resumen: string): string {
  // Busca "Receptor: <nombre> (<telefono>)" en el resumen
  const match = resumen.match(/Receptor: ([^\(\)]+) \(/);
  if (match) return match[1].trim();
  // Fallback: si no encuentra, devuelve string vacío
  return "";
}

export default function RecentOrders() {
  const [transcripciones, setTranscripciones] = useState<Transcripcion[]>([]);
  // Estado local para edición de notas del analista
  const [notas, setNotas] = useState<{[id:number]: string}>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
      .then(async data => {
        const transcripciones = data.llamadas || [];
        // Llamar al endpoint de análisis IA
        const iaRes = await fetch(`${BACKEND_URL}/analyze/transcription`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            transcripciones: transcripciones.map((tx: Transcripcion) => ({
              id: tx.id,
              texto: tx.resumen
            }))
          })
        });
        let enriquecidas = transcripciones;
        if (iaRes.ok) {
          const iaData = await iaRes.json();
          enriquecidas = transcripciones.map((tx: Transcripcion) => {
            const ia = (iaData.resultados || []).find((r: any) => r.id === tx.id) || {};
            return { ...tx, ...ia };
          });
        }
        setTranscripciones(enriquecidas);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);


  // Manejo de edición inline de notas del analista
  const handleNotaChange = (id: number, value: string) => {
    setNotas(prev => ({ ...prev, [id]: value }));
    setTranscripciones(prev => prev.map(tx => tx.id === id ? { ...tx, nota_analista: value } : tx));
  };

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-4 pb-3 pt-4 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6">
      <div className="flex flex-col gap-2 mb-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Listado de llamadas
          </h3>
        </div>
      </div>
      <div className="max-w-full overflow-x-auto">
        {loading ? (
          <div className="text-center py-8 text-gray-500">Cargando transcripciones...</div>
        ) : error ? (
          <div className="text-center py-8 text-red-500">{error}</div>
        ) : transcripciones.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No hay transcripciones registradas para este PIN.</div>
        ) : (
          <Table>
            <TableHeader className="border-gray-100 dark:border-gray-800 border-y">
              <TableRow>
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Fecha de llamada</TableCell>
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Nombre/contacto</TableCell>
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Número marcado</TableCell>
                
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Idioma</TableCell>
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Palabras clave</TableCell>
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Resumen automático</TableCell>
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Emoción/Tono</TableCell>
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Notas del analista</TableCell>
                <TableCell isHeader className="py-3 font-medium text-gray-500 text-center text-theme-xs dark:text-gray-400">Audio/PDF</TableCell>
              </TableRow>
            </TableHeader>
            <TableBody className="divide-y divide-gray-100 dark:divide-gray-800">
              {transcripciones.map((tx) => (
                <TableRow key={tx.id} className="">
                  <TableCell className="py-3 text-gray-800 dark:text-white/90">{tx.fecha} {tx.hora}</TableCell>
                  <TableCell className="py-3 text-gray-500 dark:text-gray-400">{extractContacto(tx.resumen) || '-'}</TableCell>
                  <TableCell className="py-3 text-gray-500 dark:text-gray-400">{tx.telefono}</TableCell>
                  
                  <TableCell className="py-3 text-gray-500 dark:text-gray-400">
                    {tx.idioma ? (
                      <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded dark:bg-blue-900 dark:text-blue-200">
                        {tx.idioma.toUpperCase()}
                      </span>
                    ) : <span className="text-xs text-gray-400">-</span>}
                  </TableCell>
                  <TableCell className="py-3 text-gray-500 dark:text-gray-400">
                    {(tx.palabras_clave && tx.palabras_clave.length > 0)
                      ? tx.palabras_clave.map((kw, i) => (
                        <span key={i} className="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-0.5 rounded mr-1 mb-1 dark:bg-yellow-900 dark:text-yellow-200">{kw}</span>
                      ))
                      : <span className="text-xs text-gray-400">-</span>}
                  </TableCell>
                  <TableCell className="py-3 text-gray-500 dark:text-gray-400">{tx.resumen_automatico || <span className="text-xs text-gray-400">-</span>}</TableCell>
                  <TableCell className="py-3 text-gray-500 dark:text-gray-400">
                    {tx.emocion ? (
                      <span className={
                        tx.emocion === "Tensa" ? "text-red-600 font-bold" :
                        tx.emocion === "Alegre" ? "text-green-600 font-bold" :
                        tx.emocion === "Amenazante" ? "text-orange-600 font-bold" :
                        "text-gray-600"
                      }>
                        {tx.emocion}
                      </span>
                    ) : <span className="text-xs text-gray-400">-</span>}
                  </TableCell>
                  <TableCell className="py-3 text-gray-500 dark:text-gray-400">
                    <input
                      type="text"
                      className="w-full px-2 py-1 border rounded text-sm bg-white dark:bg-gray-800 dark:text-gray-100 border-gray-300 dark:border-gray-700"
                      placeholder="Agregar nota..."
                      value={notas[tx.id] ?? tx.nota_analista ?? ""}
                      onChange={e => handleNotaChange(tx.id, e.target.value)}
                    />
                  </TableCell>
                  <TableCell className="py-3 text-gray-500 dark:text-gray-400">
                    {tx.audio_url ? <a href={tx.audio_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline mr-2">Audio</a> : null}
                    {tx.pdf_url ? <a href={tx.pdf_url} target="_blank" rel="noopener noreferrer" className="text-green-600 underline">PDF</a> : null}
                    {!tx.audio_url && !tx.pdf_url ? <span className="text-xs text-gray-400">N/A</span> : null}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
