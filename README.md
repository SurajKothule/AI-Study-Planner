

# AI Study Planner

A web application that helps users plan and optimize their AI learning journey. It predicts study time, generates personalized roadmaps, fetches resources, and provides interview preparation tools.

## Features
- Predicts study time based on user input
- Generates step-by-step learning roadmaps for any AI topic
- Fetches resources from YouTube, Coursera, and GitHub
- Resume upload and interview question generation
- User activity logging and model retraining

## Project Structure
- `app/` - Flask backend code (APIs, ML, resource fetchers)
- `frontend/` - React frontend code
- `models/` - Saved ML models
- `data/` - User activity and datasets
- `uploads/` - Uploaded resumes

## Setup Instructions

### 1. Clone or Download the Project
Extract the zip or clone the repo:
```
git clone <your-repo-url>
cd AI_Study_Planner
```

### 2. Python Backend Setup
- Make sure you have Python 3.8+
- Create and activate a virtual environment:
  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```
- Install requirements:
  ```
  pip install -r requirements.txt
  ```
- Add your API keys to a `.env` file (see `.env.example` or ask the author)
- Start the backend:
  ```
  python run.py
  ```
  The backend will run at http://127.0.0.1:5000

### 3. Frontend Setup
- Go to the frontend folder:
  ```
  cd frontend
  ```
- Install dependencies:
  ```
  npm install
  ```
- Start the frontend:
  ```
  npm start
  ```
  The frontend will run at http://localhost:3000

### 4. Usage
- Open http://localhost:3000 in your browser
- Use the dashboard to generate roadmaps, predict study time, and more
