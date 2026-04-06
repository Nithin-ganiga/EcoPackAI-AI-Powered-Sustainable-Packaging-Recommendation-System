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

const normalize = (value, max) => {
  if (!max) {
    return 0;
  }
  return (Number(value || 0) / max) * 100;
};

const TrendCharts = ({ trendsData }) => {
  const tierDist = trendsData?.tier_distribution || [];
  const byType = trendsData?.material_type_distribution || [];
  const top10 = trendsData?.top_10_sustainable || [];
  const industry = trendsData?.industry_sustainability || [];
  const bioRecycle = trendsData?.biodegradability_by_type || [];

  const totalCount = tierDist.reduce((acc, item) => acc + Number(item.count || 0), 0);
  const maxSuit = Math.max(...byType.map((x) => Number(x.avg_suitability || 0)), 1);
  const maxBio = Math.max(...byType.map((x) => Number(x.avg_bio || 0)), 1);
  const maxRec = Math.max(...byType.map((x) => Number(x.avg_recycle || 0)), 1);
  const maxLowCO2 = Math.max(...byType.map((x) => 100 - Number(x.avg_co2 || 0)), 1);

  return (
    <section className="space-y-5">
      <article className="rounded-2xl bg-white p-4 shadow-sm">
        <h3 className="text-lg font-semibold text-slate-900">Sustainability Tier Distribution</h3>
        <p className="mb-2 text-sm text-slate-500">Current material mix across Excellent, Good, Average, and Poor tiers.</p>
        <Plot
          data={[
            {
              type: "pie",
              hole: 0.55,
              labels: tierDist.map((x) => x.sustainability_tier),
              values: tierDist.map((x) => x.count),
              marker: {
                colors: tierDist.map((x) => tierColors[x.sustainability_tier] || "#95a5a6")
              },
              textinfo: "label+percent"
            }
          ]}
          layout={{
            ...chartLayout,
            height: 350,
            annotations: [{ text: `Total<br>${totalCount}`, showarrow: false, font: { size: 18 } }]
          }}
          style={{ width: "100%" }}
          config={config}
          useResizeHandler
        />
        <p className="text-sm text-slate-500">Insight: Track portfolio quality by watching Excellent and Good segments expand over time.</p>
      </article>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Material Type Comparison (Eco Metrics)</h3>
          <p className="mb-2 text-sm text-slate-500">Normalized comparison of performance dimensions on a 0-100 scale.</p>
          <Plot
            data={byType.slice(0, 6).map((item) => ({
              type: "scatterpolar",
              r: [
                normalize(item.avg_suitability, maxSuit),
                normalize(item.avg_bio, maxBio),
                normalize(item.avg_recycle, maxRec),
                normalize(100 - Number(item.avg_co2 || 0), maxLowCO2)
              ],
              theta: ["Avg Suitability", "Avg Biodegradability", "Avg Recyclability", "Low CO2 Score"],
              fill: "toself",
              name: item.material_type
            }))}
            layout={{ ...chartLayout, polar: { radialaxis: { visible: true, range: [0, 100] } }, height: 430 }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: Radar shape reveals balanced material categories versus specialist categories.</p>
        </article>

        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Top 10 Most Sustainable Materials</h3>
          <p className="mb-2 text-sm text-slate-500">Highest material suitability scores with visible tier status.</p>
          <Plot
            data={[
              {
                type: "bar",
                orientation: "h",
                y: [...top10.map((x) => `${x.packaging_material} (${x.sustainability_tier})`)].reverse(),
                x: [...top10.map((x) => x.material_suitability_score)].reverse(),
                marker: {
                  color: [...top10.map((x) => tierColors[x.sustainability_tier] || "#27ae60")].reverse()
                }
              }
            ]}
            layout={{ ...chartLayout, height: 430 }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: This ranking is ideal for immediate pilot substitutions in high-volume packaging flows.</p>
        </article>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Industry Sustainability Comparison</h3>
          <p className="mb-2 text-sm text-slate-500">Top industries by suitability with inverse CO2 benchmark.</p>
          <Plot
            data={[
              {
                type: "bar",
                name: "Avg Suitability",
                x: industry.map((x) => x.industry),
                y: industry.map((x) => x.avg_suitability),
                marker: { color: "#27ae60" }
              },
              {
                type: "bar",
                name: "Low CO2 Index",
                x: industry.map((x) => x.industry),
                y: industry.map((x) => Math.max(0, 100 - Number(x.avg_co2 || 0))),
                marker: { color: "#2980b9" }
              }
            ]}
            layout={{ ...chartLayout, barmode: "group", height: 350, xaxis: { tickangle: -30 } }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: Industry leaders combine high suitability with low-emission material profiles.</p>
        </article>

        <article className="rounded-2xl bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Biodegradability vs Recyclability by Material Type</h3>
          <p className="mb-2 text-sm text-slate-500">Spot categories with strong dual circularity performance.</p>
          <Plot
            data={[
              {
                type: "scatter",
                mode: "markers+text",
                x: bioRecycle.map((x) => x.avg_bio),
                y: bioRecycle.map((x) => x.avg_recycle),
                text: bioRecycle.map((x) => x.material_type),
                textposition: "top center",
                marker: {
                  size: 12,
                  color: bioRecycle.map((_, idx) => idx),
                  colorscale: "Viridis"
                },
                hovertemplate: "%{text}<br>Biodegradability: %{x:.2f}<br>Recyclability: %{y:.2f}<extra></extra>"
              }
            ]}
            layout={{
              ...chartLayout,
              height: 500,
              xaxis: { title: "Avg Biodegradability" },
              yaxis: { title: "Avg Recyclability" }
            }}
            style={{ width: "100%" }}
            config={config}
            useResizeHandler
          />
          <p className="text-sm text-slate-500">Insight: Upper-right clusters represent the strongest candidates for circular packaging programs.</p>
        </article>
      </div>
    </section>
  );
};

export default TrendCharts;
