let currentSegmentId = 0;
let currentSegmentName = "";

let currentSpending = 0;

let currentSubscription = "";
let currentProbability = 0;

// ======================
// CUSTOMER SEGMENTATION
// ======================

async function segmentCustomer() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/segment-customer",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    age: Number(document.getElementById("age").value),
                    purchase_amount: Number(document.getElementById("purchase_amount").value),
                    review_rating: Number(document.getElementById("review_rating").value),
                    previous_purchases: Number(document.getElementById("previous_purchases").value),
                    purchases_per_year: Number(document.getElementById("purchases_per_year").value)
                })
            }
        );

        const data = await response.json();

        currentSegmentId = data.segment_id;
        currentSegmentName = data.segment_name;

        document.getElementById("segmentResult").innerHTML = `
            <h3>Customer Segment</h3>
            <p><b>Segment ID:</b> ${data.segment_id}</p>
            <p><b>Segment Name:</b> ${data.segment_name}</p>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("segmentResult").innerHTML = `
            <p style="color:red;">Segmentation Failed</p>
        `;
    }
}


// ======================
// SPENDING PREDICTION
// ======================

async function predictSpending() {

    try {

        const payload = {

            age: Number(document.getElementById("age").value),

            gender: document.getElementById("gender").value,

            category: document.getElementById("category").value,

            season: document.getElementById("season").value,

            review_rating: Number(
                document.getElementById("spending_review_rating").value
            ),

            subscription_status:
                document.getElementById("subscription_status").value,

            previous_purchases: Number(
                document.getElementById("spending_previous_purchases").value
            ),

            purchase_frequency_days: Number(
                document.getElementById("spending_frequency_days").value
            )
        };

        const response = await fetch(
            "http://127.0.0.1:8000/predict-spending",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const result = await response.json();

        currentSpending = result.predicted_spending;

        document.getElementById("spendingResult").innerHTML = `
            <h3>Spending Prediction</h3>
            <p><b>Predicted Spending:</b> ₹${result.predicted_spending}</p>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("spendingResult").innerHTML = `
            <p style="color:red;">Error connecting to API</p>
        `;
    }
}


// ======================
// SUBSCRIPTION PREDICTION
// ======================

async function predictSubscription() {

    try {

        const payload = {

            age: Number(document.getElementById("age").value),

            purchase_amount: Number(
                document.getElementById("purchase_amount").value
            ),

            review_rating: Number(
                document.getElementById("review_rating").value
            ),

            previous_purchases: Number(
                document.getElementById("previous_purchases").value
            ),

            purchases_per_year: Number(
                document.getElementById("purchases_per_year").value
            ),

            purchase_frequency_days: Number(
                document.getElementById("subscription_frequency_days").value
            ),

            customer_segment: currentSegmentId,

            gender: document.getElementById("gender").value,

            category: document.getElementById("category").value,

            season: document.getElementById("season").value,

            shipping_type:
                document.getElementById("shipping_type").value
        };

        const response = await fetch(
            "http://127.0.0.1:8000/predict-subscription",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        currentSubscription =
            data.subscription_prediction;

        currentProbability =
            data.subscription_probability;

        document.getElementById("subscriptionResult").innerHTML = `
            <h3>Subscription Prediction</h3>
            <p><b>Prediction:</b> ${data.subscription_prediction}</p>
            <p><b>Probability:</b> ${data.subscription_probability}</p>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("subscriptionResult").innerHTML = `
            <p style="color:red;">Error connecting to API</p>
        `;
    }
}


// ======================
// GEMINI AI INSIGHT
// ======================

async function generateInsight() {

    try {

        if (
            currentSegmentName === "" ||
            currentSubscription === ""
        ) {
            alert(
                "Please run Segmentation, Spending Prediction and Subscription Prediction first."
            );
            return;
        }

        const response = await fetch(
            "http://127.0.0.1:8000/generate-insight",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({

                    segment_name:
                        currentSegmentName,

                    predicted_spending:
                        currentSpending,

                    subscription_prediction:
                        currentSubscription,

                    subscription_probability:
                        currentProbability
                })
            }
        );

        const data = await response.json();

        document.getElementById("aiInsight").innerHTML = `
            <h3>AI Generated Insight</h3>
            <div class="insight-box">
                ${data.insight.replace(/\n/g, "<br>")}
            </div>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("aiInsight").innerHTML = `
            <p style="color:red;">
                AI Insight Generation Failed
            </p>
        `;
    }
}