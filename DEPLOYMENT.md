# 🚀 Deployment Guide

This guide covers various deployment options for the PSL Data Science Project.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Production Server](#production-server)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 1. Local Development

### Setup

```bash
# Clone repository
git clone <repository-url>
cd psl

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Flask App

```bash
python flask_app.py
```

Access at: http://localhost:5000

---

## 2. Production Server

### Using Gunicorn (Linux)

```bash
# Install gunicorn
pip install gunicorn

# Run with 4 worker processes
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app

# With logging
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile logs/access.log --error-logfile logs/error.log flask_app:app

# As background process
nohup gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app > logs/gunicorn.log 2>&1 &
```

### Using Waitress (Windows)

```bash
# Install waitress
pip install waitress

# Run server
waitress-serve --port=5000 flask_app:app
```

### Nginx Configuration (Recommended)

Create `/etc/nginx/sites-available/psl-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/psl-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 3. Docker Deployment

### Single Container

```bash
# Build image
docker build -t psl-project:latest .

# Run container
docker run -d \
  --name psl-api \
  -p 5000:5000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  psl-project:latest

# View logs
docker logs -f psl-api

# Stop container
docker stop psl-api

# Remove container
docker rm psl-api
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Docker Compose with Nginx

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: psl_flask_app
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
    restart: unless-stopped

  nginx:
    image: nginx:latest
    container_name: psl_nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
    restart: unless-stopped
```

Run:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 4. Cloud Deployment

### AWS (EC2)

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.medium or larger
   - Configure security group (port 5000, 80, 443)

2. **Connect and Setup**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone <repository-url>
cd psl

# Setup and run (as shown in Production Server section)
```

3. **Configure Nginx** (as shown above)

4. **Setup SSL** (optional)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### AWS (ECS with Docker)

1. **Build and push to ECR**
```bash
# Authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t psl-project .
docker tag psl-project:latest your-account.dkr.ecr.us-east-1.amazonaws.com/psl-project:latest

# Push
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/psl-project:latest
```

2. **Create ECS Task Definition**
3. **Create ECS Service**
4. **Configure Load Balancer**

### Azure (App Service)

```bash
# Login
az login

# Create resource group
az group create --name psl-rg --location eastus

# Create App Service plan
az appservice plan create --name psl-plan --resource-group psl-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group psl-rg --plan psl-plan --name psl-api --runtime "PYTHON|3.9"

# Deploy
az webapp up --name psl-api --resource-group psl-rg
```

### Google Cloud (Cloud Run)

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/psl-project

# Deploy to Cloud Run
gcloud run deploy psl-api \
  --image gcr.io/your-project/psl-project \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku

```bash
# Login
heroku login

# Create app
heroku create psl-api

# Deploy
git push heroku main

# Open
heroku open
```

---

## 5. Monitoring & Maintenance

### Health Checks

```bash
# Check API health
curl http://your-domain.com/health

# Automated monitoring script
while true; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
  if [ $STATUS -ne 200 ]; then
    echo "API is down! Status: $STATUS"
    # Send alert or restart service
  fi
  sleep 60
done
```

### Logging

Monitor logs:
```bash
# Docker
docker logs -f psl-api

# System logs
tail -f logs/app.log
tail -f logs/access.log
tail -f logs/error.log
```

### Performance Monitoring

Install monitoring tools:
```bash
pip install prometheus-flask-exporter

# Add to flask_app.py:
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
```

### Backup Strategy

```bash
# Backup models
tar -czf models-backup-$(date +%Y%m%d).tar.gz models/

# Backup data
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)

tar -czf $BACKUP_DIR/models-$DATE.tar.gz models/
tar -czf $BACKUP_DIR/data-$DATE.tar.gz data/

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Updates and Maintenance

```bash
# Pull latest code
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Restart service
# Docker
docker-compose restart

# Gunicorn
pkill gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

---

## 🔒 Security Best Practices

1. **Environment Variables**: Use `.env` file for sensitive data
2. **HTTPS**: Always use SSL/TLS in production
3. **API Keys**: Implement API key authentication
4. **Rate Limiting**: Add rate limiting to API endpoints
5. **Firewall**: Configure firewall rules
6. **Updates**: Keep dependencies up to date
7. **Monitoring**: Monitor for suspicious activity

---

## 📊 Performance Optimization

1. **Caching**: Implement Redis for caching
2. **Load Balancing**: Use load balancer for multiple instances
3. **Database**: Use PostgreSQL for production data
4. **CDN**: Use CDN for static assets
5. **Compression**: Enable gzip compression
6. **Async**: Use async workers for heavy operations

---

## 🆘 Troubleshooting

### API Not Responding
```bash
# Check if service is running
ps aux | grep flask
ps aux | grep gunicorn

# Check ports
netstat -tulpn | grep 5000

# Check logs
tail -f logs/*.log
```

### Model Loading Issues
```bash
# Verify model file exists
ls -lh models/

# Check permissions
chmod 644 models/*.pkl

# Test model loading
python -c "import joblib; model = joblib.load('models/psl_model.pkl'); print('Model loaded successfully')"
```

### Docker Issues
```bash
# Check container status
docker ps -a

# View logs
docker logs psl-api

# Rebuild image
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📞 Support

For deployment issues:
- Check logs first
- Review this guide
- Open an issue on GitHub
- Contact: mfarooqshafee333@gmail.com
- GitHub: [@Muhamma-Farooq-13](https://github.com/Muhamma-Farooq-13)

---

**Happy Deploying! 🚀**
