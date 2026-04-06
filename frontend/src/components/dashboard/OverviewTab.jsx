import Plot from "react-plotly.js";

const tierColors = {
  Excellent: "#27ae60",
  Good: "#2980b9",
  Average: "#f39c12",
  Poor: "#e74c3c"
};

const layout = {
  paper_bgcolor: "#ffffff",
  plot_bgcolor: "#ffffff",
  margin: { l: 40, r: 20, t: 60, b: 50 },
  autosize: true,
  font: { color: "#0f172a" }
};

const config = { responsive: true, displayModeBar: false };

const OverviewTab = ({ co2Data, costData }) => {
  const co2ByTier = co2Data?.co2_by_tier || [];
  const costByTier = costData?.cost_by_tier || [];

  return (
    <section className="space-y-5">
      <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Tier-Level Cost Baseline</h3>
          <p className="mb-2 text-sm text-slate-500">Average cost across sustainability tiers.</p>
          <Plot
            data={[
              {
                type: "bar",
                x: costByTier.map((x) => x.sustainability_tier),
                y: costByTier.map((x) => Number(x.avg_cost || 0)),
                marker: { color: costByTier.map((x) => tierColors[x.sustainability_tier] || "#2980b9") }
              }
            ]}
            layout={{ ...layout, height: 320 }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
      </article>

      <article className="rounded-2xl bg-white p-4 shadow-sm">
        <h3 className="text-lg font-semibold text-slate-900">Tier-Level CO2 Baseline</h3>
        <p className="mb-2 text-sm text-slate-500">Average CO2 emission score by sustainability tier.</p>
        <Plot
          data={[
            {
              type: "bar",
              x: co2ByTier.map((x) => x.sustainability_tier),
              y: co2ByTier.map((x) => Number(x.avg_co2 || 0)),
              marker: { color: co2ByTier.map((x) => tierColors[x.sustainability_tier] || "#2ecc71") }
            }
          ]}
          layout={{ ...layout, height: 340 }}
          style={{ width: "100%" }}
          config={config}
          useResizeHandler
        />
      </article>
    </section>
  );
};

export default OverviewTab;
