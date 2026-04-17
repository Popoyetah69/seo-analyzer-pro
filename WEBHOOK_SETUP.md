# 🪝 Webhooks Stripe - LOCALISATION & CONFIGURATION

## 📍 OÙ TROUVER?

### Chemin Exact:
```
https://dashboard.stripe.com
  ↓
Developers (coin haut-droit)
  ↓
Menu gauche → "Webhooks"
  ↓
[Add an endpoint]
```

---

## 🛠️ CONFIGURATION WEBHOOK

### Étape 1: Ajouter l'Endpoint
```
Endpoint URL: http://164.92.224.168:8000/api/payments/webhook
```

### Étape 2: Sélectionner les Events
```
☑ customer.subscription.created
☑ customer.subscription.updated
☑ customer.subscription.deleted
☑ invoice.payment_succeeded
☑ invoice.payment_failed
```

### Étape 3: Copier le Secret
Après création, vous verrez:
```
Signing secret: whsec_test_...
```

---

## 📝 AJOUTER AU .ENV

Sur le serveur:
```bash
nano .env

# Trouvez:
STRIPE_WEBHOOK_SECRET=whsec_test_VOTRE_WEBHOOK_SECRET_ICI

# Remplacez par le secret reçu de Stripe
STRIPE_WEBHOOK_SECRET=whsec_test_VOTRE_VRAI_SECRET_ICI

# Sauvegardez: CTRL+X → Y → ENTER
```

---

## ✅ VÉRIFIER

```bash
cat .env | grep STRIPE_WEBHOOK_SECRET
# Doit afficher: whsec_test_... (le vrai secret)
```

**Puis redémarrez Docker et testez!** 🚀
