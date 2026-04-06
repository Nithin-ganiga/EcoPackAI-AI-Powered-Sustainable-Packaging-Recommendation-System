import { useEffect, useMemo, useState } from "react";
import CO2Charts from "../components/dashboard/CO2Charts";
import CostCharts from "../components/dashboard/CostCharts";
import ExportButtons from "../components/dashboard/ExportButtons";
import OverviewTab from "../components/dashboard/OverviewTab";
import SummaryCards from "../components/dashboard/SummaryCards";
import {
  exportExcel,
  exportPDF,
  getCO2Analysis,
  getCostAnalysis,
  getDashboardSummary
} from "../services/api";

const tabs = [
  { id: "overview", label: "Overview" },
  { id: "co2", label: "CO2 Analysis" },
  { id: "cost", label: "Cost Analysis" }
];

const triggerDownload = (blob, prefix, extension) => {
  const date = new Date().toISOString().slice(0, 10);
  const url = window.URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${prefix}_${date}.${extension}`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.URL.revokeObjectURL(url);
};

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [co2Data, setCo2Data] = useState(null);
  const [costData, setCostData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [exportingPDF, setExportingPDF] = useState(false);
  const [exportingExcel, setExportingExcel] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    let mounted = true;

    const loadDashboard = async () => {
      setLoading(true);
      setError(null);

      try {
        const [summaryRes, co2Res, costRes] = await Promise.all([
          getDashboardSummary(),
          getCO2Analysis(),
          getCostAnalysis()
        ]);

        if (!mounted) {
          return;
        }

        setSummary(summaryRes);
        setCo2Data(co2Res);
        setCostData(costRes);
      } catch (err) {
        if (!mounted) {
          return;
        }
        setError(err?.message || "Failed to load dashboard data");
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadDashboard();
    return () => {
      mounted = false;
    };
  }, []);

  const handleExportPDF = async () => {
    setExportingPDF(true);
    try {
      const blob = await exportPDF();
      triggerDownload(blob, "EcoPackAI_Report", "pdf");
    } catch (err) {
      setError(err?.message || "Failed to export PDF report");
    } finally {
      setExportingPDF(false);
    }
  };

  const handleExportExcel = async () => {
    setExportingExcel(true);
    try {
      const blob = await exportExcel();
      triggerDownload(blob, "EcoPackAI_Report", "xlsx");
    } catch (err) {
      setError(err?.message || "Failed to export Excel report");
    } finally {
      setExportingExcel(false);
    }
  };

  const tabContent = useMemo(() => {
    if (activeTab === "co2") {
      return <CO2Charts co2Data={co2Data} summary={summary} />;
    }
    if (activeTab === "cost") {
      return <CostCharts costData={costData} summary={summary} />;
    }
    return <OverviewTab co2Data={co2Data} costData={costData} />;
  }, [activeTab, co2Data, costData, summary]);

  if (loading) {
    return (
      <section className="space-y-5">
        <div className="h-32 animate-pulse rounded-2xl bg-white" />
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: 6 }).map((_, idx) => (
            <div key={idx} className="h-28 animate-pulse rounded-2xl bg-white" />
          ))}
        </div>
        <div className="h-80 animate-pulse rounded-2xl bg-white" />
      </section>
    );
  }

  if (error) {
    return (
      <section className="rounded-2xl border border-rose-200 bg-rose-50 p-5 text-rose-700">
        <h2 className="text-lg font-semibold">Dashboard Error</h2>
        <p className="mt-2 text-sm">{error}</p>
      </section>
    );
  }

  return (
    <section className="space-y-6">
      <header className="rounded-2xl bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Business Intelligence Dashboard</h2>
            <p className="mt-1 text-sm text-slate-500">
              Sustainability intelligence for CO2 and cost optimization.
            </p>
          </div>
          <ExportButtons
            onExportPDF={handleExportPDF}
            onExportExcel={handleExportExcel}
            exportingPDF={exportingPDF}
            exportingExcel={exportingExcel}
          />
        </div>
      </header>

      <SummaryCards summary={summary} />

      <nav className="flex flex-wrap gap-2 rounded-2xl bg-white p-3 shadow-sm">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id)}
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
              activeTab === tab.id
                ? "bg-emerald-600 text-white"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {tabContent}
    </section>
  );
};

export default Dashboard;
