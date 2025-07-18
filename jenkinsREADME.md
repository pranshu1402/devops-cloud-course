# 🚀 Jenkins CI/CD Pipeline Setup Guide

### Prerequisites
- Jenkins server installed and configured
- Git repository access
- Python 3.10+ installed on Jenkins server
- Docker (optional, for containerized deployment)

### 📋 Step-by-Step Setup Instructions

#### 1. Fork and Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/devops-cloud-course.git
cd devops-cloud-course
```

#### 2. Jenkins Configuration

##### 2.1 Install Required Jenkins Plugins
Navigate to **Manage Jenkins > Manage Plugins** and install:
- Pipeline
- Git Integration
- Email Extension Plugin
- HTML Publisher Plugin
- Workspace Cleanup Plugin
- Blue Ocean (optional, for better UI)

##### 2.2 Configure Email Notifications
1. Go to **Manage Jenkins > Configure System**
2. Find **Extended E-mail Notification** section
3. Configure SMTP settings:
   ```
   SMTP server: smtp.gmail.com
   SMTP Port: 587
   Use SSL: Yes
   Use TLS: Yes
   Username: your-email@gmail.com
   Password: your-app-password
   ```

##### 2.3 Create Jenkins Pipeline Job
1. Click **New Item** > **Pipeline**
2. Name: `expense-tracker-pipeline`
3. Configure:
   - **Pipeline**: Definition from SCM
   - **SCM**: Git
   - **Repository URL**: Your forked repository URL
   - **Branch**: `*/main`
   - **Script Path**: `jenkinsfile`

#### 3. Environment Variables Setup

##### 3.1 Jenkins Credentials
Go to **Manage Jenkins > Manage Credentials** and add:
- **STAGING_DB_URI**: Your staging database connection string
- **STAGING_SECRET_KEY**: Your Flask secret key for staging

##### 3.2 Pipeline Environment Variables
In your Jenkins job configuration, add these environment variables:
```
STAGING_DB_URI=your_staging_database_uri
STAGING_SECRET_KEY=your_staging_secret_key
```

#### 4. Pipeline Stages Overview

The Jenkinsfile includes the following stages:

1. **Checkout**: Clones the repository
2. **Setup Python Environment**: Creates virtual environment
3. **Install Dependencies**: Installs Python packages
4. **Lint Check**: Runs flake8 for code quality
5. **Security Check**: Runs bandit for security analysis
6. **Unit Tests**: Runs pytest with coverage
7. **Build Application**: Compiles Python files
8. **Deploy to Staging**: Deploys to staging environment (main branch only)
9. **Health Check**: Verifies application is running

#### 5. Triggers Configuration

The pipeline is configured with:
- **SCM Polling**: Every 5 minutes (`H/5 * * * *`)
- **Webhook Support**: Can be configured for immediate triggers

#### 6. Notifications

Email notifications are sent for:
- **Success**: When pipeline completes successfully
- **Failure**: When pipeline fails at any stage

### 🔧 Manual Deployment Steps

#### Local Development Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r expense-tracker-main/requirements.txt

# Set environment variables
export DB_URI="your_database_uri"
export SECRET_KEY="your_secret_key"

# Run the application
cd expense-tracker-main
flask run
```

#### Staging Deployment
```bash
# SSH to your staging server
ssh user@staging-server

# Clone repository
git clone https://github.com/YOUR_USERNAME/devops-cloud-course.git
cd devops-cloud-course

# Create deployment directory
sudo mkdir -p /opt/expense-tracker-staging

# Copy application files
sudo cp -r expense-tracker-main/* /opt/expense-tracker-staging/

# Set up virtual environment
cd /opt/expense-tracker-staging
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
echo "export DB_URI=your_staging_db_uri" | sudo tee .env
echo "export SECRET_KEY=your_staging_secret_key" | sudo tee -a .env

# Create systemd service
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

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable expense-tracker-staging
sudo systemctl start expense-tracker-staging
```

### 🧪 Testing

#### Running Tests Locally
```bash
cd expense-tracker-main
source venv/bin/activate
pip install pytest pytest-cov
python -m pytest tests/ -v --cov=. --cov-report=html
```

#### Test Coverage
- Tests are located in `expense-tracker-main/tests/`
- Coverage reports are generated in HTML format
- Jenkins publishes coverage reports automatically

### 📊 Monitoring

#### Health Check Endpoint
- URL: `http://your-server:5000/health`
- Returns JSON with application status
- Tests database connectivity

#### Logs
```bash
# View application logs
sudo journalctl -u expense-tracker-staging -f

# View Jenkins build logs
# Available in Jenkins web interface
```

### 🔒 Security Considerations

1. **Environment Variables**: Never commit secrets to repository
2. **Database Security**: Use strong passwords and SSL connections
3. **Network Security**: Configure firewalls appropriately
4. **Regular Updates**: Keep dependencies updated

### 🚨 Troubleshooting

#### Common Issues

1. **Python Version Mismatch**
   ```bash
   # Ensure Python 3.10+ is installed
   python3 --version
   ```

2. **Permission Issues**
   ```bash
   # Fix permissions for deployment directory
   sudo chown -R jenkins:jenkins /opt/expense-tracker-staging
   ```

3. **Database Connection Issues**
   - Verify database URI format
   - Check network connectivity
   - Ensure database server is running

4. **Email Notifications Not Working**
   - Verify SMTP settings
   - Check Jenkins logs for email errors
   - Ensure recipient emails are configured

### 📈 Pipeline Metrics

The pipeline provides:
- Build duration tracking
- Test coverage reports
- Security scan results
- Deployment status
- Email notifications

### 🔄 Continuous Improvement

- Monitor pipeline performance
- Add more test cases
- Implement automated security scanning
- Set up production deployment pipeline
- Configure monitoring and alerting

---

## 📝 Notes

- The pipeline is configured for staging deployment only
- Production deployment should have additional security measures
- Consider implementing blue-green deployment for zero-downtime updates
- Regular backup of application data is recommended

