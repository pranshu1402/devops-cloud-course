# GitHub Actions CI/CD Pipeline Setup Guide

## 🚀 Overview

This guide explains how to set up and configure the GitHub Actions CI/CD pipeline for the Expense Tracker application. The pipeline automates testing, building, and deployment to multiple environments.

## 📋 Workflow Overview

The GitHub Actions workflow (`/.github/workflows/ci-cd.yml`) includes the following jobs:

### 1. **Test Job** (Runs on all branches)
- **Install Dependencies**: Installs Python packages using pip
- **Run Linting**: Executes flake8 for code quality checks
- **Security Checks**: Runs bandit for security analysis
- **Run Tests**: Executes pytest with coverage reporting
- **Upload Results**: Stores test results and coverage reports

### 2. **Build Job** (Runs on main branch)
- **Build Application**: Compiles Python files
- **Create Artifact**: Packages application for deployment
- **Upload Artifact**: Stores build artifacts

### 3. **Deploy to Staging** (Runs on staging branch)
- **Deploy to Staging Server**: Deploys application to staging environment
- **Health Check**: Verifies deployment success
- **Notifications**: Sends Slack notifications

### 4. **Deploy to Production** (Runs on release)
- **Deploy to Production Server**: Deploys application to production
- **Rollback Support**: Automatic rollback on failure
- **Health Check**: Verifies deployment success
- **Notifications**: Sends Slack notifications

### 5. **Docker Build** (Runs on main branch)
- **Build Docker Image**: Creates containerized application
- **Push to Registry**: Uploads to Docker Hub

## 🔧 Setup Instructions

### 1. Repository Setup

#### 1.1 Fork and Clone
```bash
# Fork the repository on GitHub
# Clone to your local machine
git clone https://github.com/YOUR_USERNAME/devops-cloud-course.git
cd devops-cloud-course
```

#### 1.2 Create Required Branches
```bash
# Create staging branch
git checkout -b staging
git push -u origin staging

# Create develop branch
git checkout -b develop
git push -u origin develop
```

### 2. GitHub Secrets Configuration

Navigate to your repository on GitHub:
**Settings > Secrets and variables > Actions**

#### 2.1 Staging Environment Secrets
```
STAGING_HOST=your-staging-server-ip
STAGING_USERNAME=your-staging-username
STAGING_SSH_KEY=your-staging-ssh-private-key
STAGING_PORT=22
STAGING_DB_URI=your-staging-database-uri
STAGING_SECRET_KEY=your-staging-secret-key
```

#### 2.2 Production Environment Secrets
```
PRODUCTION_HOST=your-production-server-ip
PRODUCTION_USERNAME=your-production-username
PRODUCTION_SSH_KEY=your-production-ssh-private-key
PRODUCTION_PORT=22
PRODUCTION_DB_URI=your-production-database-uri
PRODUCTION_SECRET_KEY=your-production-secret-key
```

#### 2.3 Docker Hub Secrets
```
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password
```

#### 2.4 Notification Secrets
```
SLACK_WEBHOOK_URL=your-slack-webhook-url
```

### 3. Environment Setup

#### 3.1 Staging Server Setup
```bash
# SSH to your staging server
ssh user@staging-server

# Install required packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx curl

# Create systemd service file
sudo tee /etc/systemd/system/expense-tracker-staging.service > /dev/null <<EOF
[Unit]
Description=Expense Tracker Staging
After=network.target

[Service]
Type=simple
User=jenkins
WorkingDirectory=/opt/expense-tracker-staging
Environment=PATH=/opt/expense-tracker-staging/venv/bin
ExecStart=/opt/expense-tracker-staging/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create deployment directory
sudo mkdir -p /opt/expense-tracker-staging
sudo chown jenkins:jenkins /opt/expense-tracker-staging
```

#### 3.2 Production Server Setup
```bash
# SSH to your production server
ssh user@production-server

# Install required packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx curl

# Create systemd service file
sudo tee /etc/systemd/system/expense-tracker-production.service > /dev/null <<EOF
[Unit]
Description=Expense Tracker Production
After=network.target

[Service]
Type=simple
User=jenkins
WorkingDirectory=/opt/expense-tracker-production
Environment=PATH=/opt/expense-tracker-production/venv/bin
ExecStart=/opt/expense-tracker-production/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create deployment directory
sudo mkdir -p /opt/expense-tracker-production
sudo chown jenkins:jenkins /opt/expense-tracker-production
```

### 4. Nginx Configuration (Optional)

#### 4.1 Staging Nginx Config
```bash
sudo tee /etc/nginx/sites-available/expense-tracker-staging > /dev/null <<EOF
server {
    listen 80;
    server_name staging.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/expense-tracker-staging /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4.2 Production Nginx Config
```bash
sudo tee /etc/nginx/sites-available/expense-tracker-production > /dev/null <<EOF
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/expense-tracker-production /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔄 Workflow Triggers

