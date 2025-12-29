import RecentOrders from "../../components/ecommerce/RecentOrders";
import PageMeta from "../../components/common/PageMeta";

export default function Crm() {
  return (
    <>
      <PageMeta
        title="Transcripciones | SENTINELA"
        description="Sección dedicada a la consulta y visualización de transcripciones de llamadas asociadas al PIN seleccionado."
      />
      <div className="max-w-5xl mx-auto mt-8">
        <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Transcripciones</h2>
        <p className="mb-6 text-gray-600 dark:text-gray-300">
          Consulta aquí el historial de llamadas y transcripciones asociadas al PPL seleccionado por PIN. Puedes revisar los detalles, descargar el audio o PDF si están disponibles.
        </p>
        <RecentOrders />
      </div>
    </>
  );
}
