// This file wraps all HTTP calls to the backend so request formatting and error handling are standardized in one place.

import axios from "axios";

const api = axios.create({
  baseURL: "/",
  timeout: 15000
});

export const getRecommendations = async (productName, productWeightGrams) => {
  try {
    const response = await api.post("/api/recommend", {
      product_name: productName,
      product_weight_grams: productWeightGrams
    });
    return response.data;
  } catch (error) {
    const message =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.message ||
      "Failed to fetch recommendations";
    throw new Error(message);
  }
};

export const getAutocomplete = async (query) => {
  if (!query || !query.trim()) {
    return [];
  }

  try {
    const response = await api.get(`/api/autocomplete?q=${encodeURIComponent(query.trim())}`);
    return response?.data?.suggestions || [];
  } catch {
    return [];
  }
};
