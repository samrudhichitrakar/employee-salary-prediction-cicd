from flask import Flask, request, render_template_string, jsonify
from sklearn.linear_model import LinearRegression
import pandas as pd
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
REQUEST_COUNT = Counter("salary_prediction_requests_total", "Total salary prediction requests")
PREDICTION_TIME = Histogram("salary_prediction_seconds", "Time spent predicting salary")

# Small synthetic educational dataset; not suitable for real compensation decisions.
DATA = pd.DataFrame({
    "experience_years": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15],
    "education_level": [0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3],
    "salary": [240000, 280000, 320000, 360000, 410000, 470000, 520000, 570000,
               620000, 680000, 760000, 880000, 1050000]
})
FEATURES = ["experience_years", "education_level"]
MODEL = LinearRegression().fit(DATA[FEATURES], DATA["salary"])

PAGE = """
<!doctype html>
<html><head><title>Employee Salary Prediction</title>
<style>
body{font-family:Arial;max-width:650px;margin:40px auto;padding:20px;background:#f4f7fb}
main{background:white;padding:28px;border-radius:12px;box-shadow:0 2px 12px #ddd}
label{display:block;margin-top:16px}input,select,button{padding:10px;width:100%;margin-top:6px;box-sizing:border-box}
button{background:#155eef;color:white;border:0;border-radius:6px;margin-top:20px}
.result{background:#e8f7ed;padding:14px;margin-top:20px;border-radius:6px}
.small{font-size:13px;color:#555}
</style></head><body><main>
<h1>Employee Salary Prediction</h1>
<p>Estimate annual salary from experience and education level.</p>
<form method="post">
<label>Years of experience (0–40)</label>
<input type="number" name="experience" min="0" max="40" step="0.5" required value="{{ experience or 3 }}">
<label>Education level</label>
<select name="education">
<option value="0" {% if education == '0' %}selected{% endif %}>Diploma / High school</option>
<option value="1" {% if education == '1' %}selected{% endif %}>Bachelor's degree</option>
<option value="2" {% if education == '2' %}selected{% endif %}>Master's degree</option>
<option value="3" {% if education == '3' %}selected{% endif %}>Doctorate / Advanced</option>
</select>
<button type="submit">Predict Salary</button></form>
{% if prediction is not none %}<div class="result"><b>Estimated annual salary:</b> ₹{{ "{:,.0f}".format(prediction) }}</div>{% endif %}
<p class="small">Educational demo using synthetic sample data. The estimate is not a real salary offer and should not be used for employment decisions.</p>
</main></body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    REQUEST_COUNT.inc()
    prediction = None
    experience = ""
    education = "1"
    if request.method == "POST":
        experience = request.form.get("experience", "0")
        education = request.form.get("education", "1")
        try:
            exp = float(experience)
            edu = int(education)
            if not 0 <= exp <= 40 or edu not in (0, 1, 2, 3):
                raise ValueError
            with PREDICTION_TIME.time():
                prediction = float(MODEL.predict(pd.DataFrame(
                    [[exp, edu]], columns=FEATURES))[0])
            prediction = max(0, prediction)
        except (ValueError, TypeError):
            prediction = None
    return render_template_string(PAGE, prediction=prediction,
                                  experience=experience, education=education)

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
