import os
import io
from fastapi.testclient import TestClient
from app.main import app
from app.config import ADMIN_EMAIL, ADMIN_PASSWORD

client = TestClient(app)

def get_admin_headers():
    res = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_unauthenticated_document_access():
    res = client.get("/api/documents")
    assert res.status_code == 401

def test_admin_list_documents():
    headers = get_admin_headers()
    res = client.get("/api/documents", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "documents" in data
    assert "total" in data

def test_upload_and_delete_txt_document():
    headers = get_admin_headers()
    
    # Cleanup previous test artifact if present
    client.delete("/api/documents/test_autoupload_doc.txt", headers=headers)

    file_content = b"## Section 1\nOfficial test document for automated backend testing."
    file_data = {
        "file": ("test_autoupload_doc.txt", io.BytesIO(file_content), "text/plain")
    }
    form_data = {"category": "schemes", "overwrite": "true"}

    # Upload
    upload_res = client.post("/api/documents/upload", headers=headers, files=file_data, data=form_data)
    if upload_res.status_code != 200:
        print(f"Upload failed with status {upload_res.status_code}: {upload_res.json()}")
    assert upload_res.status_code == 200
    assert upload_res.json()["status"] == "Indexed"

    # Delete
    del_res = client.delete("/api/documents/test_autoupload_doc.txt", headers=headers)
    assert del_res.status_code == 200

def test_invalid_file_type_upload():
    headers = get_admin_headers()
    file_data = {
        "file": ("malicious_script.exe", io.BytesIO(b"binary content"), "application/octet-stream")
    }
    form_data = {"category": "schemes"}

    res = client.post("/api/documents/upload", headers=headers, files=file_data, data=form_data)
    assert res.status_code == 400
    assert "Unsupported file type" in res.json()["detail"]
