import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app

client = TestClient(app)

class TestAPI:
    
    def test_health_check(self):
        """Test de l'endpoint de santé"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert "status" in response.json()
    
    def test_root(self):
        """Test de l'endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "active"
    
    def test_analyze_keyword(self):
        """Test d'analyse de keyword"""
        response = client.post("/api/analyze/keyword", json={"keyword": "python"})
        assert response.status_code == 200
        data = response.json()
        assert data["keyword"] == "python"
        assert "search_volume" in data
        assert "difficulty" in data
        assert "cpc" in data
    
    def test_analyze_keyword_empty(self):
        """Test avec keyword vide"""
        response = client.post("/api/analyze/keyword", json={"keyword": ""})
        assert response.status_code == 400
    
    def test_generate_content(self):
        """Test de génération de contenu"""
        response = client.post("/api/generate/content", json={
            "keyword": "test",
            "content_type": "article",
            "language": "fr",
            "tone": "professional"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["keyword"] == "test"
        assert "generated_content" in data
        assert "word_count" in data
    
    def test_analyze_backlinks(self):
        """Test d'analyse de backlinks"""
        response = client.get("/api/analyze/backlinks?domain=example.com")
        assert response.status_code == 200
        data = response.json()
        assert data["domain"] == "example.com"
        assert "backlink_count" in data
    
    def test_trending_keywords(self):
        """Test des keywords tendance"""
        response = client.get("/api/trending/keywords?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "trending_keywords" in data
        assert len(data["trending_keywords"]) <= 5
    
    def test_batch_analyze(self):
        """Test d'analyse batch"""
        response = client.get("/api/batch/analyze?keywords=python&keywords=javascript")
        assert response.status_code == 200
        data = response.json()
        assert data["total_analyzed"] == 2
        assert len(data["results"]) == 2
    
    def test_batch_analyze_limit(self):
        """Test de limite batch"""
        keywords = [f"keyword{i}" for i in range(101)]
        params = "&".join([f"keywords={kw}" for kw in keywords])
        response = client.get(f"/api/batch/analyze?{params}")
        assert response.status_code == 400
    
    def test_pricing(self):
        """Test endpoint pricing"""
        response = client.get("/api/pricing")
        assert response.status_code == 200
        data = response.json()
        assert "plans" in data
        assert len(data["plans"]) == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