### Automatic Triggers
- **Push to main**: Runs test and build jobs
- **Push to staging**: Runs test and deploy to staging
- **Push to develop**: Runs test job only
- **Pull Request**: Runs test job for validation
- **Release Published**: Runs test, build, and deploy to production

### Manual Triggers
You can also trigger workflows manually:
1. Go to **Actions** tab in your repository
2. Select the workflow
3. Click **Run workflow**
4. Choose branch and click **Run workflow**

## 📊 Monitoring and Notifications

### 1. GitHub Actions Dashboard
- View workflow runs in the **Actions** tab
- Monitor job status and logs
- Download artifacts

### 2. Slack Notifications
The workflow sends notifications to Slack for:
- Staging deployment success/failure
- Production deployment success/failure

### 3. Health Checks
- Staging: `http://staging-server:5000/health`
- Production: `http://production-server:5000/health`

## 🧪 Testing Strategy

### 1. Unit Tests
- Location: `expense-tracker-main/tests/`
- Framework: pytest
- Coverage reporting enabled
- Runs on every push and PR

### 2. Code Quality
- Linting: flake8
- Security: bandit
- Configuration files included

### 3. Integration Tests
- Health check endpoint
- Database connectivity tests
- Service availability checks

## 🚀 Deployment Strategy

### 1. Staging Deployment
- **Trigger**: Push to `staging` branch
- **Strategy**: Direct deployment
- **Rollback**: Manual intervention required

### 2. Production Deployment
- **Trigger**: Release published
- **Strategy**: Blue-green deployment with rollback
- **Safety**: Automatic rollback on health check failure

### 3. Docker Deployment
- **Trigger**: Push to `main` branch
- **Registry**: Docker Hub
- **Tags**: `latest` and commit SHA

## 🔒 Security Considerations

### 1. Secrets Management
- All sensitive data stored in GitHub Secrets
- Environment-specific secrets
- No secrets in code or logs

### 2. Access Control
- SSH key-based authentication
- Limited user permissions on servers
- Environment isolation

### 3. Network Security
- Firewall configuration
- HTTPS for production
- Internal service communication

## 🚨 Troubleshooting

### Common Issues

#### 1. Workflow Fails on Test
```bash
# Check test logs
# Verify Python version compatibility
# Check dependency installation

# Run tests locally
cd expense-tracker-main
python -m pytest tests/ -v
```

#### 2. Deployment Fails
```bash
# Check server connectivity
ssh user@server

# Check service status
sudo systemctl status expense-tracker-staging
sudo journalctl -u expense-tracker-staging -f

# Check permissions
ls -la /opt/expense-tracker-staging/
```

#### 3. Health Check Fails
```bash
# Check if service is running
curl http://localhost:5000/health

# Check logs
sudo journalctl -u expense-tracker-staging -f

# Check database connectivity
# Verify environment variables
```

#### 4. Docker Build Fails
```bash
# Check Docker Hub credentials
# Verify Dockerfile syntax
# Check build context
```

### Debugging Steps

1. **Check Workflow Logs**
   - Go to Actions tab
   - Click on failed workflow
   - Review step-by-step logs

2. **Local Testing**
   - Run tests locally
   - Test deployment scripts
   - Verify environment setup

3. **Server Verification**
   - SSH to servers
   - Check service status
   - Verify file permissions

## 📈 Best Practices

### 1. Branch Strategy
- `main`: Production-ready code
- `staging`: Pre-production testing
- `develop`: Development work
- Feature branches: Individual features

### 2. Release Process
1. Merge feature branches to `develop`
2. Test on `develop` branch
3. Merge `develop` to `staging`
4. Test on staging environment
5. Merge `staging` to `main`
6. Create release tag
7. Deploy to production

### 3. Monitoring
- Set up application monitoring
- Configure alerting
- Monitor resource usage
- Track deployment metrics

### 4. Backup Strategy
- Database backups
- Application backups
- Configuration backups
- Disaster recovery plan

## 🔄 Continuous Improvement

### 1. Performance Optimization
- Cache dependencies
- Parallel job execution
- Optimize build times
- Reduce artifact sizes

### 2. Security Enhancements
- Regular dependency updates
- Security scanning
- Vulnerability assessments
- Access reviews

### 3. Monitoring Enhancements
- Application performance monitoring
- Infrastructure monitoring
- Log aggregation
- Alerting improvements

---

## 📝 Notes

- Always test changes in staging before production
- Keep secrets secure and rotate regularly
- Monitor workflow performance and costs
- Document any custom configurations
- Regular backup and disaster recovery testing 