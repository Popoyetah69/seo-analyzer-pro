# 🔑 STRIPE SETUP - FINAL CHECKLIST

## ✅ Your Current Status
- ✅ API Running
- ✅ Docker OK
- ❌ Stripe Key: WRONG (placeholder, not real)

---

## 🎯 WHAT TO DO NOW (3 STEPS)

### STEP 1: Check your .env
```bash
cat .env | grep STRIPE_SECRET_KEY
```

**What you'll see:**
- ❌ BAD: `STRIPE_SECRET_KEY=sk_test_VOTRE_NOUVELLE_CLÉ_ICI`
- ❌ BAD: `STRIPE_SECRET_KEY=sk_test_VOTRE_VRAIE_CLÉ_ICI`
- ✅ GOOD: `STRIPE_SECRET_KEY=sk_test_51TN9VeEAhLhnW2F9O0EI...` (looks like REAL data)

---

### STEP 2: Get REAL key from Stripe
1. Open: https://dashboard.stripe.com/apikeys
2. Make sure **TEST MODE** is ON (blue toggle at top)
3. Find "Secret Key" row
4. Click on it or "Reveal" button
5. **COPY THE FULL KEY** - it's long (~100 chars)

---

### STEP 3: Update .env with REAL key

On your server:
```bash
# Edit the file
nano .env

# Find this line:
STRIPE_SECRET_KEY=sk_test_PLACEHOLDER_OR_OLD_VALUE

# Replace it with your REAL key:
STRIPE_SECRET_KEY=sk_test_REAL_KEY_YOU_COPIED_FROM_DASHBOARD

# Save: CTRL+X → Y → ENTER

# Restart Docker
docker-compose restart api

# Wait 10 seconds
sleep 10

# Test
curl -X POST http://localhost:8000/api/payments/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{"plan":"professional","email":"test@example.com","name":"Test"}'
```

---

## 🎯 EXPECTED RESULT

### If key is CORRECT ✅
```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_...",
  "session_id": "cs_test_...",
  "status": "success"
}
```

### If key is WRONG ❌
```json
{"error":"Invalid API Key provided: sk_test_*****"}
```
→ Go back to Step 1 and check your .env

---

## ✅ WHEN IT WORKS

Once you see the success JSON with checkout_url:
1. **Stripe Integration = COMPLETE! 🎉**
2. Your SaaS now accepts payments!
3. Test checkout: Visit the checkout_url in browser
4. Use test card: 4242 4242 4242 4242

---

## 🆘 STUCK?

Share the output of:
```bash
cat .env | grep STRIPE_SECRET_KEY
```

(DON'T share the full key, just show what it looks like)
