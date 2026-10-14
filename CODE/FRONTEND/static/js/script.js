document.addEventListener("DOMContentLoaded", function () {

    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }


    // ========================================================
    // PREDICTION FORM
    // ========================================================

    const predictionForm =
        document.getElementById("predictionForm");

    const predictButton =
        document.getElementById("predictButton");


    if (predictionForm) {

        predictionForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                if (predictButton) {

                    predictButton.disabled = true;

                    predictButton.innerHTML = `
                        <span class="animate-pulse">
                            Predicting...
                        </span>
                    `;
                }


                try {

                    const formData =
                        new FormData(predictionForm);

                    const data = {};


                    formData.forEach(
                        (value, key) => {

                            data[key] = value;

                        }
                    );


                    console.log(
                        "Sending prediction data:",
                        data
                    );


                    const response =
                        await fetch(
                            "/predict",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify(data)
                            }
                        );


                    const result =
                        await response.json();


                    console.log(
                        "Prediction response:",
                        result
                    );


                    if (!response.ok ||
                        !result.success) {

                        alert(
                            result.message ||
                            "Prediction failed."
                        );

                        return;
                    }


                    // ==================================================
                    // SHOW RESULT
                    // ==================================================

                    const cropResult =
                        document.getElementById(
                            "cropResult"
                        );

                    const confidenceResult =
                        document.getElementById(
                            "confidenceResult"
                        );

                    const resultModal =
                        document.getElementById(
                            "resultModal"
                        );


                    if (cropResult) {

                        cropResult.textContent =
                            result.crop ||
                            result.soil_type ||
                            "Unknown";

                    }


                    if (confidenceResult) {

                        confidenceResult.textContent =
                            result.confidence ||
                            "N/A";

                    }


                    if (resultModal) {

                        resultModal.classList.remove(
                            "hidden"
                        );

                        resultModal.classList.add(
                            "flex"
                        );

                    }

                }

                catch (error) {

                    console.error(
                        "Prediction error:",
                        error
                    );

                    alert(
                        "Unable to connect to the prediction server."
                    );

                }

                finally {

                    if (predictButton) {

                        predictButton.disabled = false;

                        predictButton.innerHTML = `
                            <i data-lucide="sprout"
                               class="w-5 h-5"></i>
                            Predict Crop
                        `;

                        if (typeof lucide !== "undefined") {
                            lucide.createIcons();
                        }

                    }

                }

            }
        );

    }


    // ========================================================
    // CLOSE RESULT MODAL
    // ========================================================

    const closeModal =
        document.getElementById("closeModal");

    const resultModal =
        document.getElementById("resultModal");


    if (closeModal && resultModal) {

        closeModal.addEventListener(
            "click",
            function () {

                resultModal.classList.add(
                    "hidden"
                );

                resultModal.classList.remove(
                    "flex"
                );

            }
        );


        resultModal.addEventListener(
            "click",
            function (event) {

                if (event.target === resultModal) {

                    resultModal.classList.add(
                        "hidden"
                    );

                    resultModal.classList.remove(
                        "flex"
                    );

                }

            }
        );

    }


    // ========================================================
    // ESCAPE KEY
    // ========================================================

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Escape" &&
                resultModal) {

                resultModal.classList.add(
                    "hidden"
                );

                resultModal.classList.remove(
                    "flex"
                );

            }

        }
    );


    // ========================================================
    // PASSWORD TOGGLE
    // ========================================================

    const togglePassword =
        document.getElementById(
            "togglePassword"
        );

    const password =
        document.getElementById(
            "password"
        );


    if (togglePassword && password) {

        togglePassword.addEventListener(
            "click",
            function () {

                if (password.type === "password") {

                    password.type = "text";

                    togglePassword.innerHTML =
                        '<i data-lucide="eye-off"></i>';

                } else {

                    password.type = "password";

                    togglePassword.innerHTML =
                        '<i data-lucide="eye"></i>';

                }

                if (typeof lucide !== "undefined") {
                    lucide.createIcons();
                }

            }
        );

    }


    // ========================================================
    // INITIALIZE ICONS
    // ========================================================

    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }

});