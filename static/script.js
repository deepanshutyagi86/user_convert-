document.getElementById('predict-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const data = {
        session_time: parseFloat(document.getElementById('session_time').value),
        pages_viewed: parseInt(document.getElementById('pages_viewed').value),
        past_visits: parseInt(document.getElementById('past_visits').value),
        traffic_source: document.getElementById('traffic_source').value,
        user_device: document.getElementById('user_device').value
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            alert('Error: ' + error.error);
            return;
        }

        const result = await response.json();
        const resultDiv = document.getElementById('result');
        const predictionText = document.getElementById('prediction-text');
        predictionText.textContent = result.prediction;
        resultDiv.style.display = 'block';
    } catch (error) {
        alert('Something went wrong: ' + error.message);
    }
});