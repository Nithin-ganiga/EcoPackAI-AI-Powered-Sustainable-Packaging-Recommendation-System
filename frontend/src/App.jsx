// This file controls the main user flow of the web app by handling search requests, loading and error states, and switching between the input screen and recommendation results.

import { useState } from "react";
import Header from "./components/Header";
import SearchForm from "./components/SearchForm";
import ResultCards from "./components/ResultCards";
import LoadingSpinner from "./components/LoadingSpinner";
import ErrorMessage from "./components/ErrorMessage";
import { getRecommendations } from "./services/api";

const App = () => {
  const [view, setView] = useState("home");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [lastSearch, setLastSearch] = useState({
    productName: "",
    weightGrams: 0,
    fragility: "auto"
  });

  const handleSearch = async (productName, weightGrams) => {
    setLoading(true);
    setError(null);

    try {
      const data = await getRecommendations(productName, weightGrams);
      setResults(data);
      setLastSearch({
        productName,
        weightGrams,
        fragility: data?.fragility || "auto"
      });
      setView("results");
    } catch (err) {
      setError(err.message || "Failed to fetch recommendations");
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setView("home");
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <Header />
      <main className="mx-auto max-w-7xl px-4 py-8 md:px-8">
        {error && (
          <div className="mb-6">
            <ErrorMessage message={error} />
            <button
              type="button"
              onClick={handleBack}
              className="mt-3 rounded-lg bg-slate-800 px-4 py-2 text-sm font-semibold text-white"
            >
              Retry
            </button>
          </div>
        )}

        {view === "home" && <SearchForm onSubmit={handleSearch} loading={loading} />}

        {view === "results" && results && (
          <div className="space-y-5">
            <button
              type="button"
              onClick={handleBack}
              className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm hover:bg-slate-50"
            >
              ← Search Again
            </button>
            <ResultCards
              results={results}
              productName={lastSearch.productName}
              fragility={lastSearch.fragility}
              weightGrams={lastSearch.weightGrams}
            />
          </div>
        )}
      </main>
      {loading && <LoadingSpinner />}
    </div>
  );
};

export default App;
