# 🔌 Guide d'Intégrations & APIs Réelles

Ici comment connecter des APIs réelles pour avoir des vraies données instead de mocks.

## 1. Google Trends API

Pour vraies données de tendance de keywords

```python
from pytrends.request import TrendReq

def get_google_trends(keyword: str) -> dict:
    """Récupère les données Google Trends"""
    pytrends = TrendReq(hl='fr-FR', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m')
    
    data = pytrends.interest_over_time()
    suggestions = pytrends.get_related_queries()
    
    return {
        "trend_data": data.to_dict(),
        "related_queries": suggestions
    }
```

**Installation:**
```bash
pip install pytrends
```

**Gratuit**: Oui (avec rate limiting)
**Rate limit**: ~1 request par seconde

## 2. SemRush API

Données puissantes sur keywords, difficulté, CPC

```python
import requests

SEMRUSH_API = "https://api.semrush.com/"
API_KEY = "your-api-key"

def get_keyword_difficulty(keyword: str, database: str = "us") -> dict:
    """Récupère la difficulté keyword via SemRush"""
    
    params = {
        "type": "keyword_difficulty",
        "key": API_KEY,
        "keyword": keyword,
        "database": database
    }
    
    response = requests.get(SEMRUSH_API, params=params)
    
    lines = response.text.strip().split('\n')
    if len(lines) > 0:
        values = lines[0].split('|')
        return {
            "keyword": values[0],
            "difficulty": float(values[1]) if len(values) > 1 else 0,
            "volume": int(values[2]) if len(values) > 2 else 0,
        }
    return {}
```

**Inscription**: https://semrush.com/api/
**Coût**: $0-500+/mois (par usage)
**Rate limit**: Selon plan

## 3. Ahrefs API

Analyse de backlinks et autorité de domaine

```python
import requests

AHREFS_API = "https://api.ahrefs.com/v3"
API_KEY = "your-api-key"

def get_domain_metrics(domain: str) -> dict:
    """Récupère les métriques de domaine via Ahrefs"""
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # Get domain rating
    response = requests.get(
        f"{AHREFS_API}/site-explorer/metrics",
        params={"target": domain},
        headers=headers
    )
    
    data = response.json()
    
    return {
        "domain": domain,
        "domain_rating": data.get("domain_rating"),
        "referring_domains": data.get("referring_domains"),
        "backlinks": data.get("backlinks"),
        "traffic": data.get("organic_traffic")
    }
```

**Inscription**: https://ahrefs.com/api
**Coût**: $1000+/mois
**Meilleur pour**: Agences sérieuses

## 4. Google Search Console API

Données de recherche réelle d'un site

```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def get_search_analytics(site_url: str, start_date: str, end_date: str):
    """Récupère les données de Google Search Console"""
    
    # Setup credentials
    credentials = Credentials.from_service_account_file(
        'service-account.json',
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    
    service = build('searchconsole', 'v1', credentials=credentials)
    
    request = service.searchanalytics().query(
        siteUrl=site_url,
        body={
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query'],
            'rowLimit': 1000
        }
    )
    
    return request.execute()
```

**Setup**: https://search.google.com/search-console/
**Coût**: Gratuit
**Données**: Réelles pour votre site

## 5. OpenAI API (Content Generation)

Générer contenu avec GPT plutôt que templates

```python
import openai

openai.api_key = "sk-..."

def generate_seo_article(keyword: str, length: str = "medium") -> str:
    """Génère un article SEO avec GPT"""
    
    prompt = f"""
    Write a comprehensive SEO-optimized article about '{keyword}'.
    
    Requirements:
    - Length: {length} (800-1500 words)
    - Include H2 and H3 headings
    - Include practical examples
    - Focus on user intent and keywords
    - Professional tone
    
    Start with a catchy introduction that mentions the keyword.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content
```

**Inscription**: https://platform.openai.com/
**Coût**: $0.015-0.03 per 1K tokens (~$5-10 per article)
**Avantage**: Bien meilleur contenu qu'avec templates

## 6. Stripe API (Paiements)

Pour facturer les utilisateurs

