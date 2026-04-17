# 🚀 Guide de Déploiement en Production

Ce guide couvre le déploiement de SEO Analyzer Pro sur différentes plateformes.

---

## 📋 Pré-requis

- Node.js 16+ ou Python 3.9+
- Docker (recommandé)
- Compte sur plateforme cloud (DigitalOcean, AWS, Heroku, etc.)
- Domaine personnalisé (optionnel mais recommandé)
- Certificat SSL (auto-généré ou LetsEncrypt)

---

## 🐳 Déploiement avec Docker (Recommandé)

### 1. Préparer le projet

```bash
# Cloner ou accéder au répertoire du projet
cd seo-analyzer-pro

# Vérifier la structure
ls -la
```

### 2. Construire l'image Docker

```bash
# Build l'image
docker build -t seo-analyzer-pro:latest .

# Vérifier l'image
docker images | grep seo-analyzer-pro
```

### 3. Exécuter localement

```bash
# Créer le fichier .env
cp .env.example .env

# Exécuter le conteneur
docker run -d \
  --name seo-analyzer-pro \
  -p 8000:8000 \
  --env-file .env \
  seo-analyzer-pro:latest

# Vérifier les logs
docker logs -f seo-analyzer-pro
```

### 4. Vérifier la santé

```bash
# Santé basique
curl http://localhost:8000/

# Santé détaillée
curl http://localhost:8000/api/health
```

---

## ☁️ Déploiement sur DigitalOcean (Recommandé - $27/mois)

### 1. Créer une Droplet

```bash
# Via CLI (doctl)
doctl compute droplet create seo-analyzer \
  --region nyc3 \
  --image ubuntu-22-04-x64 \
  --size s-1vcpu-1gb \
  --enable-monitoring \
  --wait

# Ou via le dashboard: https://cloud.digitalocean.com/droplets
```

### 2. Se connecter à la Droplet

```bash
ssh root@YOUR_DROPLET_IP
```

### 3. Installer Docker

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Vérifier installation
docker --version
```

### 4. Cloner et déployer

```bash
# Clone du repository
git clone https://github.com/yourusername/seo-analyzer-pro.git
cd seo-analyzer-pro

# Créer .env
cp .env.example .env
nano .env  # Éditer les variables

# Build et run
docker-compose up -d

# Vérifier
docker-compose logs -f
```

### 5. Configuration Nginx (Reverse Proxy)

```bash
# Installer Nginx
apt install nginx -y

# Créer configuration
nano /etc/nginx/sites-available/seo-analyzer-pro
```

**Contenu du fichier:**

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name seoanalyzerpro.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
}
```

```bash
# Activer configuration
ln -s /etc/nginx/sites-available/seo-analyzer-pro \
      /etc/nginx/sites-enabled/

# Tester
nginx -t

# Redémarrer
systemctl restart nginx
```

### 6. SSL avec Let's Encrypt

```bash
# Installer Certbot
apt install certbot python3-certbot-nginx -y

# Obtenir certificat
certbot --nginx -d seoanalyzerpro.com -d www.seoanalyzerpro.com

# Auto-renouvellement
certbot renew --dry-run
```

### 7. Vérifier le déploiement

```bash
curl https://seoanalyzerpro.com/api/health
```

---

## 🚀 Déploiement sur AWS (ECS + Fargate)

### 1. Créer un repository ECR

```bash
# Créer repository
aws ecr create-repository \
  --repository-name seo-analyzer-pro \
  --region us-east-1

# Récupérer URI
aws ecr describe-repositories \
  --region us-east-1 \
  --query 'repositories[0].repositoryUri'
```

### 2. Pousser l'image

```bash
# Login à ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build et tag
docker build -t seo-analyzer-pro:latest .
docker tag seo-analyzer-pro:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/seo-analyzer-pro:latest

# Push
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/seo-analyzer-pro:latest
```

### 3. Créer tâche ECS

```bash
# Via AWS Console:
# 1. ECS > Clusters > Create cluster
# 2. Fargate
# 3. Task Definition > seo-analyzer-pro
# 4. Container image: ECR URI
# 5. Port: 8000
# 6. CPU: 256, Memory: 512
```

### 4. Service ECS

```bash
# Via Console:
# 1. Create service
# 2. Fargate
# 3. Task definition: seo-analyzer-pro
# 4. Desired count: 2 (haute disponibilité)
# 5. Load balancer: Application Load Balancer
# 6. Configure auto-scaling
```

---

## 📦 Déploiement sur Heroku

### 1. Installer Heroku CLI

