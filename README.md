# 🧠 ABSA Dashboard (Aspect-Based Sentiment Analysis)

An end-to-end web application that performs **Aspect-Based Sentiment Analysis (ABSA)** on user reviews.
It extracts aspects (features), determines sentiment (positive, negative, neutral), and visualizes insights through an interactive dashboard.

---

## 🚀 Features

* 🔍 **Aspect Extraction (ATE)** – Identifies key aspects from text
* 😊 **Sentiment Classification (ASC)** – Classifies sentiment per aspect
* 📊 **Interactive Dashboard**

  * Sentiment Pie Chart
  * Aspect Distribution Bar Chart
  * Trend Analysis
* ☁️ **Word Cloud Visualization**
* 📁 **Upload Reviews (CSV/Excel/Text)**
* ✍️ **Manual Review Input**
* ⚡ Fast API backend + modern React frontend

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Pandas, NumPy
* NLP / Transformers

### Frontend

* React (Vite)
* JavaScript
* Chart Libraries

---

## 📂 Project Structure

```
absa-dashboard/
│
├── backend/
│   ├── app/
│   │   ├── api.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── predictor.py
│   │   └── ...
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/Himabindu-4/absa-dashboard.git
cd absa-dashboard
```

---

### 🔹 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 🔹 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 📊 How It Works

1. User uploads reviews or enters text
2. Backend processes text using ABSA pipeline
3. Extracts:

   * Aspect
   * Sentiment
   * Confidence
4. Results are visualized in dashboard

---

## 📸 Screenshots
(<Screenshot (675)(1).png>)
(<Screenshot (674)(1).png>)
(<Screenshot (676)(1).png>)
(<Screenshot (677)(1).png>)
---

## ⚠️ Notes

* Large ML model files are excluded from this repository
* Models can be loaded/downloaded separately

---

## 🎯 Future Improvements

* Deploy to cloud (Render / Vercel)
* Add user authentication
* Improve model accuracy
* Real-time streaming analysis

---

## 👩‍💻 Author

**Himabindu**


