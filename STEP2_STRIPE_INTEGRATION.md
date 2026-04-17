# ÉTAPE 2: INTÉGRATION STRIPE - Configuration des Paiements

## 🎯 Objectif
Activer les paiements Stripe pour monétiser votre SaaS SEO Analyzer Pro

## 📋 Prérequis
- ✅ Déploiement Docker réussi (Étape 1 complète)
- Compte Stripe (créer sur https://dashboard.stripe.com)
- Clés API Stripe (Secret & Public)

---

## STEP 1: Créer un compte Stripe

1. Allez sur https://dashboard.stripe.com
2. Cliquez "Sign up" 
3. Remplissez: Email, mot de passe, nom
4. Complétez le profil avec infos entreprise

**⏱️ Temps: 5 minutes**

---

## STEP 2: Obtenir vos clés API Stripe

1. Dashboard Stripe → "Developers" (coin haut-droit)
2. Cliquez "API Keys"
3. Vous verrez 2 clés:
   - **Publishable Key**: `pk_test_...` (front-end, public)
   - **Secret Key**: `sk_test_...` (backend, SECRET!)

**COPIER LES 2 CLÉS** (vous en aurez besoin)

---

## STEP 3: Configurer les Webhooks Stripe

Les webhooks permettent à Stripe de notifier votre API quand un paiement est reçu.

1. Dashboard Stripe → "Developers" → "Webhooks"
2. Cliquez "Add an endpoint"
3. **Endpoint URL**: `http://164.92.224.168:8000/api/payments/webhook`
4. **Select events to send**: Cochez:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
5. Cliquez "Add endpoint"
6. Cliquez sur votre endpoint → Vous verrez **Signing secret**: `whsec_test_...`

**COPIER LE SIGNING SECRET**

---

## STEP 4: Créer le fichier .env sur le serveur

Sur votre serveur Droplet, créez le fichier `.env`:

```bash
ssh root@164.92.224.168

# Dans le dossier ~/seo-analyzer-pro
cat > .env << 'EOF'
# ===== STRIPE CONFIGURATION =====
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
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
EOF
```

**Remplacez les 3 clés Stripe par VOS clés réelles!**

---

## STEP 5: Redémarrer l'API avec les nouvelles variables

```bash
# Vérifier le fichier .env
cat .env

# Redémarrer les containers
docker-compose down
docker-compose up -d

# Attendre 30 secondes
sleep 30

# Vérifier les logs de l'API
docker logs seo-analyzer-pro_api_1
```

✅ Vous devriez voir: `"status": "operational"` dans les logs

---

## STEP 6: Tester les endpoints Stripe

### Test 1: Créer une Checkout Session

```bash
curl -X POST http://localhost:8000/api/payments/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{
    "plan": "professional",
    "email": "test@example.com",
    "name": "John Doe",
    "company": "My Company"
  }'
```

**Réponse attendue:**
```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_...",
  "session_id": "cs_test_...",
  "status": "success"
}
```

### Test 2: Créer un Client Stripe

```bash
curl -X POST http://localhost:8000/api/payments/create-customer \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "name": "Jane Smith",
    "company": "Tech Startup"
  }'
```

### Test 3: Vérifier les Paiements Réussis

```bash
curl http://localhost:8000/api/payments/customer/cus_CUSTOMER_ID
```

---

## STEP 7: Tester un paiement réel (mode test)

1. **Allez sur le checkout_url reçu** (ou utilisez Stripe's test card)
2. **Remplissez le formulaire:**
   - Email: `test@example.com`
   - Numéro de carte: `4242 4242 4242 4242`
   - Date expiration: N'importe quelle date future (ex: 12/26)
   - CVC: N'importe quel code 3 chiffres (ex: 123)
3. **Cliquez "Subscribe"**

✅ Le paiement devrait réussir (mode TEST - pas d'argent réel)

---

## STEP 8: Vérifier le webhook

1. Dashboard Stripe → "Developers" → "Webhooks" → Votre endpoint
2. Cliquez "Event Log" pour voir les webhooks reçus
3. Vérifiez que vous voyez les événements:
   - `customer.subscription.created` ✅
   - `invoice.payment_succeeded` ✅

---

## 💰 Configurations Tarifaires (définis dans main.py)

| Plan | Prix/mois | Limites | Caractéristiques |
|------|-----------|---------|------------------|
| **Free** | $0 | 100 appels | Basique |
| **Pro** | $29 | 5,000 appels | IA + Support |
| **Enterprise** | $99 | Illimité | Blanc-label + SLA |

*Ces prix sont intégrés dans `backend/main.py` - modifiez-les selon vos besoins*

---

## 🔐 SECURITY CHECKLIST

- ✅ Secret Key JAMAIS en public (gardez en .env)
- ✅ Webhook signing secret protégé
- ✅ HTTPS requis en production
- ✅ Les logs ne doivent JAMAIS afficher les clés

---

## 🐛 Troubleshooting

### Erreur: "Invalid API Key"
→ Vérifiez que STRIPE_SECRET_KEY est correcte dans .env

### Erreur: "Webhook signature verification failed"
→ Vérifiez STRIPE_WEBHOOK_SECRET dans .env

### Paiements non reçus
→ Vérifiez les Event Logs dans Stripe Dashboard
→ Vérifiez que votre serveur peut être atteint par Stripe

### Connexion DB échoue
→ Vérifiez DATABASE_URL dans .env
→ Vérifiez que PostgreSQL est Up: `docker ps | grep db`

---

## ✅ Validation Succès

Une fois complétée, vous devriez pouvoir:
- ✅ Créer une session de checkout Stripe
- ✅ Traiter les paiements en mode test
- ✅ Recevoir les webhooks Stripe
- ✅ Voir les transactions dans le dashboard Stripe

**Bravo! 🎉 Votre SaaS est maintenant monétisé!**

---

## PROCHAINES ÉTAPES

### Étape 3: Frontend Payment Integration
- Intégrer Stripe.js au frontend
- Afficher les plans de tarification
- Bouton "Subscribe" → Redirect Stripe Checkout

### Étape 4: Production Launch
- Passer en mode LIVE (clés en prod)
- Configurer le domaine personnalisé
- Mettre à jour les URLs de redirection
- Lancer ProductHunt!

---

## 📞 Support

- Docs Stripe: https://stripe.com/docs
- API Reference: https://stripe.com/docs/api
- Community: https://stripe.com/communities

