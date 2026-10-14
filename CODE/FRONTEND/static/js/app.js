// ============================================================
// SMART FARMING - MAIN FRONTEND JAVASCRIPT
// ============================================================

// -----------------------------
// Soil -> Crop recommendation
// -----------------------------
const soilCropMap = {
    alluvial: ["Rice", "Wheat", "Sugarcane", "Maize"],
    black: ["Cotton", "Soybean", "Sorghum"],
    red: ["Groundnut", "Millets", "Pulses"],
    laterite: ["Cashew", "Tea", "Coffee"],
    sandy: ["Groundnut", "Watermelon", "Carrot"],
    clay: ["Rice", "Wheat", "Cabbage"],
    loamy: ["Wheat", "Maize", "Vegetables"]
};

function getRecommendedCrop(soil) {
    if (!soil) return "Suitable Crops";

    const key = String(soil).trim().toLowerCase();
    const crops = soilCropMap[key];

    return crops ? crops.join(", ") : "Rice, Maize & Vegetables";
}

// -----------------------------
// Password visibility
// -----------------------------
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.type = input.type === "password" ? "text" : "password";
}

// -----------------------------
// Common page initialization
// -----------------------------
document.addEventListener("DOMContentLoaded", function () {

    // Lucide icons
    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }

    // Mobile navigation
    const mobileMenuButton = document.getElementById("mobileMenuButton");
    const mobileMenu = document.getElementById("mobileMenu");

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener("click", function () {
            mobileMenu.classList.toggle("hidden");
        });
    }

    // Dashboard crop recommendations
    document.querySelectorAll(".crop-recommendation").forEach(function (element) {
        const soil = element.dataset.soil;

        if (!soil || soil === "--") {
            element.textContent = "--";
        } else {
            element.textContent = getRecommendedCrop(soil);
        }
    });

    // Prediction page
    initializePredictionPage();
});

