// This file displays one recommended material with key sustainability and suitability information in a compact readable card.

const tierColorMap = {
  Excellent: "bg-green-100 text-green-700",
  Good: "bg-blue-100 text-blue-700",
  Average: "bg-orange-100 text-orange-700",
  Poor: "bg-red-100 text-red-700"
};

const fragilityColorMap = {
  Low: "text-red-600",
  Medium: "text-yellow-600",
  High: "text-green-600"
};

const MaterialCard = ({ material }) => {
  const isBest = material.rank === 1;
  const scoreValue = Math.max(0, Math.min(100, Number(material.suitability_score) || 0));

  return (
    <article
      className={`card-lift relative rounded-2xl bg-white p-6 shadow-lg ring-1 ring-slate-200 ${
        isBest ? "border-2 border-slate-900" : ""
      }`}
    >
      <div
        className={`absolute -left-3 -top-3 flex h-11 w-11 items-center justify-center rounded-full text-sm font-bold text-white shadow-lg ${
          isBest ? "bg-slate-900" : "bg-eco-green"
        }`}
      >
        {material.rank}
      </div>

      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <h3 className="text-xl font-extrabold text-slate-800">
            {material.material_name}
          </h3>
          <p className="text-sm text-slate-500">{material.material_type}</p>
        </div>
        <span className={`rounded-full px-3 py-1 text-xs font-semibold ${tierColorMap[material.sustainability_tier] || "bg-slate-100 text-slate-700"}`}>
          {material.sustainability_tier}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-slate-500">Strength</p>
          <p className="font-semibold text-slate-800">{material.strength}</p>
        </div>
        <div>
          <p className="text-slate-500">Weight Capacity</p>
          <p className="font-semibold text-slate-800">{material.weight_capacity}</p>
        </div>
        <div>
          <p className="text-slate-500">Sustainability Tier</p>
          <p className="font-semibold text-slate-800">{material.sustainability_tier}</p>
        </div>
        <div>
          <p className="text-slate-500">Eco Friendly</p>
          <p className={`font-semibold ${material.eco_friendly ? "text-green-600" : "text-red-600"}`}>
            {material.eco_friendly ? "Yes" : "No"}
          </p>
        </div>
        <div>
          <p className="text-slate-500">Recyclability</p>
          <p className="font-semibold text-slate-800">{material.recyclability_percent}%</p>
        </div>
        <div>
          <p className="text-slate-500">Fragility Support</p>
          <p className={`font-semibold ${fragilityColorMap[material.fragility_support] || "text-slate-800"}`}>
            {material.fragility_support}
          </p>
        </div>
      </div>

      <div className="mt-5">
        <div className="mb-1 flex justify-between text-sm font-semibold text-slate-700">
          <span>Suitability Score</span>
          <span>{scoreValue.toFixed(1)}</span>
        </div>
        <div className="h-2 w-full rounded-full bg-slate-200">
          <div className="h-2 rounded-full bg-gradient-to-r from-eco-dark to-eco-green" style={{ width: `${scoreValue}%` }} />
        </div>
      </div>

      <div className="mt-4 rounded-xl bg-green-50 p-3 text-sm text-green-800">
        <p className="font-semibold">Why Recommended</p>
        <p className="mt-1">{material.why_recommended}</p>
      </div>
    </article>
  );
};

export default MaterialCard;
