import { GroupIcon } from "../../icons";
import AlertsCard from "./AlertsCard";

export default function EcommerceMetrics() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:gap-6">
      {/* <!-- Metric Item Start --> */}
      <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] md:p-6">
        <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-xl dark:bg-gray-800">
          <GroupIcon className="text-gray-800 size-6 dark:text-white/90" />
        </div>

        <form
          className="flex flex-col gap-2 mt-5"
          onSubmit={e => {
            e.preventDefault();
            const form = e.target as HTMLFormElement;
            const pin = (form.elements.namedItem('pin') as HTMLInputElement).value.trim();
            if (pin) {
              localStorage.setItem('pin', pin);
              window.location.reload();
            }
          }}
        >
          <label htmlFor="pin" className="text-sm text-gray-500 dark:text-gray-400">Buscar por PIN</label>
          <div className="flex gap-2">
            <input
              id="pin"
              name="pin"
              type="text"
              placeholder="Ej: 666"
              defaultValue={localStorage.getItem('pin') || ''}
              className="rounded-lg border border-gray-300 px-3 py-1.5 text-gray-800 dark:bg-gray-900 dark:text-white/90 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            <button
              type="submit"
              className="bg-blue-600 text-white rounded-lg px-4 py-1.5 font-semibold hover:bg-blue-700 transition"
            >
              Buscar
            </button>
          </div>
        </form>
      </div>
      {/* <!-- Metric Item End --> */}

      {/* <!-- Alertas Importantes Start --> */}
      <AlertsCard />
      {/* <!-- Alertas Importantes End --> */}
    </div>
  );
}
