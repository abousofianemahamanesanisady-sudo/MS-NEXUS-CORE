import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_root():
    r=client.get("/"); assert r.status_code==200 and r.json()["version"]=="2.2.0"
def test_health(): assert client.get("/health").json()["status"]=="ok"
def test_api_requires_key(): assert client.get("/v1/models").status_code==401
