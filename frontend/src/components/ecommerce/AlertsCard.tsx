import { useEffect, useState } from "react";
import Badge from "../ui/badge/Badge";
import { GroupIcon } from "../../icons"; // Usar GroupIcon como placeholder si BellIcon no existe

interface Alert {
  id: string;
  message: string;
  severity: "urgente" | "relevante" | "informativa";
  timestamp: string;
  keyword?: string;
}

export default function AlertsCard() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const pin = localStorage.getItem("pin") || "";
    const url = pin ? `/alerts/events/?pin=${encodeURIComponent(pin)}` : "/alerts/events/";
    fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        const raw = await res.text();
        if (!res.ok) {
          console.error("Respuesta no OK:", res.status, raw);
          throw new Error(`HTTP ${res.status}: ${raw}`);
        }
        try {
          const json = JSON.parse(raw);
          return json;
        } catch (e) {
          console.error("Respuesta no es JSON:", raw);
          throw new Error(`Respuesta no es JSON: ${raw}`);
        }
      })
      .then((json) => setAlerts(json.alerts || json))
      .catch((err) => {
        console.error("Error en fetch de alertas:", err);
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, []);

  const severityColor = {
    urgente: "error",
    relevante: "warning",
    informativa: "info",
  } as const;

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] md:p-6 h-64 flex flex-col">
      <div className="flex items-center gap-2 mb-4">
        <GroupIcon className="text-yellow-500 size-6" />
        <span className="text-base font-semibold text-gray-800 dark:text-white/90">
          Alertas importantes
        </span>
      </div>
      <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
        {loading ? (
          <div className="text-gray-400 text-center py-6">Cargando alertas...</div>
        ) : error ? (
          <div className="text-red-500 text-center py-6">{error}</div>
        ) : alerts.length === 0 ? (
          <div className="text-gray-400 text-center py-6">No hay alertas recientes.</div>
        ) : (
          alerts.map((alert) => (
            <div key={alert.id} className="flex items-start gap-3 bg-yellow-50 dark:bg-yellow-900/10 rounded-lg p-2">
              <Badge color={severityColor[alert.severity]}>
                {alert.severity}
              </Badge>
              <div className="flex-1">
                <div className="text-sm text-gray-700 dark:text-gray-200 font-medium">
                  {alert.message}
                  {alert.keyword && (
                    <span className="ml-2 text-xs text-blue-600 dark:text-blue-400 font-mono bg-blue-100 dark:bg-blue-900/20 px-1 rounded">
                      {alert.keyword}
                    </span>
                  )}
                </div>
                <div className="text-xs text-gray-400 mt-0.5">
                  {new Date(alert.timestamp).toLocaleString()}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