```bash
# macOS
brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Télécharger depuis https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Authentification

```bash
heroku login
```

### 3. Créer app

```bash
heroku create seo-analyzer-pro
```

### 4. Configurer variables

```bash
heroku config:set \
  SECRET_KEY=your_secret_key \
  DATABASE_URL=postgres://... \
  --app seo-analyzer-pro
```

### 5. Déployer

```bash
git push heroku main
```

### 6. Vérifier

```bash
heroku logs --tail --app seo-analyzer-pro
```

---

## 🔄 Déploiement avec GitHub Actions (CI/CD)

Créer `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t seo-analyzer-pro:latest .
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Push to Docker Hub
      run: docker push seo-analyzer-pro:latest
    
    - name: Deploy to DigitalOcean
      env:
        DROPLET_IP: ${{ secrets.DROPLET_IP }}
        DROPLET_SSH_KEY: ${{ secrets.DROPLET_SSH_KEY }}
      run: |
        mkdir -p ~/.ssh
        echo "$DROPLET_SSH_KEY" > ~/.ssh/deploy_key
        chmod 600 ~/.ssh/deploy_key
        ssh -i ~/.ssh/deploy_key root@$DROPLET_IP \
          'cd seo-analyzer-pro && git pull && docker-compose up -d'
```

---

## 📊 Monitoring en production

### 1. Logs centralisés (ELK Stack)

```bash
# Elasticsearch
docker run -d \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:8.0.0

# Kibana
docker run -d \
  -p 5601:5601 \
  -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" \
  docker.elastic.co/kibana/kibana:8.0.0
```

### 2. Monitoring des performances (Prometheus + Grafana)

```bash
# Prometheus
docker run -d \
  -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Grafana
docker run -d \
  -p 3000:3000 \
  grafana/grafana
```

### 3. Alertes (AlertManager)

Configurer des alertes pour:
- CPU > 80%
- Mémoire > 85%
- Erreurs 5xx > 1%
- Temps de réponse > 2s

---

## 🔐 Sécurité en production

### 1. Variables d'environnement

```bash
# Ne JAMAIS committer de secrets
export SECRET_KEY="changez_cette_valeur"
export DATABASE_URL="postgresql://user:pass@host/db"
export API_KEYS_ENABLED=true
```

### 2. CORS

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seoanalyzerpro.com"],  # Spécifique
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization"],
)
```

### 3. Rate Limiting

```python
# Déjà implémenté via AuthManager.check_rate_limit()
```

### 4. HTTPS

```bash
# Obligatoire en production
# Certbot + Let's Encrypt
certbot --nginx -d seoanalyzerpro.com
```

### 5. Firewall

```bash
# UFW (DigitalOcean)
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw default deny incoming
ufw enable
```

---

## 📈 Scaling

### Horizontal Scaling (Multiple instances)

```bash
# Docker Swarm
docker swarm init
docker service create \
  --name seo-analyzer-pro \
  --replicas 3 \
  -p 8000:8000 \
  seo-analyzer-pro:latest
```

### Load Balancer

```bash
# Nginx upstream
upstream seo_analyzer {
    server 10.0.0.1:8000;
    server 10.0.0.2:8000;
    server 10.0.0.3:8000;
}

server {
    listen 80;
    server_name seoanalyzerpro.com;
    
    location / {
        proxy_pass http://seo_analyzer;
    }
}
```

### Database Replication

```bash
# PostgreSQL replication
# À configurer en base de données
```

---

## ✅ Checklist de déploiement

- [ ] Test local réussi
- [ ] Tests unitaires passants
- [ ] Variables d'environnement configurées
- [ ] Database migré et testé
- [ ] SSL/HTTPS activé
- [ ] DNS pointé vers le serveur
- [ ] Monitoring configuré
- [ ] Backups automatisés
- [ ] Health checks fonctionnels
- [ ] Documentation mise à jour
- [ ] Equipe informée du déploiement
- [ ] Plan de rollback préparé

---

## 🆘 Troubleshooting

### Conteneur ne démarre pas

```bash
docker logs seo-analyzer-pro
docker inspect seo-analyzer-pro
```

### Port 8000 déjà utilisé

```bash
lsof -i :8000
kill -9 <PID>
```

### Erreur de connexion database

```bash
# Vérifier la chaîne de connexion
echo $DATABASE_URL
# Vérifier que la base existe
psql $DATABASE_URL -c "SELECT 1"
```

### Temps de réponse lent

```bash
# Analyser avec htop
htop

# Analyser avec iotop
iotop
```

---

**Déploiement réussi! 🎉**

Pour plus d'aide: support@seoanalyzerpro.com
