# 🔐 Sécurité Stripe - À FAIRE IMMÉDIATEMENT

## ⚠️ Incident: Clé Secrète Exposée

Si vous avez partagé votre `sk_test_...` quelque part (chat, screenshot, etc.), **RÉVQUEZ-LA IMMÉDIATEMENT!**

---

## 🛡️ Action 1: Révoquer la Clé Compromise

### Étape 1: Allez au Dashboard Stripe
```
https://dashboard.stripe.com/apikeys
```

### Étape 2: Localisez la Clé Compromise
- Trouvez la clé `sk_test_...` que vous avez partagée
- Elle doit être SUPPRIMÉE

### Étape 3: SUPPRIMEZ la clé
- Cliquez sur les 3 points "..." à côté de la clé
- Sélectionnez "Delete"
- **CONFIRMEZ**

✅ La clé est maintenant INUTILISABLE, même si quelqu'un la possède

---

## 🔑 Action 2: Générer une NOUVELLE Clé

### Étape 1: Sur la page API Keys
- Cliquez "Create API Key" ou "Create Restricted Key"
- (Utilisez "Restricted Key" pour plus de sécurité)

### Étape 2: Donner un nom
```
SEO Analyzer Pro - Production
```

### Étape 3: Copier la NOUVELLE clé
- Elle commence par `sk_test_...`
- Elle est COMPLÈTEMENT DIFFÉRENTE de l'ancienne
- **NE LA PARTAGEZ JAMAIS!**

---

## 📝 Action 3: Mettre à jour votre .env

```bash
# Sur le serveur
ssh root@164.92.224.168
cd ~/seo-analyzer-pro

# Modifier .env UNIQUEMENT - pas d'autres fichiers!
nano .env

# Remplacez:
# STRIPE_SECRET_KEY=sk_test_ANCIENNE_CLÉ
# Par:
# STRIPE_SECRET_KEY=sk_test_NOUVELLE_CLÉ

# Sauvegardez: CTRL+X → Y → ENTER

# Redémarrer Docker
docker-compose restart api

# Tester
sleep 10
curl -X POST http://localhost:8000/api/payments/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{"plan": "professional", "email": "test@example.com", "name": "Test"}'
```

---

## 🚨 Bonnes Pratiques de Sécurité

### ✅ À FAIRE:
- ✅ Garder `.env` **JAMAIS** en Git
- ✅ Ne JAMAIS partager les clés `sk_test_` ou `sk_live_`
- ✅ Utiliser des screenshots MASQUÉS: `sk_test_***` au lieu du vrai
- ✅ Révoquer immédiatement si exposée
- ✅ Utiliser `restricted keys` avec permissions minimales

### ❌ À ÉVITER:
- ❌ Copier/coller les clés en texte brut
- ❌ Les mettre en screenshots visibles
- ❌ Les committer en Git
- ❌ Les envoyer par email/chat non-chiffré

---

## ✅ Vérification: Nouvelle Clé Fonctionne

Une fois configurée avec la nouvelle clé:

```bash
# Test:
curl -X POST http://localhost:8000/api/payments/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{"plan": "professional", "email": "test@example.com", "name": "Test User"}'
```

**Résultat attendu:**
```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_...",
  "session_id": "cs_test_...",
  "status": "success"
}
```

✅ = Nouvelle clé fonctionne! 🎉

---

## 📞 En Cas de Doute

- Docs Stripe Security: https://stripe.com/docs/security
- API Key Safety: https://stripe.com/docs/keys

