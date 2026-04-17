from fastapi import FastAPI, HTTPException, Depends, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import httpx
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import hashlib
import json
from auth import AuthManager
from scraper import LegalDataScraper

load_dotenv()

app = FastAPI(
    title="SEO Analyzer Pro API",
    description="Plateforme SaaS d'analyse SEO et génération de contenu",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELS ====================

class KeywordAnalysis(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100)
    search_volume: int = 0
    difficulty: float = Field(0, ge=0, le=100)
    cpc: float = 0.0
    trend: str = "stable"
    
class ContentGenerationRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100)
    content_type: str = Field("article", pattern="^(article|meta|title|description)$")
    language: str = Field("fr", pattern="^(fr|en|es|de)$")
    tone: str = Field("professional", pattern="^(professional|casual|technical)$")
    
class BacklinkAnalysis(BaseModel):
    domain: str
    backlink_count: int = 0
    referring_domains: int = 0
    authority_score: float = 0.0
    top_backlinks: List[str] = []

class UserAnalysis(BaseModel):
    analysis_id: str
    created_at: datetime
    keyword: str
    results: dict

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    plan: str = "free"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    plan: str

# ==================== MOCK DATA & FUNCTIONS ====================

MOCK_KEYWORDS = {
    "python tutorial": {"search_volume": 12100, "difficulty": 45, "cpc": 0.85},
    "web development": {"search_volume": 8900, "difficulty": 62, "cpc": 1.20},
    "machine learning": {"search_volume": 15600, "difficulty": 78, "cpc": 2.15},
    "seo tips": {"search_volume": 3200, "difficulty": 35, "cpc": 0.45},
    "fastapi tutorial": {"search_volume": 1850, "difficulty": 28, "cpc": 0.55},
}

def generate_keyword_data(keyword: str) -> dict:
    """Génère des données d'analyse keywords réalistes"""
    keyword_lower = keyword.lower()
    
    if keyword_lower in MOCK_KEYWORDS:
        base_data = MOCK_KEYWORDS[keyword_lower]
    else:
        # Génération pseudo-aléatoire basée sur le hash du keyword
        hash_val = int(hashlib.md5(keyword_lower.encode()).hexdigest(), 16)
        base_data = {
            "search_volume": 1000 + (hash_val % 50000),
            "difficulty": (hash_val % 100),
            "cpc": round(0.1 + ((hash_val % 300) / 100), 2)
        }
    
    return KeywordAnalysis(
        keyword=keyword,
        search_volume=base_data["search_volume"],
        difficulty=base_data["difficulty"],
        cpc=base_data["cpc"],
        trend="increasing" if hash_val % 3 == 0 else ("stable" if hash_val % 3 == 1 else "declining")
    )

def generate_content(keyword: str, content_type: str, language: str, tone: str) -> str:
    """Génère du contenu SEO optimisé"""
    
    templates = {
        "en": {
            "article": f"## Complete Guide to {keyword}\n\nLearning {keyword} is essential in today's digital landscape. This comprehensive guide covers everything you need to know about {keyword} for {tone} purposes.\n\n### Key Points:\n- Understanding {keyword} fundamentals\n- Best practices for {keyword} implementation\n- Advanced {keyword} techniques\n- Common {keyword} mistakes to avoid",
            "meta": f"{keyword} - Professional Guide | Learn {keyword} Today",
            "title": f"{keyword}: The Complete 2026 Guide for Professionals",
            "description": f"Master {keyword} with our expert guide. Learn proven strategies, best practices, and advanced techniques for {keyword} success."
        },
        "fr": {
            "article": f"## Guide Complet sur {keyword}\n\nMaîtriser {keyword} est essentiel dans le paysage numérique actuel. Ce guide couvre tout ce que vous devez savoir sur {keyword} pour des fins {tone}.\n\n### Points Clés:\n- Fondamentaux de {keyword}\n- Meilleures pratiques d'implémentation de {keyword}\n- Techniques avancées de {keyword}\n- Erreurs courantes à éviter avec {keyword}",
            "meta": f"{keyword} - Guide Professionnel | Maîtrisez {keyword}",
            "title": f"{keyword}: Le Guide Complet 2026 pour les Professionnels",
            "description": f"Maîtrisez {keyword} avec notre guide expert. Apprenez les stratégies éprouvées et les meilleures pratiques de {keyword}."
        }
    }
    
    lang = "fr" if language == "fr" else "en"
    return templates.get(lang, templates["en"]).get(content_type, "Content generation failed")

# ==================== ENDPOINTS ====================

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de vérification du service"""
    return {
        "status": "active",
        "service": "SEO Analyzer Pro API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Vérification détaillée de la santé du service"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0.0"
    }

@app.post("/api/analyze/keyword", response_model=KeywordAnalysis, tags=["Analysis"])
async def analyze_keyword(request: KeywordAnalysis) -> KeywordAnalysis:
    """Analyse un keyword pour le potentiel SEO"""
    if not request.keyword or len(request.keyword.strip()) == 0:
        raise HTTPException(status_code=400, detail="Keyword cannot be empty")
    
    return generate_keyword_data(request.keyword)

@app.get("/api/analyze/keyword", response_model=KeywordAnalysis, tags=["Analysis"])
async def analyze_keyword_get(keyword: str = Query(..., min_length=1)) -> KeywordAnalysis:
    """Analyse un keyword (GET version)"""
    if not keyword or len(keyword.strip()) == 0:
        raise HTTPException(status_code=400, detail="Keyword cannot be empty")
    
    return generate_keyword_data(keyword)

@app.post("/api/generate/content", tags=["Content Generation"])
async def generate_seo_content(request: ContentGenerationRequest) -> dict:
    """Génère du contenu SEO optimisé"""
    content = generate_content(
        request.keyword,
        request.content_type,
        request.language,
        request.tone
    )
    
    return {
        "keyword": request.keyword,
        "content_type": request.content_type,
        "language": request.language,
        "tone": request.tone,
        "generated_content": content,
        "word_count": len(content.split()),
        "generated_at": datetime.now().isoformat()
    }

@app.post("/api/analyze/backlinks", response_model=BacklinkAnalysis, tags=["Analysis"])
async def analyze_backlinks(domain: str = Query(..., min_length=3)) -> BacklinkAnalysis:
    """Analyse les backlinks d'un domaine"""
    hash_val = int(hashlib.md5(domain.encode()).hexdigest(), 16)
    
    return BacklinkAnalysis(
        domain=domain,
        backlink_count=500 + (hash_val % 5000),
        referring_domains=50 + (hash_val % 500),
        authority_score=round(20 + ((hash_val % 80)), 1),
        top_backlinks=[f"https://site{i}.com/{domain}" for i in range(1, 6)]
    )

@app.get("/api/trending/keywords", tags=["Analytics"])
async def get_trending_keywords(limit: int = Query(10, ge=1, le=50)) -> dict:
    """Retourne les keywords tendance du moment"""
    keywords_data = [generate_keyword_data(kw) for kw in list(MOCK_KEYWORDS.keys())[:limit]]
    return {
        "trending_keywords": keywords_data,
        "total": len(keywords_data),
        "generated_at": datetime.now().isoformat()
    }

@app.post("/api/batch/analyze", tags=["Batch Operations"])
async def batch_analyze(keywords: List[str] = Query(..., min_length=1)) -> dict:
    """Analyse plusieurs keywords en batch"""
    if len(keywords) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 keywords per request")
    
    results = [generate_keyword_data(kw) for kw in keywords]
    
    return {
        "total_analyzed": len(results),
        "results": results,
        "generated_at": datetime.now().isoformat(),
        "processing_time_ms": len(keywords) * 10
    }

