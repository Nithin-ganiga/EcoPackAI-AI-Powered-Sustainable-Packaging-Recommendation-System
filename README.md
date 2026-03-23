# EcoPackAI - Packaging Material Recommendation System

EcoPackAI is a full-stack application that recommends the top 5 packaging materials for a product based on:
- Product name
- Product weight
- Fragility level

It combines:
- Pre-trained ML models for base scoring
- Rule-based filtering and ranking for weight and fragility

## Tech Stack

- Frontend: React 18, Tailwind CSS, Axios
- Backend: FastAPI, Uvicorn, Python 3.10+
- Database: MySQL
- ML runtime: scikit-learn, xgboost, pandas, numpy, joblib

## Project Structure

- backend: FastAPI API, ML inference pipeline, rule engine, MySQL access
- frontend: React UI with search form, autocomplete, result cards, loading and error states

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- MySQL 8+

## 1) Backend Setup

From project root:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

If you already use the root venv, you can install directly with that environment too.

## 2) Configure Environment Variables

Edit backend/.env and set your MySQL credentials:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DB=ecopackai_db
MYSQL_PORT=3306
```

## 3) Create MySQL Database and Tables

Create database:

```sql
CREATE DATABASE ecopackai_db;
```

The backend includes utilities to create required tables:
- materials table can be created by running backend/run_import.py
- search_logs table is auto-created at API startup

Run importer:

```powershell
cd backend
python run_import.py
```

Note: If backend/materials.csv is not present, the script still creates the materials table and prints a message.

## 4) Start Backend API

```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend URLs:
- API root: http://localhost:8000
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs

## 5) Frontend Setup

Open a new terminal from project root:

```powershell
cd frontend
npm install
npm start
```

Frontend URL:
- http://localhost:3000

The frontend proxy is already set to backend at http://localhost:8000.

## API Usage

POST /api/recommend

Example request body:

```json
{
  "product_name": "phone",
  "product_weight_grams": 250,
  "fragility": "high"
}
```

GET /api/autocomplete?q=pho

## Notes

- Weight and fragility are handled by the rule engine after ML predictions.
- No model retraining is required.
- Replace model files in backend/models with your trained artifacts for production quality outputs.

## Troubleshooting

- If Tailwind shows unknown at-rule warnings in VS Code, workspace settings are already included in .vscode/settings.json.
- If backend cannot connect to MySQL, verify backend/.env values and ensure MySQL service is running.
- If frontend cannot fetch recommendations, make sure backend is running on port 8000.
