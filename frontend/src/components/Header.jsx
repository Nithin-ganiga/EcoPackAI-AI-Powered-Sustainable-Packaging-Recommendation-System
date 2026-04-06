// This file renders the top application header and brand area so users always know the purpose of the tool.

const Header = ({ currentPage, onNavigate }) => {
  return (
    <header className="bg-navy text-white border-b border-slate-800">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">EcoPackAI</h1>
          <p className="hidden text-sm text-slate-200 md:block">
            AI-Powered Sustainable Packaging Recommendations
          </p>
        </div>

        <nav className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => onNavigate("home")}
            className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition ${
              currentPage === "home" || currentPage === "results"
                ? "bg-emerald-600 text-white"
                : "bg-slate-700 text-slate-100 hover:bg-slate-600"
            }`}
          >
            Recommendations
          </button>
          <button
            type="button"
            onClick={() => onNavigate("dashboard")}
            className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition ${
              currentPage === "dashboard"
                ? "bg-emerald-600 text-white"
                : "bg-slate-700 text-slate-100 hover:bg-slate-600"
            }`}
          >
            Dashboard
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
