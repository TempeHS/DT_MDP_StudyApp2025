# Study App Deployment Guide for Render.com

## Overview

This document provides step-by-step instructions for deploying the Python Flask Study App to Render.com.

## Prerequisites

- GitHub repository with your Flask application code
- Render.com account (free tier available)

## Files Created for Deployment

### 1. `requirements.txt`

Contains all Python dependencies needed for the application:

- Flask==3.1.2
- Flask-WTF==1.2.2
- gunicorn==23.0.0
- And other dependencies

### 2. `render.yaml` (Primary Configuration)

Render.com service configuration file that defines:

- Service type: web application
- Python environment
- Build command: `pip install -r requirements.txt && python init_db.py`
- Start command: `gunicorn --bind 0.0.0.0:$PORT main:app`
- Environment variables for production
- Health check endpoint

### 3. `Procfile` (Alternative Configuration)

Simple process file for deployment:

```
web: gunicorn main:app
```

### 4. `init_db.py`

Database initialization script that:

- Creates necessary database tables if they don't exist
- Ensures the database directory structure is correct
- Runs automatically during deployment

### 5. `.gitignore`

Prevents sensitive and unnecessary files from being committed to the repository.

## Deployment Steps

### Step 1: Prepare Your Repository

1. Ensure all the deployment files listed above are in your repository
2. Commit and push all changes to your GitHub repository:
   ```bash
   git add .
   git commit -m "Add deployment configuration for Render.com"
   git push origin main
   ```

### Step 2: Create Render.com Service

1. Log in to [Render.com](https://render.com/)
2. Click "New +" button and select "Web Service"
3. Connect your GitHub repository
4. Select your study app repository

### Step 3: Configure Deployment

Choose one of these configuration methods:

#### Option A: Using render.yaml (Recommended)

1. Render will automatically detect the `render.yaml` file
2. Review the configuration and click "Create Web Service"
3. Render will automatically configure:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt && python init_db.py`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT main:app`
   - Environment variables

#### Option B: Manual Configuration

1. If not using render.yaml, configure manually:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python init_db.py`
   - **Start Command**: `gunicorn main:app`
   - **Auto-Deploy**: Yes

### Step 4: Environment Variables

The following environment variables will be automatically set:

- `PORT`: Automatically provided by Render
- `SECRET_KEY`: Auto-generated secure key
- `FLASK_ENV`: Set to "production"
- `PYTHON_VERSION`: Set to 3.12.1

### Step 5: Deploy

1. Click "Create Web Service" or "Deploy"
2. Render will:
   - Build your application
   - Install dependencies
   - Initialize the database
   - Start the application

## Post-Deployment

### Accessing Your Application

- Your app will be available at: `https://your-service-name.onrender.com`
- The service name is configurable during setup

### Monitoring

- View logs in the Render dashboard
- Monitor application health via the built-in health check
- Check deployment status and build logs

### Database Management

- The SQLite database is file-based and will persist with your service
- For production applications, consider upgrading to a managed database service
- Current tables:
  - `user_details`: User account information
  - `syllabus`: Educational content and study materials

## Security Considerations

### Production Security Updates Made:

1. **Secret Key**: Uses environment variable instead of hardcoded value
2. **Debug Mode**: Automatically disabled in production
3. **CSRF Protection**: Enabled via Flask-WTF
4. **Environment-based Configuration**: Different settings for development vs. production

### Additional Security Recommendations:

1. **HTTPS**: Render.com provides free SSL certificates
2. **Database Security**: Consider migrating to PostgreSQL for production
3. **Input Validation**: Ensure all user inputs are properly validated
4. **Session Management**: Configure secure session settings
5. **Content Security Policy**: Implement CSP headers (endpoint exists at `/csp_report`)

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check requirements.txt for correct package versions
2. **Database Errors**: Ensure init_db.py runs successfully during build
3. **Import Errors**: Verify all dependencies are listed in requirements.txt
4. **Port Issues**: Render automatically sets PORT environment variable

### Logs and Debugging:

- View build logs in Render dashboard
- Check runtime logs for application errors
- Use the security_log.log file for application-specific logging

## Scaling and Upgrades

### Free Tier Limitations:

- Service goes to sleep after 15 minutes of inactivity
- 750 build hours per month
- Limited compute resources

### Upgrade Options:

- Starter plan: $7/month for always-on service
- Professional plans: Higher performance and resources
- Database upgrades: Managed PostgreSQL available

## Maintenance

### Regular Updates:

1. Keep dependencies updated in requirements.txt
2. Monitor security logs for any issues
3. Regularly backup your database
4. Update Python version as needed

### Automated Deployments:

- Enable auto-deploy from your main branch
- Every push to main will trigger a new deployment
- Use feature branches for development

## Support Resources

- [Render.com Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gunicorn Documentation](https://gunicorn.org/)

---

**Note**: This deployment guide assumes you're using the free tier of Render.com. For production applications with higher traffic, consider upgrading to a paid plan for better performance and reliability.
