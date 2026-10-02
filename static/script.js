const form = document.getElementById("predictionForm");

const result = document.getElementById("result");


form.addEventListener("submit", async function(event) {

    event.preventDefault();


    // Get input values

    const area =
        Number(document.getElementById("area").value);

    const bedrooms =
        Number(document.getElementById("bedrooms").value);

    const bathrooms =
        Number(document.getElementById("bathrooms").value);

    const floors =
        Number(document.getElementById("floors").value);

    const age =
        Number(document.getElementById("age").value);


    // Validation

    if (
        !area ||
        !bedrooms ||
        !bathrooms ||
        !floors ||
        age < 0
    ) {

        result.className = "result error";

        result.innerHTML =
            "Please enter valid house details.";

        return;
    }


    // Show loading

    result.className = "result";

    result.innerHTML =
        "⏳ Predicting house price...";


    try {

        // Send data to FastAPI

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    area: area,

                    bedrooms: bedrooms,

                    bathrooms: bathrooms,

                    floors: floors,

                    age: age

                })
            }
        );


        const data = await response.json();


        if (data.success) {

            result.className =
                "result success";

            result.innerHTML =
                `🏠 Predicted House Price:
                ₹${data.predicted_price}
                Lakhs`;

        }

        else {

            result.className =
                "result error";

            result.innerHTML =
                "Prediction failed.";

        }


    }

    catch (error) {

        console.error(error);

        result.className =
            "result error";

        result.innerHTML =
            "❌ Unable to connect to FastAPI server.";

    }

});