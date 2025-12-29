import LlamadasPorDiaChart from "../../components/ecommerce/LlamadasPorDiaChart";
import LlamadasPorHoraChart from "../../components/ecommerce/LlamadasPorHoraChart";
import TopNumerosMarcados from "../../components/ecommerce/TopNumerosMarcados";
import PageMeta from "../../components/common/PageMeta";

export default function Analytics() {
  return (
    <>
      <PageMeta
        title="React.js Analytics Dashboard | TailAdmin - React.js Admin Dashboard Template"
        description="This is React.js Analytics Dashboard page for TailAdmin - React.js Tailwind CSS Admin Dashboard Template"
      />
      <div className="grid grid-cols-12 gap-4 md:gap-6">
        <div className="col-span-12">
          <LlamadasPorDiaChart />
        </div>
        <div className="col-span-12">
          <LlamadasPorHoraChart />
        </div>
        <div className="col-span-12">
          <TopNumerosMarcados />
        </div>
      </div>
    </>
  );
}