```python
import stripe

stripe.api_key = "sk_test_..."

def create_subscription(customer_email: str, plan_id: str) -> dict:
    """Crée un abonnement Stripe"""
    
    # Create customer
    customer = stripe.Customer.create(
        email=customer_email,
        payment_method="pm_card_visa",
        invoice_settings={"default_payment_method": "pm_card_visa"}
    )
    
    # Create subscription
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{"price": plan_id}],
        payment_behavior="default_incomplete",
        expand=["latest_invoice.payment_intent"]
    )
    
    return {
        "customer_id": customer.id,
        "subscription_id": subscription.id,
        "client_secret": subscription.latest_invoice.payment_intent.client_secret
    }

def get_usage(subscription_id: str) -> int:
    """Récupère l'usage actuel d'un utilisateur"""
    sub = stripe.Subscription.retrieve(subscription_id)
    return sub.usage
```

**Setup**: https://stripe.com/
**Coût**: 2.9% + $0.30 par transaction
**Documentation**: Excellente

## 7. SendGrid API (Emails)

Pour envoyer emails et notifications

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_notification_email(to_email: str, analysis_results: dict):
    """Envoie une notification par email"""
    
    message = Mail(
        from_email="noreply@seoanalyzerpro.com",
        to_emails=to_email,
        subject="Your SEO Analysis is Ready!",
        html_content=f"""
        <h1>Analysis Complete</h1>
        <p>Your analysis for <strong>{analysis_results['keyword']}</strong> is ready!</p>
        
        <h2>Results:</h2>
        <ul>
            <li>Search Volume: {analysis_results['volume']}</li>
            <li>Difficulty: {analysis_results['difficulty']}</li>
            <li>CPC: ${analysis_results['cpc']}</li>
        </ul>
        
        <a href="https://seoanalyzerpro.com/results/{analysis_results['id']}">View Full Report</a>
        """
    )
    
    sg = SendGridAPIClient("SG...")
    response = sg.send(message)
    return response.status_code == 202
```

**Coût**: $9-99/mois par tier
**Gratuit**: 100 emails/jour avec SendGrid free

## 8. Zapier / n8n (Automation)

Pour créer des workflows sans code

```
Zapier Zap Example:
Trigger: Form submission on website
Action 1: Add to SEO Analyzer Pro (via webhook)
Action 2: Send API result to Slack
Action 3: Save to Google Sheets
Action 4: Send email with results
```

**Setup automation via Zapier:**
```
https://zapier.com/developer/create
```

**Ou utiliser n8n (self-hosted):**
```bash
npm install -g n8n
n8n start
# Accédez sur http://localhost:5678
```

## 🎯 Integration Priority

**Phase 1 (Week 1-2) - Must Have:**
- [ ] Stripe pour paiements
- [ ] SendGrid pour emails
- [ ] Database (PostgreSQL)

**Phase 2 (Week 3-4) - Should Have:**
- [ ] Google Trends
- [ ] Google Search Console
- [ ] OpenAI pour meilleur contenu

**Phase 3 (Month 2) - Nice to Have:**
- [ ] SemRush API
- [ ] Ahrefs API
- [ ] Zapier/n8n integrations
- [ ] WordPress plugin

## 📊 Coûts Estimés (Monthly)

| Service | Entry | Growth | Scale |
|---------|-------|--------|-------|
| Stripe | 0 | 2.9% | 2.9% |
| SendGrid | 0 | $20 | $100 |
| OpenAI | $0 | $100 | $1000 |
| SemRush | 0 | $0 | $500+ |
| AWS/Linode | $50 | $200 | $500+ |
| **Total** | **$50** | **$322** | **$2100** |

## 🔑 Environment Variables Template

```bash
# APIs
GOOGLE_TRENDS_API_KEY=xxx
SEMRUSH_API_KEY=xxx
AHREFS_API_KEY=xxx
OPENAI_API_KEY=xxx
STRIPE_SECRET_KEY=xxx
SENDGRID_API_KEY=xxx

# Database
DATABASE_URL=postgresql://...

# Email
ADMIN_EMAIL=admin@seoanalyzerpro.com
SUPPORT_EMAIL=support@seoanalyzerpro.com

# Features
ENABLE_REAL_DATA=True
ENABLE_PAYMENTS=True
ENABLE_EMAILS=True
```

## 📚 Ressources

- SemRush API Docs: https://semrush.com/api-documentation/
- Ahrefs API: https://ahrefs.com/api
- Stripe Docs: https://stripe.com/docs/api
- OpenAI: https://platform.openai.com/docs
- SendGrid: https://docs.sendgrid.com/

---

**Next Step**: Choisir au moins 2 APIs pour week 1!
