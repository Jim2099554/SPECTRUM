import EcommerceMetrics from "../../components/ecommerce/EcommerceMetrics";
import LlamadasPorDiaChart from "../../components/ecommerce/LlamadasPorDiaChart";
import StatisticsNetwork from "../StatisticsNetwork";
import MonthlyTarget from "../../components/ecommerce/MonthlyTarget";
import DangerousWords from "../../components/ecommerce/DangerousWords";
import RecentOrders from "../../components/ecommerce/RecentOrders";
import DemographicCard from "../../components/ecommerce/DemographicCard";
import PageMeta from "../../components/common/PageMeta";


export default function DashboardPrincipal() {
  // Obtener el PIN desde localStorage (ajusta la clave si es diferente)

  return (
    <>
      <PageMeta
        title="Dashboard Principal | SENTINELA"
        description="Este es el dashboard principal de SENTINELA."
      />
      
      <div className="grid grid-cols-12 gap-4 md:gap-6">
        <div className="col-span-12 space-y-6 xl:col-span-7">
          <EcommerceMetrics />

          <LlamadasPorDiaChart />


        </div>

        <div className="col-span-12 xl:col-span-5 space-y-6">
          <MonthlyTarget />
          <DangerousWords />
        </div>

        <div className="col-span-12">
          <StatisticsNetwork />
        </div>

        <div className="col-span-12 xl:col-span-5">
          <DemographicCard />
        </div>

        <div className="col-span-12 xl:col-span-7">
          <RecentOrders />
        </div>
      </div>
    </>
  );
}
