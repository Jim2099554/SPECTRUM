import PageMeta from "../../components/common/PageMeta";
import UserTable from "../../components/UserTable";

export default function Usuarios() {
  return (
    <>
      <PageMeta
        title="Gestión de Usuarios | SENTINELA"
        description="Pantalla de administración para agregar y eliminar usuarios."
      />
      <div className="space-y-5 sm:space-y-6">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">Gestión de Usuarios</h1>
        <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]">
          <UserTable />
        </div>
      </div>
    </>
  );
}
