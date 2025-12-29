import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

interface CallFlowChartProps {
  pin: string;
}

interface CallData {
  date: string;
  count: number;
}

const CallFlowChart: React.FC<CallFlowChartProps> = ({ pin }) => {
  const [data, setData] = useState<CallData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch(`/llamadas-por-dia?pin=${pin}`)
      .then((res) => {
        if (!res.ok) throw new Error("Error al obtener datos de llamadas");
        return res.json();
      })
      .then((json) => {
        setData(json);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [pin]);

  const options: ApexOptions = {
    chart: {
      id: "call-flow-chart",
      type: "line",
      fontFamily: "Outfit, sans-serif",
      height: 310,
      toolbar: { show: false },
    },
    colors: ["#00BFFF"],
    stroke: { curve: "smooth", width: 3 },
    xaxis: {
      categories: data.map((item) => item.date),
      title: { text: "Fecha" },
      labels: { rotate: -45 },
    },
    yaxis: {
      title: { text: "Llamadas" },
      labels: { style: { fontSize: "12px" } },
    },
    dataLabels: { enabled: false },
    tooltip: { enabled: true },
    grid: { yaxis: { lines: { show: true } } },
  };

  const series = [
    {
      name: "Llamadas",
      data: data.map((item) => item.count),
    },
  ];

  return (
    <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold mb-2">Flujo de llamadas diarias</h3>
      {loading ? (
        <div>Cargando...</div>
      ) : error ? (
        <div className="text-red-500">{error}</div>
      ) : (
        <Chart options={options} series={series} type="line" height={310} />
      )}
    </div>
  );
};

export default CallFlowChart;
