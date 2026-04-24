const BASE_URL = "http://127.0.0.1:8000";

export const analyzeText = async (text, category) => {
  const res = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, category })
  });
  return res.json();
};

export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData
  });

  return res.json();
};

export const getStats = async (category) => {
  const res = await fetch(`${BASE_URL}/stats?category=${category}`);
  return res.json();
};

export const getTrend = async (category) => {
  const res = await fetch(`${BASE_URL}/trend?category=${category}`);
  return res.json();
};

export const getTopAspects = async (category) => {
  const res = await fetch(`${BASE_URL}/top-aspects?category=${category}`);
  return res.json();
};