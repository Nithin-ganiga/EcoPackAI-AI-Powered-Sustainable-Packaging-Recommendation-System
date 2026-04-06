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

const CostCharts = ({ costData, summary }) => {
  const byTier = costData?.cost_by_tier || [];
  const byType = costData?.cost_by_material_type || [];
  const distribution = costData?.cost_distribution || [];
  const scatter = costData?.cost_vs_suitability || [];

  return (
    <section className="space-y-5">
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Cost Analysis by Sustainability Tier</h3>
          <p className="mb-2 text-sm text-slate-500">Compare average, minimum, and maximum cost spread across tiers.</p>
          <Plot
            data={[
              {
                type: "bar",
                name: "Average",
                x: byTier.map((x) => x.sustainability_tier),
                y: byTier.map((x) => x.avg_cost),
                marker: { color: "#3498db" }
              },
              {
                type: "bar",
                name: "Minimum",
                x: byTier.map((x) => x.sustainability_tier),
                y: byTier.map((x) => x.min_cost),
                marker: { color: "#2ecc71" }
              },
              {
                type: "bar",
                name: "Maximum",
                x: byTier.map((x) => x.sustainability_tier),
                y: byTier.map((x) => x.max_cost),
                marker: { color: "#f39c12" }
              }
            ]}
            layout={{ ...chartLayout, barmode: "group", height: 350 }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <div className="rounded-xl border border-blue-200 bg-blue-50 p-3 text-sm text-blue-900">
            Insight: Eco-friendly material shifts can unlock up to {summary?.cost_savings_percent || 0}% cost savings.
          </div>
        </article>

        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Average Packaging Cost by Material Type</h3>
          <p className="mb-2 text-sm text-slate-500">Lower bars indicate more economical options.</p>
          <Plot
            data={[
              {
                type: "bar",
                x: byType.map((x) => x.material_type),
                y: byType.map((x) => x.avg_cost),
                marker: { color: "#3498db" }
              }
            ]}
            layout={{ ...chartLayout, height: 350, xaxis: { tickangle: -30 } }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: This view helps identify low-cost material types without sacrificing sustainability goals.</p>
        </article>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Cost Range Distribution</h3>
          <p className="mb-2 text-sm text-slate-500">Budget-to-luxury spread across the full inventory.</p>
          <Plot
            data={[
              {
                type: "pie",
                labels: distribution.map((x) => x.cost_range),
                values: distribution.map((x) => x.count),
                marker: { colors: ["#27ae60", "#2ecc71", "#f39c12", "#e74c3c"] }
              }
            ]}
            layout={{ ...chartLayout, height: 350, legend: { orientation: "h" } }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: A balanced distribution gives flexibility for both budget-first and premium sustainability strategies.</p>
        </article>

        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Cost vs Suitability Score (Sweet Spot Analysis)</h3>
          <p className="mb-2 text-sm text-slate-500">Ideal options cluster at low cost and high suitability.</p>
          <Plot
            data={Object.entries(tierColors).map(([tier, color]) => ({
              type: "scatter",
              mode: "markers",
              name: tier,
              x: scatter.filter((item) => item.sustainability_tier === tier).map((x) => x.packaging_cost_inr),
              y: scatter.filter((item) => item.sustainability_tier === tier).map((x) => x.material_suitability_score),
              text: scatter.filter((item) => item.sustainability_tier === tier).map((x) => x.packaging_material),
              hovertemplate: "%{text}<br>Cost: %{x:.2f}<br>Suitability: %{y:.2f}<extra></extra>",
              marker: { color, size: 9, opacity: 0.75 }
            }))}
            layout={{
              ...chartLayout,
              height: 500,
              annotations: [
                {
                  xref: "paper",
                  yref: "paper",
                  x: 0.2,
                  y: 0.85,
                  text: "Sweet Spot: Low Cost + High Suitability",
                  showarrow: true,
                  arrowhead: 2,
                  ax: 50,
                  ay: -30,
                  bgcolor: "#ecfeff"
                }
              ],
              xaxis: { title: "Packaging Cost (INR)" },
              yaxis: { title: "Suitability Score" }
            }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: Target markers in the upper-left region for strongest value-per-rupee outcomes.</p>
        </article>
      </div>
    </section>
  );
};

export default CostCharts;
