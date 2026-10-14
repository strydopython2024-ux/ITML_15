from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from pathlib import Path
from datetime import datetime

import pandas as pd
import joblib
import json
import gc


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = "smart-farming-secret-key-2026"


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
BACKEND_DIR = PROJECT_DIR / "BACKEND"

USER_FILE = BACKEND_DIR / "user.txt"
DB_FILE = BACKEND_DIR / "DB.txt"

SOIL_MODEL_DIR = BACKEND_DIR / "MODELS_soil"


# ============================================================
# SOIL MODEL FILES
# ============================================================

SOIL_MODEL_PATH = (
    SOIL_MODEL_DIR /
    "soil_prediction_model.pkl"
)

SOIL_PREPROCESSOR_PATH = (
    SOIL_MODEL_DIR /
    "soil_preprocessor.pkl"
)

SOIL_ENCODER_PATH = (
    SOIL_MODEL_DIR /
    "soil_label_encoder.pkl"
)


# ============================================================
# MODEL VARIABLES
# ============================================================

soil_model = None
soil_preprocessor = None
soil_label_encoder = None


# ============================================================
# CREATE REQUIRED FILES
# ============================================================

BACKEND_DIR.mkdir(parents=True, exist_ok=True)

if not USER_FILE.exists():
    USER_FILE.touch()

if not DB_FILE.exists():
    DB_FILE.touch()


# ============================================================
# LOAD SOIL MODEL
# ============================================================

def load_soil_models():

    global soil_model
    global soil_preprocessor
    global soil_label_encoder

    # Already loaded
    if (
        soil_model is not None
        and soil_preprocessor is not None
        and soil_label_encoder is not None
    ):
        return True

    try:

        print("\n========================================")
        print("LOADING SOIL PREDICTION MODEL")
        print("========================================")

        print("Model:")
        print(SOIL_MODEL_PATH)

        print("Preprocessor:")
        print(SOIL_PREPROCESSOR_PATH)

        print("Label Encoder:")
        print(SOIL_ENCODER_PATH)

        # Check files
        if not SOIL_MODEL_PATH.exists():
            print("ERROR: Soil model file not found.")
            return False

        if not SOIL_PREPROCESSOR_PATH.exists():
            print("ERROR: Soil preprocessor not found.")
            return False

        if not SOIL_ENCODER_PATH.exists():
            print("ERROR: Soil label encoder not found.")
            return False

        # Load model
        soil_model = joblib.load(
            SOIL_MODEL_PATH
        )

        print("Soil model loaded.")

        # Load preprocessor
        soil_preprocessor = joblib.load(
            SOIL_PREPROCESSOR_PATH
        )

        print("Soil preprocessor loaded.")

        # Load encoder
        soil_label_encoder = joblib.load(
            SOIL_ENCODER_PATH
        )

        print("Soil label encoder loaded.")

        print("========================================")
        print("SOIL MODEL LOADED SUCCESSFULLY")
        print("========================================")

        return True

    except Exception as e:

        print("\n========================================")
        print("SOIL MODEL LOADING ERROR")
        print("========================================")

        print(repr(e))

        import traceback
        traceback.print_exc()

        soil_model = None
        soil_preprocessor = None
        soil_label_encoder = None

        return False


# ============================================================
# USER FUNCTIONS
# ============================================================

