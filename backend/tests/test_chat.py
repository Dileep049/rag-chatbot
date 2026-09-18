from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_valid_question():
    response = client.post("/api/chat", json={"question": "My Aadhaar card is lost. What should I do?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0

def test_chat_empty_question():
    response = client.post("/api/chat", json={"question": "   "})
    assert response.status_code == 400

def test_chat_out_of_domain():
    response = client.post("/api/chat", json={"question": "Who won the FIFA World Cup 2026?"})
    assert response.status_code == 200
    data = response.json()
    assert "could not find sufficient information" in data["answer"].lower() or len(data["sources"]) == 0

def test_chat_with_conversation_history():
    history = [
        {"role": "user", "content": "My Aadhaar card is lost."},
        {"role": "assistant", "content": "Here is the lost Aadhaar procedure..."}
    ]
    response = client.post("/api/chat", json={
        "question": "What documents do I need?",
        "history": history
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data

def test_chat_telugu_question():
    response = client.post("/api/chat", json={"question": "నా ఆధార్ కార్డు పోయింది. నేను ఏమి చేయాలి?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0

def test_chat_mixed_language_question():
    response = client.post("/api/chat", json={"question": "Aadhaar card lost ayindi, ippudu em cheyyali?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0
