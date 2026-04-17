# 🔑 Guide: Récupérer vos Clés Stripe

## 📍 LOCATION DES CLÉS

Les clés Stripe se trouvent au: https://dashboard.stripe.com/apikeys

---

## 🎯 ÉTAPES DÉTAILLÉES

### **1️⃣ Connexion à Stripe Dashboard**

```
1. Ouvrez: https://dashboard.stripe.com
2. Connectez-vous avec votre compte Stripe
   (Si pas de compte: cliquez "Sign up" et créez-en un)
3. Vous arrivez à la page d'accueil
```

### **2️⃣ Naviguer vers "API Keys"**

```
Page d'accueil Stripe Dashboard:
├── Coin haut-DROIT: "Developers" (ou ⚙️ Settings)
│   └── Cliquez "Developers"
│
├── Menu gauche s'ouvre:
│   ├── API Keys ← 👈 CLIQUEZ ICI
│   ├── Webhooks
│   ├── Events
│   └── ...
```

### **3️⃣ Copier vos 3 Clés**

Une fois sur la page "API Keys", vous verrez:

```
┌─────────────────────────────────────────────────┐
│  TEST MODE (pour développer/tester)            │
├─────────────────────────────────────────────────┤
│ Publishable Key:  pk_test_XXXXXXXXXXXXXX       │
│ Secret Key:       sk_test_XXXXXXXXXXXXXX       │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  LIVE MODE (pour gagner de l'argent réel)     │
├─────────────────────────────────────────────────┤
│ Publishable Key:  pk_live_XXXXXXXXXXXXXX       │
│ Secret Key:       sk_live_XXXXXXXXXXXXXX       │
└─────────────────────────────────────────────────┘
```

**POUR COMMENCER = UTILISEZ LE "TEST MODE"**

**Copiez:**
- `pk_test_...` (Publishable Key)
- `sk_test_...` (Secret Key)

### **4️⃣ Créer le Webhook (IMPORTANT!)**

Les webhooks permettent à Stripe de notifier votre serveur quand un paiement réussit.

```
1. Menu gauche: Cliquez "Webhooks"
2. Bouton: "Add an endpoint"
3. Remplissez:
   - Endpoint URL: http://164.92.224.168:8000/api/payments/webhook
   - Description: SEO Analyzer Pro Webhook
4. Cliquez "Add endpoint"
5. Cliquez sur votre endpoint créé
6. Vous verrez: "Signing secret": whsec_test_XXXXX
7. Copiez ce "Signing secret"
```

### **5️⃣ Sélectionner les Events Webhook**

```
Sur la page de votre endpoint:
1. Bouton: "Select events"
2. Cochez:
   ✅ customer.subscription.created
   ✅ customer.subscription.updated
   ✅ customer.subscription.deleted
   ✅ invoice.payment_succeeded
   ✅ invoice.payment_failed
3. Cliquez "Add events"
```

---

## 📋 Résumé des 3 Clés à Copier

| Clé | Format | Exemple | Utilisation |
|-----|--------|---------|------------|
| **Publishable Key** | `pk_test_...` | `pk_test_51Nrm7IXXXXXXXXXXXXXXXX` | Frontend (JavaScript) |
| **Secret Key** | `sk_test_...` | `sk_test_4eC39HqLyjWDarhtT657XXXXXX` | Backend (Python/Node) |
| **Webhook Secret** | `whsec_test_...` | `whsec_1NrFEPXXXXXXXXXXXXXXXX` | Vérifier webhooks |

---

## 💻 Ajouter au Serveur

### **Méthode 1: Créer .env directement sur le serveur**

```bash
# SSH sur le serveur
ssh root@164.92.224.168

# Dans le dossier du projet
cd ~/seo-analyzer-pro

# Créer le fichier .env
cat > .env << 'EOF'
# ===== STRIPE KEYS (copier vos vraies clés!) =====
STRIPE_SECRET_KEY=sk_test_VOTRE_SECRET_KEY_ICI
STRIPE_PUBLIC_KEY=pk_test_VOTRE_PUBLIC_KEY_ICI
STRIPE_WEBHOOK_SECRET=whsec_test_VOTRE_WEBHOOK_SECRET_ICI

# ===== DATABASE =====
DATABASE_URL=postgresql://user:password@db:5432/seo_analyzer

# ===== API SETTINGS =====
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# ===== JWT =====
JWT_SECRET=your-super-secret-jwt-key-change-in-production
EOF

# Vérifier le fichier
cat .env

# Redémarrer Docker
docker-compose down
docker-compose up -d --build

# Attendre 30 secondes
sleep 30

# Vérifier les logs
docker logs seo-analyzer-pro_api_1 | grep -i stripe
```

### **Méthode 2: Créer .env local puis transférer**

```bash
# Sur votre ordinateur
cat > .env << 'EOF'
STRIPE_SECRET_KEY=sk_test_VOTRE_CLÉ_ICI
STRIPE_PUBLIC_KEY=pk_test_VOTRE_CLÉ_ICI
STRIPE_WEBHOOK_SECRET=whsec_test_VOTRE_CLÉ_ICI
EOF

# Transférer au serveur
scp .env root@164.92.224.168:~/seo-analyzer-pro/

# Sur le serveur, redémarrer
ssh root@164.92.224.168 'cd ~/seo-analyzer-pro && docker-compose down && docker-compose up -d --build'
```

---

## ✅ Vérifier que ça marche

### Test 1: Health Check
```bash
curl http://164.92.224.168:8000/api/health
```

Réponse attendue:
```json
{"status":"operational","timestamp":"...","api_version":"1.0.0"}
```

### Test 2: Créer une Session Checkout
```bash
curl -X POST http://164.92.224.168:8000/api/payments/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{
    "plan": "professional",
    "email": "test@example.com",
    "name": "Test User",
    "company": "Test Company"
  }'
```

Réponse attendue:
```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_...",
  "session_id": "cs_test_...",
  "status": "success"
}
```

### Test 3: Tester un Paiement

1. Cliquez sur le `checkout_url` reçu (ou allez dans Stripe Dashboard Test)
2. Remplissez le formulaire avec:
   - Email: `test@example.com`
   - Numéro carte: `4242 4242 4242 4242` (test card)
   - Expiration: N'importe quelle date future (ex: 12/26)
   - CVC: N'importe quel code 3 chiffres (ex: 123)
3. Cliquez "Subscribe"

✅ Le paiement devrait réussir (c'est du test, pas d'argent réel!)

### Test 4: Vérifier le Webhook

Dans Stripe Dashboard:
1. Developers → Webhooks → Votre endpoint
2. Cliquez "Event Log"
3. Vous devriez voir les événements:
   - `customer.subscription.created` ✅
   - `invoice.payment_succeeded` ✅

---

## 🚨 SÉCURITÉ - Important!

⚠️ **JAMAIS partager votre Secret Key!**
- Ne la mettez PAS en public (GitHub, emails, etc.)
- Ne la mettez que dans `.env` sur votre serveur
- Ne la commitez JAMAIS en git

✅ **À FAIRE:**
- Gardez `.env` SECRET (ajoutez-le à `.gitignore`)
- Utilisez les clés TEST pour développer
- Passez aux clés LIVE seulement en production
- Changez la clé JWT dans `.env` en production

---

## 📞 Aide

- Docs Stripe: https://stripe.com/docs
- API Reference: https://stripe.com/docs/api
- Test Cards: https://stripe.com/docs/testing