def read_users():

    users = []

    try:

        if not USER_FILE.exists():
            return users

        with open(
            USER_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                parts = line.split("|", 2)

                if len(parts) == 3:

                    name = parts[0].strip()
                    email = parts[1].strip().lower()
                    password_hash = parts[2].strip()

                    users.append({
                        "name": name,
                        "email": email,
                        "password": password_hash
                    })

    except Exception as e:

        print("Read users error:", repr(e))

    return users


def find_user(email):

    email = email.strip().lower()

    users = read_users()

    for user in users:

        if user["email"] == email:
            return user

    return None


def save_user(name, email, password):

    email = email.strip().lower()
    name = name.strip()

    password_hash = generate_password_hash(
        password
    )

    with open(
        USER_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{name}|{email}|{password_hash}\n"
        )

    print("\nUSER SAVED")
    print("Name:", name)
    print("Email:", email)


# ============================================================
# LOGIN REQUIRED DECORATOR
# ============================================================

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not session.get("user_email"):

            return redirect(
                url_for("login")
            )

        return function(*args, **kwargs)

    return wrapper


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    if session.get("user_email"):

        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        print("\n================================")
        print("LOGIN ATTEMPT")
        print("Email:", email)
        print("================================")

        user = find_user(email)

        if user is None:

            print("LOGIN FAILED: USER NOT FOUND")

            return render_template(
                "login.html",
                error="Account not found. Please register first."
            )

        try:

            password_valid = check_password_hash(
                user["password"],
                password
            )

        except Exception as e:

            print(
                "PASSWORD CHECK ERROR:",
                repr(e)
            )

            password_valid = False

        if not password_valid:

            print(
                "LOGIN FAILED: INVALID PASSWORD"
            )

            return render_template(
                "login.html",
                error="Incorrect password."
            )

        session["user_email"] = user["email"]
        session["user_name"] = user["name"]

        print("LOGIN SUCCESS")
        print("User:", user["name"])

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "login.html"
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not name or not email or not password:

            return render_template(
                "register.html",
                error="All fields are required."
            )

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        if len(password) < 6:

            return render_template(
                "register.html",
                error="Password must contain at least 6 characters."
            )

        existing_user = find_user(email)

        if existing_user:

            return render_template(
                "register.html",
                error="An account with this email already exists."
            )

        try:

            save_user(
                name,
                email,
                password
            )

            print(
                "REGISTRATION SUCCESS:",
                email
            )

            return redirect(
                url_for("login")
            )

        except Exception as e:

            print(
                "REGISTRATION ERROR:",
                repr(e)
            )

            return render_template(
                "register.html",
                error="Unable to create account."
            )

    return render_template(
        "register.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# SAVE SOIL PREDICTION
# ============================================================

def save_prediction(
    soil,
    confidence,
    inputs
):

    try:

        email = session.get(
            "user_email",
            ""
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        record = {
            "timestamp": timestamp,
            "email": email,
            "soil": str(soil),
            "soil_confidence": round(
                float(confidence),
                2
            ),
            "inputs": inputs
        }

        with open(
            DB_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )

        print(
            "Prediction history saved."
        )

    except Exception as e:

        print(
            "History save error:",
            repr(e)
        )


# ============================================================
# GET USER PREDICTIONS
# ============================================================

def get_user_predictions():

    predictions = []

    email = session.get(
        "user_email",
        ""
    ).strip().lower()

    if not email:
        return predictions

    if not DB_FILE.exists():
        return predictions

    try:

        with open(
            DB_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                try:

                    record = json.loads(line)

                    if (
                        record.get("email", "")
                        .strip()
                        .lower()
                        == email
                    ):

                        predictions.append(
                            record
                        )

                except json.JSONDecodeError:

                    # Ignore old/malformed records
                    continue

    except Exception as e:

        print(
            "History read error:",
            repr(e)
        )

    predictions.reverse()

    return predictions


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    predictions = get_user_predictions()

    latest = (
        predictions[0]
        if predictions
        else None
    )

    return render_template(
        "dashboard.html",
        predictions=predictions,
        latest=latest,
        user_name=session.get(
            "user_name",
            "User"
        )
    )


# ============================================================
# SOIL PREDICTION PAGE
# ============================================================

@app.route("/prediction")
@login_required
def prediction():

    return render_template(
        "prediction.html",
        user_name=session.get(
            "user_name",
            "User"
        )
    )


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
@login_required
def about():

    return render_template(
        "about.html",
        user_name=session.get(
            "user_name",
            "User"
        )
    )


# ============================================================
# MODEL STATUS
# ============================================================

@app.route("/model-status")
@login_required
def model_status():

    return jsonify({

        "soil_model": {

            "model":
                SOIL_MODEL_PATH.exists(),

            "preprocessor":
                SOIL_PREPROCESSOR_PATH.exists(),

            "encoder":
                SOIL_ENCODER_PATH.exists()
        }

    })


# ============================================================
# SOIL PREDICTION
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
@login_required
def predict():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message":
                    "No prediction data received."
            }), 400

        print("\n========================================")
        print("NEW SOIL PREDICTION")
        print("========================================")

        print("Input:")
        print(data)

        # ------------------------------------------------
        # LOAD SOIL MODEL
        # ------------------------------------------------

        if not load_soil_models():

            return jsonify({
                "success": False,
                "message":
                    "Unable to load soil prediction model."
            }), 500

        # ------------------------------------------------
        # READ INPUTS
        # ------------------------------------------------

        season = str(
            data.get(
                "SEASON",
                ""
            )
        ).strip()

        water_source = str(
            data.get(
                "WATER_SOURCE",
                ""
            )
        ).strip()

        try:

            soil_ph = float(
                data.get("SOIL_PH")
            )

            temp = float(
                data.get("TEMP")
            )

            humidity = float(
                data.get("RELATIVE_HUMIDITY")
            )

            n = float(
                data.get("N")
            )

            p = float(
                data.get("P")
            )

            k = float(
                data.get("K")
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({
                "success": False,
                "message":
                    "Please enter valid numeric values."
            }), 400

        # ------------------------------------------------
        # VALIDATION
        # ------------------------------------------------

        if not season:

            return jsonify({
                "success": False,
                "message":
                    "Season is required."
            }), 400

        if not water_source:

            return jsonify({
                "success": False,
                "message":
                    "Water source is required."
            }), 400

        if not 0 <= soil_ph <= 14:

            return jsonify({
                "success": False,
                "message":
                    "Soil pH must be between 0 and 14."
            }), 400

        if not -50 <= temp <= 70:

            return jsonify({
                "success": False,
                "message":
                    "Temperature must be between -50 and 70 °C."
            }), 400

        if not 0 <= humidity <= 100:

            return jsonify({
                "success": False,
                "message":
                    "Relative humidity must be between 0 and 100%."
            }), 400

        if n < 0 or p < 0 or k < 0:

            return jsonify({
                "success": False,
                "message":
                    "N, P and K cannot be negative."
            }), 400

        # ------------------------------------------------
        # CREATE INPUT DATAFRAME
        # ------------------------------------------------

        soil_input = pd.DataFrame([{

            "SEASON": season,

            "WATER_SOURCE":
                water_source,

            "SOIL_PH":
                soil_ph,

            "TEMP":
                temp,

            "RELATIVE_HUMIDITY":
                humidity,

            "N":
                n,

            "P":
                p,

            "K":
                k

        }])

        print("\nSoil input:")
        print(soil_input)

        # ------------------------------------------------
        # PREPROCESS
        # ------------------------------------------------

        soil_transformed = (
            soil_preprocessor.transform(
                soil_input
            )
        )

        print(
            "Preprocessing completed."
        )

        # ------------------------------------------------
        # MODEL PREDICTION
        # ------------------------------------------------

        raw_prediction = (
            soil_model.predict(
                soil_transformed
            )[0]
        )

        print(
            "Raw prediction:",
            raw_prediction
        )

        # ------------------------------------------------
        # DECODE LABEL
        # ------------------------------------------------

        soil_prediction = (
            soil_label_encoder
            .inverse_transform(
                [raw_prediction]
            )[0]
        )

        # ------------------------------------------------
        # CONFIDENCE
        # ------------------------------------------------

        confidence = 0.0

        if hasattr(
            soil_model,
            "predict_proba"
        ):

            probabilities = (
                soil_model.predict_proba(
                    soil_transformed
                )[0]
            )

            confidence = (
                float(
                    max(probabilities)
                    * 100
                )
            )

        print(
            "Predicted soil:",
            soil_prediction
        )

        print(
            "Confidence:",
            confidence
        )

        # ------------------------------------------------
        # SAVE HISTORY
        # ------------------------------------------------

        save_prediction(
            soil_prediction,
            confidence,
            data
        )

        # ------------------------------------------------
        # MEMORY CLEANUP
        # ------------------------------------------------

        del soil_input
        del soil_transformed

        gc.collect()

        # ------------------------------------------------
        # RESPONSE
        # ------------------------------------------------

        return jsonify({

            "success":
                True,

            "soil_type":
                str(
                    soil_prediction
                ),

            "soil_confidence":
                f"{confidence:.2f}%",

            "inputs":
                data,

            "message":
                (
                    f"The predicted soil type is "
                    f"{soil_prediction}."
                )
        })

    except Exception as e:

        print("\n========================================")
        print("SOIL PREDICTION ERROR")
        print("========================================")

        print(
            repr(e)
        )

        import traceback

        traceback.print_exc()

        return jsonify({

            "success":
                False,

            "message":
                f"Prediction failed: {str(e)}"

        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "application":
            "Smart Farming Soil Prediction",
        "model":
            "Soil Prediction Only"
    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("SMART FARMING SOIL PREDICTION")
    print("========================================")

    print(
        "Backend:",
        BACKEND_DIR
    )

    print(
        "Soil model:",
        SOIL_MODEL_PATH
    )

    print(
        "Crop model: DISABLED"
    )

    print(
        "Server: http://127.0.0.1:5000"
    )

    print("========================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )