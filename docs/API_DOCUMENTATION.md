# 📚 SEO Analyzer Pro - API Documentation Complète

## Vue d'ensemble

SEO Analyzer Pro est une plateforme SaaS d'analyse SEO avec API REST complète. Cette documentation couvre tous les endpoints disponibles, l'authentification, les limites de taux et les exemples d'utilisation.

---

## 🔐 Authentication

### Endpoints d'authentification

#### 1. Signup (Créer un compte)

```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password123",
  "plan": "free"  // "free", "pro", or "enterprise"
}
```

**Response (201):**
```json
{
  "success": true,
  "user_id": "user@example.com",
  "api_key": "sk_live_abc123def456"
}
```

#### 2. Login (S'authentifier)

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "plan": "pro"
}
```

#### 3. Verify Token (Vérifier un token)

```http
POST /api/auth/verify
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "valid": true,
  "user": "user@example.com",
  "plan": "pro"
}
```

#### 4. Upgrade Plan (Améliorer le plan)

```http
POST /api/auth/upgrade-plan
Query Parameters:
  - email: user@example.com
  - new_plan: pro  // "free", "pro", "enterprise"
```

**Response (200):**
```json
{
  "success": true,
  "new_plan": "pro"
}
```

### Utilisation de l'authentification

Tous les endpoints (sauf /api/health et /) requièrent une authentification. Incluez le token JWT dans l'en-tête:

```http
Authorization: Bearer {access_token}
```

---

## 📊 Analyse des Keywords

### 1. Analyser un keyword

```http
POST /api/analyze/keyword
Authorization: Bearer {token}
Content-Type: application/json

{
  "keyword": "python tutorial",
  "search_volume": 0,
  "difficulty": 0,
  "cpc": 0.0,
  "trend": "stable"
}
```

**Response (200):**
```json
{
  "keyword": "python tutorial",
  "search_volume": 12100,
  "difficulty": 45,
  "cpc": 0.85,
  "trend": "increasing",
  "opportunity_score": 268.89
}
```

### 2. Récupérer les keywords tendance

```http
GET /api/trending/keywords?limit=10
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "trending_keywords": [
    {
      "keyword": "python tutorial",
      "search_volume": 12100,
      "difficulty": 45,
      "cpc": 0.85,
      "trend": "increasing"
    },
    // ... more keywords
  ],
  "total": 10,
  "generated_at": "2024-04-17T10:30:00"
}
```

### 3. Analyser plusieurs keywords (Batch)

```http
POST /api/batch/analyze
Authorization: Bearer {token}
Query Parameters:
  - keywords: ["python tutorial", "web development", "machine learning"]
```

**Response (200):**
```json
{
  "total_analyzed": 3,
  "results": [
    {
      "keyword": "python tutorial",
      "search_volume": 12100,
      "difficulty": 45,
      "cpc": 0.85
    },
    // ... more results
  ],
  "generated_at": "2024-04-17T10:30:00",
  "processing_time_ms": 30
}
```

---

## 📝 Génération de Contenu

### Générer du contenu SEO

```http
POST /api/generate/content
Authorization: Bearer {token}
Content-Type: application/json

{
  "keyword": "python tutorial",
  "content_type": "article",  // "article", "meta", "title", "description"
  "language": "fr",            // "fr", "en", "es", "de"
  "tone": "professional"       // "professional", "casual", "technical"
}
```

**Response (200):**
```json
{
  "keyword": "python tutorial",
  "content_type": "article",
  "language": "fr",
  "tone": "professional",
  "generated_content": "## Guide Complet sur Python Tutorial\n\nMaîtriser Python Tutorial est essentiel...",
  "word_count": 245,
  "generated_at": "2024-04-17T10:30:00"
}
```

### Types de contenu disponibles

| Type | Description | Exemple de sortie |
|------|-------------|-------------------|
| `article` | Article blog complet | 500-2000 mots |
| `meta` | Balise meta optimisée | 50-60 caractères |
| `title` | Titre SEO optimisé | 30-60 caractères |
| `description` | Description SEO | 150-160 caractères |

---

## 🔗 Analyse des Backlinks

### Analyser les backlinks d'un domaine

```http
POST /api/analyze/backlinks?domain=example.com
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "domain": "example.com",
  "backlink_count": 1542,
  "referring_domains": 287,
  "authority_score": 65.3,
  "top_backlinks": [
    "https://site1.com/example.com",
    "https://site2.com/example.com",
    // ...
  ]
}
```

---

## 🕷️ Legal Scraping Endpoints

### 1. Récupérer les données d'un keyword

```http
GET /api/scrape/keyword/{keyword}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "keyword": "python tutorial",
  "search_volume": 12100,
  "keyword_difficulty": 45,
  "avg_cpc": 0.85,
  "opportunity_score": 268.89,
  "trend": "rising",
  "related_keywords": [
    "python tutorial for beginners",
    "best python tutorial",
    "python tutorial advanced"
  ],
  "scraped_at": "2024-04-17T10:30:00"
}
```

### 2. Récupérer les backlinks d'un domaine

```http
GET /api/scrape/backlinks/{domain}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "domain": "example.com",
  "total_backlinks": 1542,
  "referring_domains": 287,
  "backlinks": [
    {
      "domain": "source1.com",
      "authority": 65,
      "traffic": 45000
    },
    // ... more backlinks
  ],
  "domain_authority": 72,
  "scraped_at": "2024-04-17T10:30:00"
}
```

### 3. Analyser un concurrent

```http
GET /api/scrape/competitor/{domain}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "competitor_domain": "competitor.com",
  "top_keywords": [
    {
      "keyword": "keyword-1",
      "position": 1,
      "volume": 25000
    },
    // ... more keywords
  ],
  "estimated_traffic": 145000,
  "content_count": 387,
  "domain_authority": 78,
  "top_content": [
    {
      "title": "Top Article 1",
      "url": "https://competitor.com/article-1",
      "traffic": 5000,
      "backlinks": 127
    },
    // ... more content
  ]
}
```

### 4. Récupérer les sujets tendance

```http
GET /api/scrape/trending
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "trending_topics": [
    {
      "topic": "Artificial Intelligence",
      "trend_score": 85,
      "growth": "+23%",
      "related_keywords": ["AI", "machine learning", "ChatGPT"],
      "news_articles": 5234,
      "social_mentions": 125000
    },
    // ... more trending topics
  ]
}
```

### 5. Générer des idées de contenu

```http
GET /api/scrape/content-ideas/{keyword}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "content_ideas": [
    {
      "title": "Complete Guide to Python Tutorial",
      "type": "guide",
      "estimated_traffic": 15000,
      "questions_covered": 25
    },
    {
      "title": "Top Python Tutorial Tools in 2024",
      "type": "comparison",
      "estimated_traffic": 8000,
      "tools_included": 12
    },
    {
      "title": "Python Tutorial: Common Questions Answered",
      "type": "faq",
      "estimated_traffic": 5000,
      "questions": 23
    }
  ]
}
```

### 6. Analyser plusieurs keywords (Batch)

```http
POST /api/scrape/batch-keywords
Authorization: Bearer {token}
Query Parameters:
  - keywords: ["python", "javascript", "react"]
```

**Response (200):**
```json
{
  "results": [
    {
      "keyword": "python",
      "search_volume": 50000,
      "keyword_difficulty": 68,
      "avg_cpc": 1.20,
      "opportunity_score": 735.29
    },
    // ... more results
  ],
  "total": 3
}
```

### 7. Vérifier le statut du scraping

```http
GET /api/scrape/status
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "status": "operational",
  "data_sources": [
    "Google Trends API",
    "SemRush API (licensed)",
    "Ahrefs API (licensed)",
    "Moz API",
    "Public databases"
  ],
  "last_update": "2024-04-17T10:30:00",
  "compliance": {
    "gdpr": "compliant",
    "robots_txt": "respected",
    "rate_limits": "enforced",
    "legal_status": "100% legal"
  }
}
```

---

## 💰 Pricing

### Récupérer les plans disponibles

```http
GET /api/pricing
```

**Response (200):**
```json
{
  "plans": [
    {
      "name": "Free",
      "price": 0,
      "requests_per_month": 100,
      "features": [
        "Basic keyword analysis",
        "Content generation (limited)"
      ]
    },
    {
      "name": "Pro",
      "price": 29,
      "requests_per_month": 5000,
      "features": [
        "Advanced analysis",
        "Unlimited content generation",
        "Batch operations",
        "API access"
      ]
    },
    {
      "name": "Enterprise",
      "price": 99,
      "requests_per_month": 50000,
      "features": [
        "All Pro features",
        "Backlink analysis",
        "Priority support",
        "Custom integrations"
      ]
    }
  ]
}
```

---

## 🏥 Santé du Service

### Vérifier la santé basique

```http
GET /
```

**Response (200):**
```json
{
  "status": "active",
  "service": "SEO Analyzer Pro API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Vérifier la santé détaillée

```http
GET /api/health
```

**Response (200):**
```json
{
  "status": "operational",
  "timestamp": "2024-04-17T10:30:00",
  "api_version": "1.0.0"
}
```

---

## ⚙️ Limites de taux (Rate Limiting)

### Par plan

| Plan | Requêtes/mois | Requêtes/jour | Requêtes/heure |
|------|---|---|---|
| **Free** | 100 | ~3 | 1 |
| **Pro** | 5,000 | ~167 | 7 |
| **Enterprise** | 50,000 | ~1,667 | 69 |

### Headers de limite de taux

Chaque réponse inclut les en-têtes:

```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4982
X-RateLimit-Reset: 1713355200
```

---

## 🐛 Codes d'erreur

| Code | Signification | Exemple |
|------|--------------|---------|
| **200** | Succès | Requête traitée avec succès |
| **201** | Créé | Ressource créée |
| **400** | Mauvaise requête | Paramètres invalides |
| **401** | Non authentifié | Token manquant ou invalide |
| **403** | Interdit | Accès refusé |
| **404** | Non trouvé | Ressource non trouvée |
| **429** | Trop de requêtes | Limite de taux dépassée |
| **500** | Erreur serveur | Erreur interne du serveur |

### Exemple d'erreur

```json
{
  "error": "Invalid or expired token",
  "timestamp": "2024-04-17T10:30:00",
  "status": 401
}
```

---

## 📝 Exemples d'intégration

### Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"
headers = {
    "Authorization": "Bearer {token}",
    "Content-Type": "application/json"
}

# Analyser un keyword
response = requests.post(
    f"{BASE_URL}/api/analyze/keyword",
    headers=headers,
    json={"keyword": "python tutorial"}
)
print(json.dumps(response.json(), indent=2))
```

### JavaScript

```javascript
const baseURL = "http://localhost:8000";
const token = "YOUR_TOKEN_HERE";

fetch(`${baseURL}/api/scrape/keyword/python`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(json.stringify(data, null, 2)))
.catch(error => console.error('Error:', error));
```

### cURL

```bash
curl -X POST http://localhost:8000/api/analyze/keyword \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "python tutorial",
    "search_volume": 0,
    "difficulty": 0,
    "cpc": 0.0,
    "trend": "stable"
  }'
```

---

## 📚 Ressources supplémentaires

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GitHub**: https://github.com/yourusername/seo-analyzer-pro
- **Status Page**: http://localhost:8000/api/health
- **Support**: support@seoanalyzerpro.com

---

**Last Updated**: April 17, 2024  
**API Version**: 1.0.0  
**Documentation Version**: 1.0.0