@app.get("/api/pricing", tags=["Pricing"])
async def get_pricing() -> dict:
    """Plans de pricing disponibles"""
    return {
        "plans": [
            {
                "name": "Free",
                "price": 0,
                "requests_per_month": 100,
                "features": ["Basic keyword analysis", "Content generation (limited)"]
            },
            {
                "name": "Pro",
                "price": 29,
                "requests_per_month": 5000,
                "features": ["Advanced analysis", "Unlimited content generation", "Batch operations", "API access"]
            },
            {
                "name": "Enterprise",
                "price": 99,
                "requests_per_month": 50000,
                "features": ["All Pro features", "Backlink analysis", "Priority support", "Custom integrations"]
            }
        ]
    }

@app.get("/api/docs/swagger", tags=["Documentation"])
async def swagger_docs():
    """Documentation interactive de l'API"""
    return {"message": "Visit /docs for Swagger UI"}

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/auth/signup", response_model=dict, tags=["Authentication"])
async def signup(request: SignupRequest):
    """Crée un nouveau compte utilisateur"""
    result = AuthManager.create_user(request.email, request.password, request.plan)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/auth/login", response_model=TokenResponse, tags=["Authentication"])
async def login(request: LoginRequest):
    """Authentifie un utilisateur et retourne un JWT token"""
    result = AuthManager.authenticate_user(request.email, request.password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return TokenResponse(
        access_token=result["access_token"],
        token_type=result["token_type"],
        plan=result["plan"]
    )

@app.post("/api/auth/verify", tags=["Authentication"])
async def verify_token(token: str = Header(None)):
    """Vérifie si un JWT token est valide"""
    if not token:
        raise HTTPException(status_code=401, detail="Token required")
    
    payload = AuthManager.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {"valid": True, "user": payload.get("sub"), "plan": payload.get("plan")}

@app.post("/api/auth/upgrade-plan", tags=["Authentication"])
async def upgrade_plan(email: str, new_plan: str = Query(..., regex="^(free|pro|enterprise)$")):
    """Upgrade le plan d'un utilisateur"""
    result = AuthManager.upgrade_plan(email, new_plan)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# ==================== LEGAL SCRAPING ENDPOINTS ====================

@app.get("/api/scrape/keyword/{keyword}", tags=["Legal Scraping"])
async def scrape_keyword(keyword: str):
    """Récupère les données d'un keyword depuis des sources officielles"""
    return LegalDataScraper.scrape_keyword_data(keyword)

@app.get("/api/scrape/backlinks/{domain}", tags=["Legal Scraping"])
async def scrape_backlinks(domain: str):
    """Récupère les données de backlinks d'un domaine"""
    return LegalDataScraper.scrape_backlink_data(domain)

@app.get("/api/scrape/competitor/{domain}", tags=["Legal Scraping"])
async def scrape_competitor(domain: str):
    """Analyse complète du domaine concurrent"""
    return LegalDataScraper.scrape_competitor_data(domain)

@app.get("/api/scrape/trending", tags=["Legal Scraping"])
async def scrape_trending():
    """Récupère les sujets tendance actuels"""
    return {"trending_topics": LegalDataScraper.scrape_trending_topics()}

@app.get("/api/scrape/content-ideas/{keyword}", tags=["Legal Scraping"])
async def scrape_content_ideas(keyword: str):
    """Génère des idées de contenu basées sur un keyword"""
    return {"content_ideas": LegalDataScraper.scrape_content_ideas(keyword)}

@app.post("/api/scrape/batch-keywords", tags=["Legal Scraping"])
async def scrape_batch_keywords(keywords: List[str] = Query(...)):
    """Récupère les données pour plusieurs keywords"""
    if len(keywords) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 keywords per batch")
    
    return {
        "results": LegalDataScraper.batch_scrape_keywords(keywords),
        "total": len(keywords)
    }

@app.get("/api/scrape/status", tags=["Legal Scraping"])
async def scrape_status():
    """Affiche le statut du système de scraping"""
    return LegalDataScraper.get_scraping_status()

# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "timestamp": datetime.now().isoformat()},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
