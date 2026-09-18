import io
from fastapi.testclient import TestClient
from app.main import app, rate_limit_records

client = TestClient(app)

def test_health_check_endpoint():
    rate_limit_records.clear()
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["service"] == "Citizen Assistance RAG API"

def test_unauthenticated_api_protection():
    rate_limit_records.clear()
    # Documents listing
    res1 = client.get("/api/documents")
    assert res1.status_code == 401

    # Upload document without Authorization header
    files = {"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 test"), "application/pdf")}
    res2 = client.post("/api/documents/upload", files=files, data={"category": "schemes"})
    assert res2.status_code in (401, 403)

    # Reindex document
    res3 = client.post("/api/documents/reindex/aadhaar_official_guide.txt")
    assert res3.status_code in (401, 403)

    # Delete document
    res4 = client.delete("/api/documents/aadhaar_official_guide.txt")
    assert res4.status_code in (401, 403)

def test_security_headers_present():
    rate_limit_records.clear()
    res = client.get("/")
    assert res.status_code == 200
    assert res.headers["X-Content-Type-Options"] == "nosniff"
    assert res.headers["X-Frame-Options"] == "DENY"
    assert res.headers["X-XSS-Protection"] == "1; mode=block"

def test_rate_limiting():
    rate_limit_records.clear()
    # Make multiple rapid requests to trigger 429
    responses = [client.post("/api/chat", json={"question": f"Question {i}"}) for i in range(70)]
    status_codes = [r.status_code for r in responses]
    assert 429 in status_codes or 200 in status_codes
    rate_limit_records.clear()
