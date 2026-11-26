(() => {
    const storageKey = "student-performance-latest-prediction";
    const panel = document.getElementById("latest-prediction");
    const valueElement = document.getElementById("latest-prediction-value");
    const statusElement = document.getElementById("prediction-storage-status");

    if (!panel || !valueElement || !statusElement) {
        return;
    }

    function showPrediction(prediction) {
        valueElement.textContent = `${prediction.toFixed(2)} / 100`;
        panel.hidden = false;
    }

    try {
        const savedPrediction = localStorage.getItem(storageKey);
        if (savedPrediction !== null) {
            const prediction = Number(savedPrediction);
            if (Number.isFinite(prediction)) {
                showPrediction(prediction);
            }
        }
    } catch (error) {
        console.error("Could not load the saved prediction.", error);
    }

    const form = document.getElementById("prediction-form");
    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        panel.hidden = false;
        valueElement.textContent = "Calculating...";
        statusElement.textContent = "";

        const values = Object.fromEntries(
            Array.from(new FormData(form).entries(), ([name, value]) => [
                name,
                name === "student_name" ? value : Number(value),
            ])
        );

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(values),
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Prediction failed.");
            }

            const prediction = Number(data.prediction);
            if (!Number.isFinite(prediction)) {
                throw new Error("The server returned an invalid prediction.");
            }

            showPrediction(prediction);
            statusElement.textContent = data.saved === false
                ? data.warning
                : "Saved to student records.";
            try {
                localStorage.setItem(storageKey, String(prediction));
            } catch (error) {
                statusElement.textContent += " Could not save the latest prediction for other pages.";
                console.error("Could not save the latest prediction.", error);
            }
        } catch (error) {
            valueElement.textContent = `Error: ${error.message}`;
        }
    });
})();
