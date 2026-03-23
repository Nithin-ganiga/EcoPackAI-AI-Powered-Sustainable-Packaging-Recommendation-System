// This file shows the recommendation summary and arranges ranked material cards so users can quickly compare top suggestions.

import MaterialCard from "./MaterialCard";

const ResultCards = ({ results, productName, fragility, weightGrams }) => {
  const recommendations = results?.recommendations || [];
  if (!recommendations.length) {
    return null;
  }

  const bestPick = recommendations[0];
  const rest = recommendations.slice(1);

  return (
    <section className="mx-auto w-full max-w-7xl space-y-5">
      <div className="rounded-2xl bg-white p-5 shadow-md ring-1 ring-slate-200">
        <h2 className="text-xl font-extrabold text-slate-800">
          Top 5 recommendations for <span className="text-eco-dark">{productName}</span>
        </h2>
        <p className="mt-1 text-sm text-slate-600">
          Weight: {Number(weightGrams).toFixed(2)} grams
        </p>
      </div>

      <div className="rounded-2xl border border-slate-300 bg-slate-50 p-4 text-slate-800 shadow-sm">
        <p className="text-sm font-bold">Best Pick: {bestPick.material_name}</p>
      </div>

      <MaterialCard material={bestPick} />

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {rest.map((material) => (
          <MaterialCard key={`${material.rank}-${material.material_name}`} material={material} />
        ))}
      </div>
    </section>
  );
};

export default ResultCards;
