# Smart Farming Soil Prediction Using Machine Learning

> A Flask-based machine learning application that predicts soil type from agricultural and environmental parameters and provides soil-based crop recommendations.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [How the System Works](#how-the-system-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Machine Learning Model](#machine-learning-model)
- [Input Features](#input-features)
- [Soil-to-Crop Recommendation](#soil-to-crop-recommendation)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Using the Application](#using-the-application)
- [Model Files](#model-files)
- [Data and Training](#data-and-training)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Project Objective](#project-objective)
- [Conclusion](#conclusion)

---

## Project Overview

**Smart Farming Soil Prediction Using Machine Learning** is a web-based smart agriculture application that uses a trained machine learning model to predict soil type from agricultural and environmental parameters.

The application accepts:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Soil pH
- Temperature
- Relative Humidity
- Season
- Water Source

The backend preprocesses these values and sends them to the trained soil prediction model. The predicted soil class is then decoded into a readable soil name.

After the soil type is identified, the frontend uses a predefined soil-to-crop mapping to display suitable crops.

The supplied project contains a Flask application, trained model artifacts, datasets, Jupyter notebooks, frontend templates, JavaScript, and supporting files. fileciteturn24file0L98-L139

---

## Key Features

- User registration and login
- Password hashing for newly registered users
- Responsive web dashboard
- Soil type prediction using machine learning
- Soil-based crop recommendation
- Prediction history
- Prediction result popup
- Client-side input validation
- Flask backend
- Saved preprocessing pipeline
- Saved label encoder
- Saved trained model
- Model status endpoint
- Health endpoint
- No Docker required
- No paid API required

---

## How the System Works

```text
                    ┌──────────────────────┐
                    │     User Register    │
                    │       / Login        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Dashboard       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Soil Prediction     │
                    │       Form           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Input Validation     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Saved Preprocessor   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Soil ML Model        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Predicted Soil Type  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Soil → Crop Mapping  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Recommended Crops    │
                    └──────────────────────┘
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Frontend | HTML, JavaScript |
| UI | TailwindCSS / project frontend styling |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib / Pickle artifacts |
| Development | Jupyter Notebook |
| Authentication | Flask session + password hashing |
| Storage | Local text files |
| Deployment | Local Flask server |

---

## Project Structure

The current project structure is:

```text
SMART FARMING SOIL PREDICTION ML
│
├── requirement.txt
├── str.txt
│
├── BACKEND
│   ├── create_test_dataset.py
│   ├── DATA_PREPROCESSING.ipynb
│   ├── DB.txt
│   ├── inspect_dataset.ipynb
│   ├── train_soil_model.ipynb
│   ├── user.txt
│   │
│   └── MODELS_soil
│       ├── soil_label_encoder.pkl
│       ├── soil_model_comparison.pkl
│       ├── soil_model_metadata.json
│       ├── soil_prediction_model.pkl
│       └── soil_preprocessor.pkl
│
├── DATA_SET
│   ├── Crop recommendation dataset.csv
│   └── test_dataset_all_crops.csv
│
└── FRONTEND
    ├── app.py
    │
    ├── static
    │   ├── css
    │   │   └── style.css
    │   ├── images
    │   └── js
    │       ├── app.js
    │       └── script.js
    │
    └── templates
        ├── about.html
        ├── dashboard.html
        ├── login.html
        ├── prediction.html
        └── register.html
```

This structure is based on the supplied project files. fileciteturn24file0L98-L139

---

# Machine Learning Model

## Model Purpose

The trained model predicts the target variable:

```text
SOIL
```

The application does not ask the user to provide the soil type. Soil type is the model's prediction output.

## Prediction Pipeline

The application follows this sequence:

```text
Raw User Input
      ↓
Validation
      ↓
Feature DataFrame
      ↓
Saved Preprocessor
      ↓
Trained Soil Model
      ↓
Encoded Prediction
      ↓
Label Encoder
      ↓
Readable Soil Type
```

The backend uses the saved preprocessing and model artifacts rather than retraining the model every time the application starts.

---

# Input Features

The model expects the following eight input features:

| Feature | Type | Description |
|---|---|---|
| `SEASON` | Categorical | Agricultural season |
| `WATER_SOURCE` | Categorical | Main source of irrigation/water |
| `SOIL_PH` | Numeric | Soil pH value |
| `TEMP` | Numeric | Temperature |
| `RELATIVE_HUMIDITY` | Numeric | Relative humidity |
| `N` | Numeric | Nitrogen value |
| `P` | Numeric | Phosphorus value |
| `K` | Numeric | Potassium value |

These feature names must remain consistent with the saved preprocessing pipeline.

---

# Soil-to-Crop Recommendation

Once the ML model predicts the soil type, the application recommends crops using a predefined mapping.

| Predicted Soil | Recommended Crops |
|---|---|
| Alluvial | Rice, Wheat, Sugarcane, Maize |
| Black | Cotton, Soybean, Sorghum |
| Red | Groundnut, Millets, Pulses |
| Laterite | Cashew, Tea, Coffee |
| Sandy | Groundnut, Watermelon, Carrot |
| Clay | Rice, Wheat, Cabbage |
| Loamy | Wheat, Maize, Vegetables |

### Important

The current application uses the predicted soil as the basis for crop recommendation. The active frontend workflow does **not** require a separate crop ML prediction model.

---

# Prerequisites

Before running the project, install the following:

- Python 3.10+ recommended
- pip
- Git (optional)
- VS Code or another Python IDE (optional)
- A modern web browser

The project does not require:

- Docker
- Redis
- A paid API
- An API key
- Cloud services

---

# Installation

## Step 1 — Open the Project

Clone the repository if it is stored in Git:

```bash
git clone <YOUR_REPOSITORY_URL>
```

Or download/extract the project and open the project folder.

The final project root should contain:

```text
requirement.txt
BACKEND/
DATA_SET/
FRONTEND/
```

---

## Step 2 — Open a Terminal in the Project Root

Example:

```bash
cd "SMART FARMING SOIL PREDICTION ML"
```

Verify the folders:

### Windows

```cmd
dir
```

You should see:

```text
BACKEND
DATA_SET
FRONTEND
requirement.txt
```

---

## Step 3 — Create a Virtual Environment

Creating a virtual environment is recommended so the project dependencies do not interfere with other Python projects.

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

If PowerShell blocks activation, use:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Conda Alternative

If you prefer Anaconda:

```bash
conda create -n smart_farming python=3.11
```

Activate it:

```bash
conda activate smart_farming
```

Use **either** the virtual environment method or Conda. Do not create multiple environments unnecessarily.

---

## Step 4 — Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## Step 5 — Install Dependencies

From the project root:

```bash
pip install -r requirement.txt
```

If the requirement file is named differently in your copy of the project, use the exact filename.

Verify Flask:

```bash
python -c "import flask; print('Flask:', flask.__version__)"
```

Verify the ML libraries:

```bash
python -c "import pandas, numpy, sklearn, joblib; print('ML dependencies OK')"
```

If all commands complete successfully, the environment is ready.

---

# Running the Application

## Step 1 — Navigate to the Frontend

From the project root:

```bash
cd FRONTEND
```

---

## Step 2 — Start Flask

```bash
python app.py
```

You should see Flask start on:

```text
http://127.0.0.1:5000
```

---

## Step 3 — Open the Browser

Open:

```text
http://127.0.0.1:5000
```

Do not open the HTML files directly from the `templates` folder.

The pages must be served through Flask.

---

# First-Time Usage

## 1. Register

Open the application and select **Register**.

Enter:

```text
Name
Email
Password
Confirm Password
```

Submit the registration form.

---

## 2. Login

Use the same email and password to log in.

---

## 3. Open Dashboard

After successful login, the application opens the dashboard.

---

## 4. Open Soil Prediction

Select:

```text
Soil Prediction
```

---

## 5. Enter Required Values

Example:

```text
Nitrogen: 90
Phosphorus: 42
Potassium: 43
Soil pH: 6.5
Temperature: 25
Relative Humidity: 70
Season: Kharif
Water Source: Rainfall
```

---

## 6. Predict Soil

Click:

```text
Predict Soil
```

The frontend sends the values to:

```text
POST /predict
```

The Flask backend then:

1. Validates the request.
2. Creates the model input.
3. Applies the saved soil preprocessor.
4. Runs the trained soil model.
5. Decodes the predicted class.
6. Saves the prediction history.
7. Returns the predicted soil to the frontend.

---

## 7. View Recommendation

The frontend receives the predicted soil and determines suitable crops using the soil-to-crop mapping.

For example:

```text
Predicted Soil:
Black

Recommended Crops:
Cotton, Soybean, Sorghum
```

---

# Model Files

The trained model artifacts are located at:

```text
BACKEND/MODELS_soil/
```

The project contains:

```text
soil_prediction_model.pkl
soil_preprocessor.pkl
soil_label_encoder.pkl
soil_model_comparison.pkl
soil_model_metadata.json
```

These files are part of the current project structure. fileciteturn24file0L112-L117

### `soil_prediction_model.pkl`

The trained machine learning model used to predict soil type.

### `soil_preprocessor.pkl`

The preprocessing pipeline used to transform input data before prediction.

### `soil_label_encoder.pkl`

Converts the model's encoded output into the corresponding soil class.

### `soil_model_comparison.pkl`

Stores model comparison information generated during model development.

### `soil_model_metadata.json`

Contains metadata associated with the trained model.

---

# Dataset

The project contains:

```text
DATA_SET/
├── Crop recommendation dataset.csv
└── test_dataset_all_crops.csv
```

These files are included in the supplied project structure. fileciteturn24file0L119-L120

The soil model uses the required features described in the [Input Features](#input-features) section.

---

# Data and Training

The backend contains notebooks used during development:

```text
BACKEND/
├── DATA_PREPROCESSING.ipynb
├── inspect_dataset.ipynb
└── train_soil_model.ipynb
```

These notebooks are used for activities such as:

- Dataset inspection
- Data preprocessing
- Feature preparation
- Model training
- Model evaluation
- Saving model artifacts

The notebooks are development resources. **You do not need to retrain the model just to run the application** if the supplied model files are already present.

---

# Authentication and Local Storage

The current application uses local files for user information and prediction history.

## User File

```text
BACKEND/user.txt
```

## Prediction History

```text
BACKEND/DB.txt
```

These files are part of the current project structure. fileciteturn24file0L104-L110

Newly registered passwords are stored using password hashing.

---

# Application Routes

The Flask application provides routes/pages including:

| Route | Purpose |
|---|---|
| `/` | Application entry page |
| `/login` | Login |
| `/register` | Registration |
| `/logout` | Logout |
| `/dashboard` | User dashboard |
| `/prediction` | Soil prediction page |
| `/about` | About page |
| `/predict` | Soil prediction API |
| `/health` | Application health check |
| `/model-status` | Model availability/status |

---

# Validation Rules

The application validates input before prediction.

### N, P, K

```text
N >= 0
P >= 0
K >= 0
```

### Soil pH

```text
0 <= SOIL_PH <= 14
```

### Relative Humidity

```text
0 <= RELATIVE_HUMIDITY <= 100
```

### Required Fields

The following must be provided:

```text
SEASON
WATER_SOURCE
SOIL_PH
TEMP
RELATIVE_HUMIDITY
N
P
K
```

---

# Configuration

The application is designed to run locally with the current project structure.

Before starting the application, make sure these relative paths remain unchanged:

```text
BACKEND/MODELS_soil/
FRONTEND/
DATA_SET/
```

The model artifacts must be accessible from the Flask backend.

If you move the model files, update the paths in:

```text
FRONTEND/app.py
```

Do not rename model files unless the backend is updated accordingly.

---

# Health Check

After starting Flask, you can test whether the application is responding.

Open:

```text
http://127.0.0.1:5000/health
```

The response should indicate that the application is running.

The project also provides:

```text
http://127.0.0.1:5000/model-status
```

This can be used to check model availability.

---

# Troubleshooting

## `python` is not recognized

Install Python and make sure Python is added to the system PATH.

Check:

```bash
python --version
```

or:

```bash
py --version
```

---

## `pip` is not recognized

Use:

```bash
python -m pip --version
```

Then install dependencies using:

```bash
python -m pip install -r requirement.txt
```

---

## `ModuleNotFoundError`

Example:

```text
ModuleNotFoundError: No module named 'flask'
```

Activate your environment and reinstall dependencies:

```bash
python -m pip install -r requirement.txt
```

---

## Flask starts but the page does not open

Confirm the terminal shows:

```text
http://127.0.0.1:5000
```

Then open that address manually in the browser.

Do not double-click:

```text
login.html
dashboard.html
prediction.html
```

Flask must serve these templates.

---

## Model not found

Check:

```text
BACKEND/MODELS_soil/
```

The following files must exist:

```text
soil_prediction_model.pkl
soil_preprocessor.pkl
soil_label_encoder.pkl
```

The supplied project currently contains these files. fileciteturn24file0L112-L117

---

## Prediction gives an error

Check:

1. All fields are filled.
2. N, P, and K are not negative.
3. pH is between 0 and 14.
4. Relative humidity is between 0 and 100.
5. Season is selected.
6. Water source is selected.
7. The model files are present.
8. The model and preprocessor came from the same training pipeline.

Then check the Flask terminal for the exact error message.

---

## Login fails

Check:

```text
BACKEND/user.txt
```

If this is a fresh installation, register a new account from the application rather than manually editing password hashes.

---

## Port 5000 is already in use

If another application is using port 5000, stop that application or change the Flask port in `app.py`.

For example:

```python
app.run(host="127.0.0.1", port=5001, debug=True)
```

Then open:

```text
http://127.0.0.1:5001
```

Only change the port if necessary.

---

# Model Retraining

Retraining is **not required for normal usage** because the trained artifacts are already included in:

```text
BACKEND/MODELS_soil/
```

If you modify the dataset or training process, retrain the model using:

```text
BACKEND/train_soil_model.ipynb
```

After retraining, make sure the following artifacts are regenerated consistently:

```text
soil_prediction_model.pkl
soil_preprocessor.pkl
soil_label_encoder.pkl
soil_model_comparison.pkl
soil_model_metadata.json
```

A model and preprocessor from different training runs should not be mixed without verifying compatibility.

---

# Development Mode

For development, run:

```bash
cd FRONTEND
python app.py
```

Keep the Flask terminal open while using the application.

To stop the server:

```text
CTRL + C
```

---

# Advantages

- Easy-to-use web interface
- Machine learning-based soil prediction
- Soil-based crop recommendation
- User authentication
- Prediction history
- Input validation
- Locally stored ML model
- No paid APIs
- No Docker dependency
- Suitable for academic/student projects
- Easy to extend with IoT and precision agriculture features

---

# Limitations

The current project has several practical limitations:

- Crop recommendations are based on a predefined mapping.
- The application currently uses local file storage for users and prediction history.
- Prediction quality depends on the training dataset and trained model.
- The system does not directly collect measurements from physical soil sensors.
- It does not currently provide real-time weather information.
- It should not be treated as a replacement for professional agricultural or soil-laboratory analysis.

---

# Future Enhancements

Possible future improvements include:

- IoT-based soil sensor integration
- Real-time soil moisture monitoring
- Weather API integration
- Automated irrigation recommendation
- Fertilizer recommendation
- Crop disease detection
- Crop yield prediction
- Regional crop recommendations
- Multilingual farmer interface
- Mobile application
- Cloud deployment
- Advanced machine learning/deep learning models
- Real-time farm monitoring dashboard

---

# Project Objective

The objective is to develop a practical smart farming application that uses machine learning to analyze agricultural and environmental parameters, predict soil type, and provide suitable crop recommendations.

The project connects a trained ML model with a Flask web application so that users can obtain predictions through a simple graphical interface rather than directly interacting with notebooks or model files.

---

# Conclusion

**Smart Farming Soil Prediction Using Machine Learning** demonstrates how machine learning can be integrated into a practical smart agriculture web application.

The system accepts important agricultural and environmental parameters, processes them using the saved preprocessing pipeline, predicts the soil type using the trained ML model, and provides suitable crop recommendations based on the predicted soil.

The architecture provides a foundation for future precision-agriculture features such as IoT sensors, weather monitoring, irrigation management, fertilizer recommendations, crop disease detection, and yield prediction.

---

# Quick Start

For someone who already has Python installed, the shortest setup is:

```bash
# 1. Open project root
cd "SMART FARMING SOIL PREDICTION ML"

# 2. Create environment
python -m venv .venv

# 3. Activate environment - Windows
.venv\Scripts\activate

# 4. Install dependencies
python -m pip install --upgrade pip
pip install -r requirement.txt

# 5. Start application
cd FRONTEND
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

Register → Login → Dashboard → Soil Prediction → Enter Values → Predict Soil.

---

# Author

**Smart Farming Soil Prediction Using Machine Learning**

Machine Learning and Smart Agriculture Project.
