#!/usr/bin/env python3
"""
Script de déploiement et configuration pour SEO Analyzer Pro
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Setup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.os_type = platform.system()
    
    def run_command(self, cmd, cwd=None):
        """Exécute une commande shell"""
        print(f"[*] {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=False)
            return result.returncode == 0
        except Exception as e:
            print(f"[✗] Erreur: {e}")
            return False
    
    def setup_backend(self):
        """Configure le backend"""
        print("\n[1] Configuration du Backend")
        print("=" * 50)
        
        backend_path = self.project_root / "backend"
        
        # Installer les dépendances
        print("[*] Installation des dépendances...")
        self.run_command("pip install -r requirements.txt", cwd=backend_path)
        
        # Créer .env
        env_file = self.project_root / ".env"
        if not env_file.exists():
            print("[*] Création du fichier .env...")
            with open(env_file, 'w') as f:
                f.write("API_HOST=0.0.0.0\n")
                f.write("API_PORT=8000\n")
                f.write("DATABASE_URL=sqlite:///./seoanalyzer.db\n")
        
        print("✅ Backend configuré!")
    
    def setup_frontend(self):
        """Configure le frontend"""
        print("\n[2] Configuration du Frontend")
        print("=" * 50)
        print("✅ Frontend prêt! (HTML statique, pas de dépendances)")
    
    def setup_cli(self):
        """Configure le CLI"""
        print("\n[3] Configuration du CLI")
        print("=" * 50)
        print("✅ CLI prêt!")
    
    def run_tests(self):
        """Lance les tests"""
        print("\n[4] Tests")
        print("=" * 50)
        
        backend_path = self.project_root / "backend"
        self.run_command("python -m pytest test_api.py -v", cwd=backend_path)
    
    def start_services(self):
        """Démarre les services"""
        print("\n[5] Démarrage des Services")
        print("=" * 50)
        
        print("\n📌 Options de démarrage:")
        print("\nA) Démarrage simple (recommandé pour développement):")
        print("   Terminal 1: cd backend && python main.py")
        print("   Terminal 2: cd frontend && python -m http.server 3000")
        print("   Terminal 3: cd cli && python cli.py --help")
        
        print("\nB) Démarrage avec Docker:")
        print("   docker-compose up")
        
        print("\nC) Démarrage avec scripts:")
        if self.os_type == "Windows":
            print("   powershell -ExecutionPolicy Bypass -File start.ps1")
        else:
            print("   bash start.sh")
    
    def full_setup(self):
        """Setup complet"""
        print("🚀 SEO Analyzer Pro - Setup")
        print("=" * 50)
        
        self.setup_backend()
        self.setup_frontend()
        self.setup_cli()
        
        # Optionnel: lancer les tests
        # self.run_tests()
        
        self.start_services()
        
        print("\n" + "=" * 50)
        print("✅ Setup terminé!")
        print("=" * 50)
        
        print("\n📚 Prochaines étapes:")
        print("1. Lire docs/README.md pour la documentation")
        print("2. Lire docs/MONETIZATION.md pour les stratégies revenue")
        print("3. Configurer .env pour vos paramètres")
        print("4. Customiser le pricing dans main.py")
        print("5. Connecter une vraie base de données")
        print("6. Implémenter l'authentification")
        print("7. Ajouter les vraies API (Google, SemRush, etc)")

if __name__ == "__main__":
    setup = Setup()
    setup.full_setup()
