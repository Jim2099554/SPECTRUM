import { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

interface Llamada {
  id: number;
  fecha: string;
  hora: string; // formato "HH:MM"
  telefono: string;
  resumen: string;
  pdf_url: string | null;
  audio_url: string | null;
}

import { BACKEND_URL } from '../../config';

export default function LlamadasPorHoraChart() {
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

  // Procesar llamadas por hora
  const llamadasPorHora = Array(24).fill(0);
  llamadas.forEach((llamada) => {
    if (llamada.hora) {
      const hora = parseInt(llamada.hora.split(":")[0], 10);
      if (!isNaN(hora) && hora >= 0 && hora <= 23) {
        llamadasPorHora[hora] += 1;
      }
    }
  });

  const options: ApexOptions = {
    chart: {
      type: "bar",
      height: 260,
      fontFamily: "Outfit, sans-serif",
      toolbar: { show: false },
    },
    plotOptions: {
      bar: {
        columnWidth: "55%",
        borderRadius: 4,
        borderRadiusApplication: "end",
      },
    },
    dataLabels: { enabled: false },
    xaxis: {
      categories: Array.from({ length: 24 }, (_, i) => `${i}:00`),
      title: { text: "Hora del día" },
      labels: { rotate: -45 },
    },
    yaxis: {
      title: { text: "Llamadas" },
    },
    fill: { opacity: 1 },
    grid: { yaxis: { lines: { show: true } } },
    tooltip: {
      y: { formatter: (val: number) => `${val} llamadas` },
    },
  };

  const series = [
    {
      name: "Llamadas",
      data: llamadasPorHora,
    },
  ];

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-5 pt-5 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6 sm:pt-6 mt-6">
      <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90 mb-2">
        Histograma de Horas de Llamadas
      </h3>
      {loading ? (
        <div className="text-center py-8 text-gray-400">Cargando...</div>
      ) : error ? (
        <div className="text-center py-8 text-red-500">{error}</div>
      ) : (
        <Chart options={options} series={series} type="bar" height={260} />
      )}
    </div>
  );
}
