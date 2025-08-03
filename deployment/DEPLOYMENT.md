# Deployment Guide

This guide covers deployment options for the Krippendorff Alpha web application to various cloud platforms.

## 🚀 Quick Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)

1. **Fork/Clone Repository** to your GitHub account
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Connect** your GitHub account
4. **Deploy** by selecting:
   - Repository: `your-username/krippendorff-alpha-python`
   - Branch: `main`
   - Main file path: `web_app/app.py`
5. **Advanced Settings**:
   - Python version: `3.11`
   - Requirements file: `web_app/requirements.txt`

**Pros**: Free, automatic SSL, custom domain support
**Cons**: Limited resources, may sleep with low traffic

### Option 2: Heroku (Easy with Free Tier)

1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create App**: `heroku create krippendorff-alpha-calculator`
4. **Set Stack**: `heroku stack:set container`
5. **Deploy**: `git push heroku main`

**Environment Variables**:
```bash
heroku config:set STREAMLIT_SERVER_HEADLESS=true
heroku config:set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Option 3: Docker (Any Platform)

```bash
# Build image
docker build -t krippendorff-alpha .

# Run locally
docker run -p 8501:8501 krippendorff-alpha

# Or use docker-compose
docker-compose up
```

### Option 4: Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/krippendorff-alpha
gcloud run deploy --image gcr.io/PROJECT-ID/krippendorff-alpha --platform managed
```

### Option 5: AWS App Runner

1. **Create `apprunner.yaml`**:
```yaml
version: 1.0
runtime: docker
build:
  commands:
    build:
      - echo "Building Docker image"
run:
  runtime-version: latest
  command: streamlit run web_app/app.py --server.port=8080 --server.address=0.0.0.0
  network:
    port: 8080
    env:
      - STREAMLIT_SERVER_HEADLESS=true
```

2. **Deploy via AWS Console** or CLI

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STREAMLIT_SERVER_PORT` | `8501` | Port for the web app |
| `STREAMLIT_SERVER_ADDRESS` | `0.0.0.0` | Bind address |
| `STREAMLIT_SERVER_HEADLESS` | `true` | Run without browser |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | `false` | Disable analytics |

### Resource Requirements

- **Minimum**: 512MB RAM, 1 vCPU
- **Recommended**: 1GB RAM, 1 vCPU  
- **For Heavy Use**: 2GB RAM, 2 vCPU

### Domain Setup

Most platforms support custom domains:
- **Streamlit Cloud**: Settings → Domain
- **Heroku**: `heroku domains:add krippendorff-alpha.yourdomain.com`
- **Vercel**: Project Settings → Domains

## 🔒 Security Considerations

### HTTPS
All major platforms provide automatic HTTPS. For custom deployments:
```bash
# Use nginx proxy with Let's Encrypt
certbot --nginx -d krippendorff-alpha.yourdomain.com
```

### Content Security Policy
The app includes secure headers in `netlify.toml`. For custom deployments, add:
```
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
```

### Data Privacy
- No data is stored permanently
- All processing happens in-memory
- Files are not cached between sessions

## 📊 Monitoring

### Health Checks
All platforms support the built-in health check:
```
GET /_stcore/health
```

### Logging
Streamlit provides built-in logging. For production:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Analytics
Optional analytics can be enabled via environment variables or Streamlit configuration.

## 🚨 Troubleshooting

### Common Issues

**Port Binding Error**:
```bash
# Ensure correct port binding
export PORT=8501
streamlit run web_app/app.py --server.port=$PORT
```

**Memory Issues**:
- Increase memory allocation
- Enable swap if available
- Consider caching strategies

**Import Errors**:
```bash
# Verify package installation
pip list | grep krippendorff
pip install -e .
```

**Performance Issues**:
- Enable Streamlit caching
- Optimize bootstrap iterations
- Consider async processing for large datasets

### Platform-Specific Issues

**Streamlit Cloud**:
- Check logs in dashboard
- Verify requirements.txt includes all dependencies
- Ensure Python version compatibility

**Heroku**:
- Check dyno logs: `heroku logs --tail`
- Verify Procfile or heroku.yml configuration
- Monitor dyno resource usage

**Docker**:
- Check container logs: `docker logs container_name`
- Verify port mapping
- Ensure all dependencies in image

## 📈 Scaling

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Multiple container instances
- Consider serverless functions for API endpoints

### Vertical Scaling
- Increase memory/CPU allocation
- Optimize algorithm performance
- Cache frequently used calculations

### Global Distribution
- Use CDN for static assets
- Deploy to multiple regions
- Consider edge computing for data processing

## 💰 Cost Optimization

### Free Tiers
- **Streamlit Cloud**: Unlimited public apps
- **Heroku**: 550-1000 dyno hours/month
- **Google Cloud Run**: 2M requests/month
- **AWS Lambda**: 1M requests/month

### Paid Options
- **Heroku**: $7/month for always-on dyno
- **Google Cloud Run**: Pay per request
- **AWS App Runner**: Pay per CPU/memory usage

## 🔄 CI/CD Pipeline

The repository includes GitHub Actions for:
- **Testing**: Run on Python 3.9, 3.10, 3.11
- **Docker**: Build and push to DockerHub
- **Deployment**: Auto-deploy to multiple platforms

### Manual Deployment

```bash
# Test locally first
streamlit run web_app/app.py

# Run validation
python -m krippendorff_alpha.validation

# Deploy to platform of choice
git push origin main  # Triggers CI/CD
```

## 📞 Support

For deployment issues:
- **GitHub Issues**: [Report deployment problems](https://github.com/wildboars/krippendorff-alpha-python/issues)
- **Discussions**: [Community help](https://github.com/wildboars/krippendorff-alpha-python/discussions)
- **Email**: research@wildboars.org

---

**Happy Deploying! 🚀**

*Making Krippendorff's Alpha accessible worldwide, one deployment at a time.*