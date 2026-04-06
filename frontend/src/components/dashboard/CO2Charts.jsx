import Plot from "react-plotly.js";

const tierColors = {
  Excellent: "#27ae60",
  Good: "#2980b9",
  Average: "#f39c12",
  Poor: "#e74c3c"
};

const chartLayout = {
  paper_bgcolor: "#ffffff",
  plot_bgcolor: "#ffffff",
  margin: { l: 50, r: 20, t: 60, b: 60 },
  autosize: true,
  font: { color: "#0f172a" }
};

const config = { responsive: true, displayModeBar: false };

const CO2Charts = ({ co2Data, summary }) => {
  const byTier = co2Data?.co2_by_tier || [];
  const byType = co2Data?.co2_by_material_type || [];
  const distribution = co2Data?.co2_distribution_buckets || [];

  const reduction = summary?.co2_reduction_percent || 0;

  return (
    <section className="space-y-5">
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Average CO2 Emission Score by Sustainability Tier</h3>
          <p className="mb-2 text-sm text-slate-500">Lower score indicates lower climate impact.</p>
          <Plot
            data={[
              {
                type: "bar",
                x: byTier.map((x) => x.sustainability_tier),
                y: byTier.map((x) => Number(x.avg_co2 || 0).toFixed(2)),
                marker: { color: byTier.map((x) => tierColors[x.sustainability_tier] || "#2ecc71") }
              }
            ]}
            layout={{ ...chartLayout, height: 350 }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-900">
            Insight: Switching from Poor to Excellent tier can reduce CO2 emissions by {reduction}%.
          </div>
        </article>

        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">CO2 Emission by Material Type (Lower is Better)</h3>
          <p className="mb-2 text-sm text-slate-500">Material types sorted from best to worst average CO2 impact.</p>
          <Plot
            data={[
              {
                type: "bar",
                orientation: "h",
                y: [...byType.map((x) => x.material_type)].reverse(),
                x: [...byType.map((x) => Number(x.avg_co2 || 0))].reverse(),
                marker: {
                  color: [...byType.map((x) => Number(x.avg_co2 || 0))].reverse(),
                  colorscale: [
                    [0, "#27ae60"],
                    [0.5, "#f1c40f"],
                    [1, "#e74c3c"]
                  ]
                }
              }
            ]}
            layout={{ ...chartLayout, height: 350 }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: Paper-like and bio-based categories typically occupy the low-emission zone.</p>
        </article>
      </div>

      <div className="grid grid-cols-1 gap-5">
        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">CO2 Emission Distribution Across Materials</h3>
          <p className="mb-2 text-sm text-slate-500">Bucketed emission view for all materials in the database.</p>
          <Plot
            data={[
              {
                type: "pie",
                hole: 0.5,
                labels: distribution.map((x) => x.bucket),
                values: distribution.map((x) => x.count),
                marker: {
                  colors: ["#27ae60", "#2ecc71", "#f39c12", "#e74c3c"]
                }
              }
            ]}
            layout={{ ...chartLayout, height: 350, legend: { orientation: "h" } }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: Distribution shape reveals where most materials currently sit on the sustainability curve.</p>
        </article>
      </div>
    </section>
  );
};

export default CO2Charts;
