// This file controls the main user flow of the web app by handling search requests, loading and error states, and switching between the input screen and recommendation results.

import { useEffect, useState } from "react";
import Header from "./components/Header";
import SearchForm from "./components/SearchForm";
import ResultCards from "./components/ResultCards";
import LoadingSpinner from "./components/LoadingSpinner";
import ErrorMessage from "./components/ErrorMessage";
import Dashboard from "./pages/Dashboard";
import { getRecommendations } from "./services/api";

const resolvePageFromPath = (path) => {
  if (path === "/dashboard") {
    return "dashboard";
  }
  return "home";
};

const App = () => {
  const [currentPage, setCurrentPage] = useState(resolvePageFromPath(window.location.pathname));
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
      setCurrentPage("results");
    } catch (err) {
      setError(err.message || "Failed to fetch recommendations");
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setCurrentPage("home");
    setResults(null);
    setError(null);
  };

  const handleNavigate = (page) => {
    setError(null);
    if (page === "dashboard") {
      setCurrentPage("dashboard");
      if (window.location.pathname !== "/dashboard") {
        window.history.pushState({}, "", "/dashboard");
      }
      return;
    }
    if (window.location.pathname !== "/") {
      window.history.pushState({}, "", "/");
    }
    if (results) {
      setCurrentPage("results");
      return;
    }
    setCurrentPage("home");
  };

  useEffect(() => {
    const onPopState = () => {
      const page = resolvePageFromPath(window.location.pathname);
      if (page === "dashboard") {
        setCurrentPage("dashboard");
      } else {
        setCurrentPage(results ? "results" : "home");
      }
    };

    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, [results]);

  return (
    <div className="min-h-screen bg-slate-100">
      <Header currentPage={currentPage} onNavigate={handleNavigate} />
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

        {currentPage === "dashboard" && <Dashboard />}

        {currentPage === "home" && <SearchForm onSubmit={handleSearch} loading={loading} />}

        {currentPage === "results" && results && (
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
