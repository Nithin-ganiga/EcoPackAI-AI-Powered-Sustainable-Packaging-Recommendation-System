const cardConfig = [
  {
    id: "adoption",
    label: "Eco Adoption Rate",
    key: "eco_adoption_rate",
    suffix: "%",
    subtext: "Excellent + Good tier",
    border: "border-teal-500",
    bg: "bg-teal-50",
    icon: "🍃"
  },
  {
    id: "bio",
    label: "Avg Biodegradability",
    key: "avg_biodegradability",
    suffix: "/100",
    subtext: "across all materials",
    border: "border-cyan-500",
    bg: "bg-cyan-50",
    icon: "♻"
  },
  {
    id: "recycle",
    label: "Avg Recyclability",
    key: "avg_recyclability",
    suffix: "%",
    subtext: "across all materials",
    border: "border-sky-500",
    bg: "bg-sky-50",
    icon: "↻"
  },
  {
    id: "total",
    label: "Materials Analyzed",
    key: "total_materials",
    suffix: "",
    subtext: "in database",
    border: "border-violet-500",
    bg: "bg-violet-50",
    icon: "📦"
  }
];

const formatValue = (value, suffix) => {
  if (typeof value === "number") {
    const formatted = Number.isInteger(value) ? value.toLocaleString() : value.toFixed(1);
    return `${formatted}${suffix}`;
  }
  return `0${suffix}`;
};

const SummaryCards = ({ summary }) => {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
      {cardConfig.map((card) => (
        <article
          key={card.id}
          title={card.label}
          className={`card-lift rounded-2xl border-l-4 ${card.border} bg-white p-5 shadow-sm`}
        >
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{card.label}</p>
              <p className="mt-2 text-2xl font-bold text-slate-900">
                {formatValue(summary?.[card.key], card.suffix)}
              </p>
              <p className="mt-1 text-sm text-slate-500">{card.subtext}</p>
            </div>
            <div className={`grid h-10 w-10 place-items-center rounded-xl text-lg ${card.bg}`}>
              {card.icon}
            </div>
          </div>
        </article>
      ))}
    </div>
  );
};

export default SummaryCards;
