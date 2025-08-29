# 🚀 Render Deployment Guide

This guide will walk you through deploying your Kenya Security Dashboard to Render.

## 📋 Prerequisites

- ✅ GitHub repository with your code (Already done!)
- ✅ Render account (Free tier available)
- ✅ Python 3.9+ compatibility

## 🔗 Step-by-Step Deployment

### 1. **Sign Up for Render**
- Go to [render.com](https://render.com)
- Sign up with your GitHub account
- Verify your email address

### 2. **Create New Web Service**
- Click **"New +"** button
- Select **"Web Service"**
- Connect your GitHub account if not already connected

### 3. **Connect Your Repository**
- Select **"Walter45guru/kenya-security-and-conflict"**
- Click **"Connect"**

### 4. **Configure Your Service**

#### **Basic Settings:**
- **Name**: `kenya-security-dashboard`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty (root of repo)

#### **Build & Deploy Settings:**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run kenya_dashboard.py --server.port $PORT --server.address 0.0.0.0`

#### **Environment Variables:**
- **PORT**: `$PORT` (Render sets this automatically)
- **PYTHON_VERSION**: `3.9.16`

### 5. **Advanced Settings (Optional)**
- **Auto-Deploy**: Enable for automatic updates
- **Health Check Path**: `/`
- **Health Check Timeout**: `300`

### 6. **Create Service**
- Click **"Create Web Service"**
- Render will start building your application

## ⏱️ Build Process

The build process typically takes 5-10 minutes and includes:

1. **Environment Setup**: Python 3.9.16 installation
2. **Dependencies**: Installing all packages from requirements.txt
3. **Streamlit Configuration**: Setting up production environment
4. **Service Launch**: Starting your dashboard

## 🌐 Access Your Dashboard

Once deployment is complete, you'll get:
- **Live URL**: `https://your-app-name.onrender.com`
- **Status**: Active and running
- **Logs**: Real-time deployment and runtime logs

## 🔧 Troubleshooting

### **Common Issues:**

#### **Build Failures:**
- Check requirements.txt compatibility
- Verify Python version compatibility
- Review build logs for specific errors

#### **Runtime Errors:**
- Check Streamlit configuration
- Verify environment variables
- Review runtime logs

#### **Performance Issues:**
- Free tier has limitations
- Consider upgrading for production use
- Optimize data loading and caching

### **Useful Commands:**
```bash
# Check deployment status
curl https://your-app-name.onrender.com

# View logs in Render dashboard
# Go to your service → Logs tab
```

## 📊 Monitoring & Maintenance

### **Render Dashboard Features:**
- **Real-time Logs**: Monitor application performance
- **Metrics**: CPU, memory, and response time
- **Deployments**: Track deployment history
- **Environment Variables**: Manage configuration

### **Health Checks:**
- **Automatic**: Render monitors your service
- **Manual**: Check `/` endpoint for 200 response
- **Alerts**: Get notified of service issues

## 🔄 Updates & Redeployment

### **Automatic Updates:**
- Push to `main` branch
- Render automatically redeploys
- Zero downtime updates

### **Manual Redeployment:**
- Go to your service in Render
- Click **"Manual Deploy"**
- Select branch and deploy

## 💰 Pricing & Limits

### **Free Tier:**
- **Build Time**: 500 minutes/month
- **Runtime**: 750 hours/month
- **Bandwidth**: 100 GB/month
- **Sleep Mode**: After 15 minutes of inactivity

### **Paid Plans:**
- **Starter**: $7/month
- **Standard**: $25/month
- **Professional**: $100/month

## 🚨 Important Notes

### **Free Tier Limitations:**
- Service sleeps after 15 minutes of inactivity
- First request after sleep may take 30-60 seconds
- Limited build and runtime hours per month

### **Production Considerations:**
- Upgrade to paid plan for production use
- Set up custom domain
- Configure SSL certificates
- Set up monitoring and alerts

## 📞 Support

### **Render Support:**
- [Documentation](https://render.com/docs)
- [Community Forum](https://community.render.com)
- [Email Support](mailto:support@render.com)

### **Dashboard Issues:**
- Check GitHub repository issues
- Review Streamlit documentation
- Contact maintainer through GitHub

## 🎯 Next Steps

After successful deployment:

1. **Test Your Dashboard**: Verify all features work correctly
2. **Share Your URL**: Distribute the live dashboard link
3. **Monitor Performance**: Watch logs and metrics
4. **Gather Feedback**: Collect user input for improvements
5. **Plan Updates**: Schedule regular maintenance and updates

---

**🎉 Congratulations! Your Kenya Security Dashboard is now live on the web!**

**Live URL**: `https://your-app-name.onrender.com`
**GitHub Repo**: [Walter45guru/kenya-security-and-conflict](https://github.com/Walter45guru/kenya-security-and-conflict)
