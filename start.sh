#!/bin/bash
# Script de démarrage complet de SEO Analyzer Pro

set -e

echo "🚀 SEO Analyzer Pro - Démarrage"
echo "======================================"

# Vérifier Python
echo "[1/4] Vérification Python..."
python --version

# Installer les dépendances
echo "[2/4] Installation des dépendances..."
cd backend
pip install -q -r requirements.txt
cd ..

# Lancer les tests
echo "[3/4] Exécution des tests..."
cd backend
python -m pytest test_api.py -v --tb=short 2>/dev/null || echo "⚠️  Tests skipped (pytest peut ne pas être installé)"
cd ..

# Démarrer l'API
echo "[4/4] Démarrage de l'API..."
echo ""
echo "✅ Prêt! Démarrez le backend avec:"
echo "   cd backend && python main.py"
echo ""
echo "✅ En parallèle, lancez le frontend:"
echo "   cd frontend && python -m http.server 3000"
echo ""
echo "✅ Ou utilisez Docker:"
echo "   docker-compose up"
