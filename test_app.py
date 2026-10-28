from app import app

def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Employee Salary Prediction" in response.data

def test_health_endpoint():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_prediction_form():
    response = app.test_client().post("/", data={
        "experience": "5", "education": "2"
    })
    assert response.status_code == 200
    assert b"Estimated annual salary" in response.data
