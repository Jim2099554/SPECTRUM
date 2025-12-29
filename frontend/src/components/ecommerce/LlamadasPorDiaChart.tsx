import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

import { useState, useEffect } from "react";

interface CallData {
  fecha: string;
  llamadas: number;
}

export default function LlamadasPorDiaChart() {
  const [data, setData] = useState<CallData[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const pin = typeof window !== "undefined" ? localStorage.getItem("pin") || "" : "";

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(`/llamadas-por-dia?pin=${pin}`)
      .then((res) => {
        if (!res.ok) throw new Error("No se pudo obtener los datos de llamadas");
        return res.json();
      })
      .then((json) => setData(json))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [pin]);

  const options: ApexOptions = {
    colors: ["#465fff"],
    chart: {
      fontFamily: "Outfit, sans-serif",
      type: "bar",
      height: 180,
      toolbar: { show: false },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "39%",
        borderRadius: 5,
        borderRadiusApplication: "end",
      },
    },
    dataLabels: { enabled: false },
    stroke: { show: true, width: 4, colors: ["transparent"] },
    xaxis: {
      categories: data.map((item) => item.fecha),
      axisBorder: { show: false },
      axisTicks: { show: false },
      title: { text: "Fecha" },
    },
    legend: {
      show: true,
      position: "top",
      horizontalAlign: "left",
      fontFamily: "Outfit",
    },
    yaxis: {
      title: { text: "Llamadas" },
    },
    grid: {
      yaxis: { lines: { show: true } },
    },
    fill: { opacity: 1 },
    tooltip: {
      x: { show: true },
      y: { formatter: (val: number) => `${val} llamadas` },
    },
  };

  const series = [
    {
      name: "Llamadas",
      data: data.map((item) => item.llamadas),
    },
  ];

  

  // Cálculos de métricas
  let totalLlamadas = 0;
  let promedioDiario = 0;
  let diaPico = { fecha: '', llamadas: 0 };
  let diasSinLlamadas = 0;

  if (!loading && !error && data.length > 0) {
    totalLlamadas = data.reduce((acc, curr) => acc + curr.llamadas, 0);
    promedioDiario = totalLlamadas / data.length;
    diaPico = data.reduce((max, curr) => curr.llamadas > max.llamadas ? curr : max, data[0]);
    diasSinLlamadas = data.filter((item) => item.llamadas === 0).length;
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-5 pt-5 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6 sm:pt-6">
      {/* Tarjetas de resumen */}
      {!loading && !error && data.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="rounded-lg bg-blue-50 dark:bg-blue-900/30 p-4 text-center">
            <div className="text-xs text-blue-800 dark:text-blue-200 font-medium mb-1">Total llamadas</div>
            <div className="text-2xl font-bold text-blue-900 dark:text-blue-100">{totalLlamadas}</div>
          </div>
          <div className="rounded-lg bg-green-50 dark:bg-green-900/30 p-4 text-center">
            <div className="text-xs text-green-800 dark:text-green-200 font-medium mb-1">Promedio diario</div>
            <div className="text-2xl font-bold text-green-900 dark:text-green-100">{promedioDiario.toFixed(1)}</div>
          </div>
          <div className="rounded-lg bg-yellow-50 dark:bg-yellow-900/30 p-4 text-center">
            <div className="text-xs text-yellow-800 dark:text-yellow-200 font-medium mb-1">Día pico</div>
            <div className="text-lg font-bold text-yellow-900 dark:text-yellow-100">{diaPico.fecha}</div>
            <div className="text-base text-yellow-700 dark:text-yellow-200">({diaPico.llamadas} llamadas)</div>
          </div>
          <div className="rounded-lg bg-gray-50 dark:bg-gray-900/30 p-4 text-center">
            <div className="text-xs text-gray-800 dark:text-gray-200 font-medium mb-1">Días sin llamadas</div>
            <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">{diasSinLlamadas}</div>
          </div>
        </div>
      )}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
          Llamadas por Día
        </h3>

      </div>
      <div className="max-w-full overflow-x-auto custom-scrollbar">
        <div className="-ml-5 min-w-[650px] xl:min-w-full pl-2">
          {loading ? (
            <div className="text-center py-8 text-gray-400">Cargando...</div>
          ) : error ? (
            <div className="text-center py-8 text-red-500">{error}</div>
          ) : (
            <Chart options={options} series={series} type="bar" height={180} />
          )}
        </div>
      </div>
    </div>
  );
}

