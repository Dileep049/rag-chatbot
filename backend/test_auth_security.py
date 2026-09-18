import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from fastapi.testclient import TestClient
from app.main import app
from app.config import ADMIN_EMAIL, ADMIN_PASSWORD

client = TestClient(app)

def run_security_tests():
    print("==========================================================")
    print(" Testing Admin Authentication & RBAC Backend Security ")
    print("==========================================================")

    # Test 1: Unprotected Public Chat API
    print("\n--- TEST 1: Public Chat API (Unprotected) ---")
    res = client.post("/api/chat", json={"question": "My Aadhaar card is lost."})
    print(f"Status Code: {res.status_code}")
    assert res.status_code == 200, "Chat API should be public for citizens"
    print("[PASS] Public Chat API accessible without authentication.")

    # Test 2: Protected Admin APIs Without Token
    print("\n--- TEST 2: Admin APIs Without Authentication Token ---")
    res_list = client.get("/api/documents")
    print(f"GET /api/documents Status: {res_list.status_code} ({res_list.json()})")
    assert res_list.status_code == 401, "GET /api/documents must be protected"

    res_upload = client.post("/api/documents/upload")
    print(f"POST /api/documents/upload Status: {res_upload.status_code} ({res_upload.json()})")
    assert res_upload.status_code == 401, "POST /api/documents/upload must be protected"

    res_delete = client.delete("/api/documents/test.pdf")
    print(f"DELETE /api/documents/test.pdf Status: {res_delete.status_code} ({res_delete.json()})")
    assert res_delete.status_code == 401, "DELETE /api/documents must be protected"
    print("[PASS] All Admin APIs block unauthenticated requests with HTTP 401.")

    # Test 3: Invalid Admin Login
    print("\n--- TEST 3: Invalid Credentials Login ---")
    res_invalid = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": "wrong_password_123"})
    print(f"Status Code: {res_invalid.status_code} ({res_invalid.json()})")
    assert res_invalid.status_code == 401
    print("[PASS] Invalid credentials rejected with HTTP 401.")

    # Test 4: Valid Admin Login
    print("\n--- TEST 4: Valid Admin Login & Token Generation ---")
    res_login = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    print(f"Status Code: {res_login.status_code}")
    assert res_login.status_code == 200
    token_data = res_login.json()
    token = token_data["access_token"]
    assert token_data["user"]["role"] == "admin"
    print(f"[PASS] Admin login successful. Token generated for user role '{token_data['user']['role']}'.")

    # Test 5: Authorized Admin API Access
    print("\n--- TEST 5: Admin API Access with Valid Bearer Token ---")
    headers = {"Authorization": f"Bearer {token}"}
    res_authed_list = client.get("/api/documents", headers=headers)
    print(f"GET /api/documents Status: {res_authed_list.status_code}")
    assert res_authed_list.status_code == 200
    print(f"[PASS] Admin list documents returned {res_authed_list.json().get('total')} documents.")

    print("\n==========================================================")
    print(" ALL SECURITY & AUTHORIZATION TESTS PASSED SUCCESSFULLY! ")
    print("==========================================================")

if __name__ == "__main__":
    run_security_tests()