// ============================================================
// PREDICTION PAGE
// ============================================================
function initializePredictionPage() {
    const predictionForm = document.getElementById("predictionForm");

    // This page does not exist on login/register/dashboard/about.
    if (!predictionForm) return;

    const predictButton = document.getElementById("predictButton");
    const predictButtonText = document.getElementById("predictButtonText");
    const predictSpinner = document.getElementById("predictSpinner");
    const predictionError = document.getElementById("predictionError");
    const resultModal = document.getElementById("resultModal");
    const closeResultButton = document.getElementById("closeResultButton");
    const modalBackdrop = document.getElementById("modalBackdrop");

    function showPredictionError(message) {
        if (!predictionError) {
            alert(message);
            return;
        }

        predictionError.textContent = message;
        predictionError.classList.remove("hidden");
    }

    function hidePredictionError() {
        if (!predictionError) return;

        predictionError.textContent = "";
        predictionError.classList.add("hidden");
    }

    function setLoading(loading) {
        if (!predictButton) return;

        predictButton.disabled = loading;
        predictButton.classList.toggle("opacity-70", loading);
        predictButton.classList.toggle("cursor-not-allowed", loading);

        if (predictButtonText) {
            predictButtonText.textContent = loading
                ? "Analyzing Soil..."
                : "Predict Soil";
        }

        if (predictSpinner) {
            predictSpinner.classList.toggle("hidden", !loading);
        }
    }

    function openResultModal() {
        if (!resultModal) return;

        resultModal.classList.remove("hidden");
        resultModal.classList.add("flex");
        document.body.classList.add("overflow-hidden");

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }
    }

    function closeResultModal() {
        if (!resultModal) return;

        resultModal.classList.add("hidden");
        resultModal.classList.remove("flex");
        document.body.classList.remove("overflow-hidden");
    }

    if (closeResultButton) {
        closeResultButton.addEventListener("click", closeResultModal);
    }

    if (modalBackdrop) {
        modalBackdrop.addEventListener("click", closeResultModal);
    }

    // Close modal using Escape
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeResultModal();
        }
    });

    predictionForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        hidePredictionError();

        // Get fields safely
        const N = document.getElementById("N")?.value.trim() || "";
        const P = document.getElementById("P")?.value.trim() || "";
        const K = document.getElementById("K")?.value.trim() || "";
        const SOIL_PH = document.getElementById("SOIL_PH")?.value.trim() || "";
        const TEMP = document.getElementById("TEMP")?.value.trim() || "";
        const RELATIVE_HUMIDITY = document.getElementById("RELATIVE_HUMIDITY")?.value.trim() || "";
        const SEASON = document.getElementById("SEASON")?.value || "";
        const WATER_SOURCE = document.getElementById("WATER_SOURCE")?.value || "";

        // Required fields
        if (!N || !P || !K || !SOIL_PH || !TEMP || !RELATIVE_HUMIDITY || !SEASON || !WATER_SOURCE) {
            showPredictionError("Please fill in all required fields.");
            return;
        }

        const nitrogen = Number(N);
        const phosphorus = Number(P);
        const potassium = Number(K);
        const soilPH = Number(SOIL_PH);
        const temperature = Number(TEMP);
        const humidity = Number(RELATIVE_HUMIDITY);

        // Numeric validation
        if ([nitrogen, phosphorus, potassium, soilPH, temperature, humidity].some(Number.isNaN)) {
            showPredictionError("Please enter valid numeric values.");
            return;
        }

        if (nitrogen < 0 || phosphorus < 0 || potassium < 0) {
            showPredictionError("N, P and K values cannot be negative.");
            return;
        }

        if (soilPH < 0 || soilPH > 14) {
            showPredictionError("Soil pH must be between 0 and 14.");
            return;
        }

        if (humidity < 0 || humidity > 100) {
            showPredictionError("Relative humidity must be between 0 and 100.");
            return;
        }

        if (temperature < -50 || temperature > 70) {
            showPredictionError("Please enter a valid temperature between -50 and 70 °C.");
            return;
        }

        const requestData = {
            SEASON: SEASON,
            WATER_SOURCE: WATER_SOURCE,
            SOIL_PH: soilPH,
            TEMP: temperature,
            RELATIVE_HUMIDITY: humidity,
            N: nitrogen,
            P: phosphorus,
            K: potassium
        };

        setLoading(true);

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestData)
            });

            let result;

            try {
                result = await response.json();
            } catch (jsonError) {
                throw new Error("The server returned an invalid response.");
            }

            if (!response.ok || !result.success) {
                throw new Error(
                    result.message ||
                    result.error ||
                    "Unable to complete soil prediction."
                );
            }

            // IMPORTANT:
            // Only the soil model result is used here.
            // Confidence is NOT displayed.
            // Crop is NOT taken from the ML backend.
            const predictedSoil = result.soil_type;

            if (!predictedSoil) {
                throw new Error("The server did not return a predicted soil type.");
            }

            // Hard-coded soil -> crop recommendation
            const recommendedCrop = getRecommendedCrop(predictedSoil);

            // Safe DOM updates - no null.textContent errors
            const resultSoil = document.getElementById("resultSoil");
            const recommendedCropElement = document.getElementById("recommendedCrop");
            const resultMessage = document.getElementById("resultMessage");

            if (resultSoil) {
                resultSoil.textContent = predictedSoil;
            }

            if (recommendedCropElement) {
                recommendedCropElement.textContent = recommendedCrop;
            }

            if (resultMessage) {
                resultMessage.textContent =
                    `Based on the predicted ${predictedSoil} soil type, the recommended crops are ${recommendedCrop}.`;
            }

            openResultModal();

        } catch (error) {
            console.error("Prediction error:", error);
            showPredictionError(
                error.message ||
                "An unexpected error occurred while predicting the soil."
            );
        } finally {
            setLoading(false);
        }
    });
}
