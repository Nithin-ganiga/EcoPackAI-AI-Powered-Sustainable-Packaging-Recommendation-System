// This file renders the product input form, validates user input, and handles autocomplete behavior before sending a search request.

import { useEffect, useMemo, useState } from "react";
import { getAutocomplete } from "../services/api";

const SearchForm = ({ onSubmit, loading }) => {
  const [productName, setProductName] = useState("");
  const [weightValue, setWeightValue] = useState("");
  const [weightUnit, setWeightUnit] = useState("grams");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [formError, setFormError] = useState("");

  const normalizedWeight = useMemo(() => {
    const num = Number(weightValue);
    if (Number.isNaN(num)) {
      return 0;
    }
    return weightUnit === "kg" ? num * 1000 : num;
  }, [weightValue, weightUnit]);

  useEffect(() => {
    if (!productName.trim()) {
      setSuggestions([]);
      return;
    }

    const timer = setTimeout(async () => {
      const data = await getAutocomplete(productName);
      setSuggestions(data);
    }, 400);

    return () => clearTimeout(timer);
  }, [productName]);

  const selectSuggestion = (value) => {
    setProductName(value);
    setShowSuggestions(false);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!productName.trim()) {
      setFormError("Please enter a product name.");
      return;
    }

    if (!normalizedWeight || normalizedWeight <= 0) {
      setFormError("Please enter a valid product weight greater than zero.");
      return;
    }

    setFormError("");
    onSubmit(productName.trim(), normalizedWeight);
  };

  return (
    <div className="mx-auto w-full max-w-5xl rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200 md:p-10">
      <form className="space-y-8" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="product_name" className="mb-2 block text-sm font-semibold text-slate-700">
            Product Name
          </label>
          <div className="relative">
            <input
              id="product_name"
              type="text"
              value={productName}
              onFocus={() => setShowSuggestions(true)}
              onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="e.g. Salt, Phone, Bread, Medicine"
              className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-900 outline-none transition focus:border-eco-green focus:ring-2 focus:ring-eco-green/30"
            />
            {showSuggestions && suggestions.length > 0 && (
              <div className="absolute z-20 mt-2 max-h-56 w-full overflow-auto rounded-xl border border-slate-200 bg-white shadow-lg">
                {suggestions.slice(0, 8).map((suggestion) => (
                  <button
                    type="button"
                    key={suggestion}
                    className="block w-full border-b border-slate-100 px-4 py-2 text-left text-sm text-slate-700 hover:bg-green-50"
                    onMouseDown={() => selectSuggestion(suggestion)}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="weight" className="mb-2 block text-sm font-semibold text-slate-700">
            Product Weight
          </label>
          <div className="flex flex-col gap-3 md:flex-row">
            <input
              id="weight"
              type="number"
              min="0.1"
              step="0.1"
              value={weightValue}
              onChange={(e) => setWeightValue(e.target.value)}
              placeholder="Enter weight"
              className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-900 outline-none transition focus:border-eco-green focus:ring-2 focus:ring-eco-green/30"
            />
            <div className="inline-flex rounded-xl border border-slate-300 p-1">
              <button
                type="button"
                onClick={() => setWeightUnit("grams")}
                className={`rounded-lg px-4 py-2 text-sm font-semibold ${
                  weightUnit === "grams" ? "bg-eco-green text-white" : "text-slate-700"
                }`}
              >
                Grams
              </button>
              <button
                type="button"
                onClick={() => setWeightUnit("kg")}
                className={`rounded-lg px-4 py-2 text-sm font-semibold ${
                  weightUnit === "kg" ? "bg-eco-green text-white" : "text-slate-700"
                }`}
              >
                KG
              </button>
            </div>
          </div>
        </div>

        {formError && <p className="rounded-lg bg-red-50 px-3 py-2 text-sm font-medium text-red-700">{formError}</p>}

        <button
          type="submit"
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-eco-dark px-6 py-3 text-base font-semibold text-white transition hover:bg-eco-green disabled:cursor-not-allowed disabled:opacity-70"
        >
          {loading ? (
            <>
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Analyzing...
            </>
          ) : (
            <>
              Get Top 5 Recommendations
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default SearchForm;
