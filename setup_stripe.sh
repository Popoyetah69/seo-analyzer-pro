#!/bin/bash
# Script helper pour configurer les clés Stripe sur le serveur
# Usage: ./setup_stripe.sh sk_test_XXX pk_test_XXX whsec_test_XXX

STRIPE_SECRET_KEY=$1
STRIPE_PUBLIC_KEY=$2
STRIPE_WEBHOOK_SECRET=$3

if [ -z "$STRIPE_SECRET_KEY" ] || [ -z "$STRIPE_PUBLIC_KEY" ]; then
    echo "❌ Erreur: Clés manquantes!"
    echo "Usage: ./setup_stripe.sh sk_test_XXX pk_test_XXX whsec_test_XXX"
    exit 1
fi

echo "🔧 Configuration Stripe en cours..."

# Créer le fichier .env
cat > .env << EOF
# ===== STRIPE CONFIGURATION =====
STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY
STRIPE_PUBLIC_KEY=$STRIPE_PUBLIC_KEY
STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET:-whsec_test_placeholder}

# ===== DATABASE =====
DATABASE_URL=postgresql://user:password@db:5432/seo_analyzer

# ===== API SETTINGS =====
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# ===== JWT =====
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
EOF

echo "✅ Fichier .env créé!"

# Redémarrer Docker
echo "🐳 Redémarrage Docker..."
docker-compose down
docker-compose up -d --build

echo "⏳ Attente de 30 secondes pour le démarrage..."
sleep 30

# Vérifier les logs
echo "📋 Vérification des logs..."
docker logs seo-analyzer-pro_api_1 | tail -20

echo "✅ Configuration complétée!"
echo ""
echo "🧪 Test de santé:"
curl http://localhost:8000/api/health
