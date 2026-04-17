# ⚡ QUICK START: Obtenir votre VRAIE Clé Stripe

## Le Problème
Vous avez utilisé un **PLACEHOLDER** (texte d'exemple) au lieu d'une **VRAIE CLÉ**!

```
❌ MAUVAIS:  STRIPE_SECRET_KEY=sk_test_VOTRE_NOUVELLE_CLÉ_ICI
✅ BON:     STRIPE_SECRET_KEY=sk_test_51TN9VeEAhLhnW2...
```

---

## ✅ En 30 secondes: Obtenir la VRAIE Clé

### 1️⃣ Ouvrir le Dashboard
```
https://dashboard.stripe.com/apikeys
```

### 2️⃣ Vérifier TEST MODE (bleu en haut)
```
Ne JAMAIS utiliser LIVE MODE pour les tests!
```

### 3️⃣ Copier la SECRET KEY
```
C'est une LONGUE string qui commence par: sk_test_
Elle fait environ 100 caractères

C'est UNE VRAIE CLÉ copiée directement du dashboard!
```

### 4️⃣ Utiliser cette clé
```bash
# Sur le serveur, remplacez sk_test_VOTRE_NOUVELLE_CLÉ_ICI
# par votre VRAIE clé copiée du dashboard

cat > .env << 'EOF'
STRIPE_SECRET_KEY=sk_test_VOTRE_VRAIE_CLÉ_ICI
STRIPE_PUBLIC_KEY=pk_test_51TN9VeEAhLhnW2F9BXstJCKXFL0EePu4g8x6Acmw1g0cAeWXbGZg4nJDpQT3hKrO8nlg4B8jHBhCG6033hXat6MQ00YmIcOBhu
STRIPE_WEBHOOK_SECRET=whsec_test_placeholder
DATABASE_URL=postgresql://user:password@db:5432/seo_analyzer
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
EOF

docker-compose down
docker-compose up -d
sleep 30
curl -X POST http://localhost:8000/api/payments/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{"plan": "professional", "email": "test@example.com", "name": "Test"}'
```

---

## 🎯 Résultat Attendu

### Si la clé est BONNE:
```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_...",
  "session_id": "cs_test_...",
  "status": "success"
}
```
✅ SUCCÈS!

### Si la clé est MAUVAISE/PLACEHOLDER:
```json
{"error":"Invalid API Key provided: sk_test_*****"}
```
❌ Réessayez avec une VRAIE clé du dashboard

---

## 🔍 Vérifier Votre Clé

```bash
# Afficher ce que vous avez dans .env
cat .env | grep STRIPE_SECRET_KEY

# Vérifier:
# ✅ Commence par: sk_test_
# ✅ ~100 caractères (long!)
# ✅ Pas de "VOTRE_CLÉ_ICI" ou autres placeholders
# ✅ C'est unique/différent chaque fois
```

**Prêt? Mettez une VRAIE clé et testez!** 🚀
# ⚡ QUICK START: Obtenir votre VRAIE Clé Stripe

## Le Problème
Vous avez utilisé un **PLACEHOLDER** (texte d'exemple) au lieu d'une **VRAIE CLÉ**!

```
❌ MAUVAIS:  STRIPE_SECRET_KEY=sk_test_VOTRE_NOUVELLE_CLÉ_ICI
✅ BON:     STRIPE_SECRET_KEY=sk_test_51TN9VeEAhLhnW2F9O0EI...
```

---

## ✅ En 30 secondes: Obtenir la VRAIE Clé

### 1️⃣ Ouvrir le Dashboard
```
https://dashboard.stripe.com/apikeys
```

### 2️⃣ Vérifier TEST MODE (bleu en haut)
```
Ne JAMAIS utiliser LIVE MODE pour les tests!
```

### 3️⃣ Copier la SECRET KEY
```
C'est une LONGUE string qui commence par: sk_test_
Exemple longueur: ~100 caractères

IMPORTANT: C'est UNE VRAIE CLÉ que vous copiez du dashboard
(Pas un placeholder/exemple!)
```

### 4️⃣ Utiliser cette clé
```bash
# Sur le serveur, remplacez sk_test_VOTRE_NOUVELLE_CLÉ_ICI
# par votre VRAIE clé copiée du dashboard

cat > .env << 'EOF'
STRIPE_SECRET_KEY=sk_test_COLLEZ_VOTRE_VRAIE_CLÉ_ICI
STRIPE_PUBLIC_KEY=pk_test_51TN9VeEAhLhnW2F9BXstJCKXFL0EePu4g8x6Acmw1g0cAeWXbGZg4nJDpQT3hKrO8nlg4B8jHBhCG6033hXat6MQ00YmIcOBhu
STRIPE_WEBHOOK_SECRET=whsec_test_placeholder
DATABASE_URL=postgresql://user:password@db:5432/seo_analyzer
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
EOF

docker-compose down
docker-compose up -d
sleep 30
curl -X POST http://localhost:8000/api/payments/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{"plan": "professional", "email": "test@example.com", "name": "Test"}'
```

---

## 🎯 Résultat Attendu

### Si la clé est BONNE:
```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_...",
  "session_id": "cs_test_...",
  "status": "success"
}
```
✅ SUCCÈS!

### Si la clé est MAUVAISE:
```json
{"error":"Invalid API Key provided: sk_test_*****"}
```
❌ Réessayez avec une VRAIE clé du dashboard

---

## 🔍 Vérifier Votre Clé

```bash
# Afficher ce que vous avez dans .env
cat .env | grep STRIPE_SECRET_KEY

# Vérifier:
# ✅ Commence par: sk_test_
# ✅ ~100 caractères (pas court!)
# ✅ Pas de "VOTRE_CLÉ_ICI" ou autres placeholders
```

**Prêt? Mettez une VRAIE clé et testez!** 🚀
