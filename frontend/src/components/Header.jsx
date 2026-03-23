// This file renders the top application header and brand area so users always know the purpose of the tool.

const Header = () => {
  return (
    <header className="bg-navy text-white border-b border-slate-800">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <h1 className="text-2xl font-bold tracking-tight text-white">EcoPackAI</h1>
        <p className="hidden text-sm text-slate-200 md:block">
          AI-Powered Sustainable Packaging Recommendations
        </p>
      </div>
    </header>
  );
};

export default Header;
