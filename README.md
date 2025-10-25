# 🤖 Motivational Twitter Bot

A fully automated Twitter bot that posts daily motivational quotes to inspire your followers. Built with Python and deployed using GitHub Actions - **completely free!**

## ✨ Features

- 🔄 **Daily Automated Posting**: Posts motivational quotes every day at 9 AM UTC
- 🎯 **Smart Hashtag System**: Automatically adds relevant hashtags like #Motivation, #Success
- 📚 **Rich Quote Database**: 100+ carefully curated motivational quotes
- 🚀 **Zero Cost Deployment**: Uses GitHub Actions for free automation
- 📊 **Comprehensive Logging**: Track bot activity and troubleshoot issues
- 🛡️ **Error Handling**: Robust error handling for API limits and network issues

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your Twitter API Keys

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app or use your existing one
3. Navigate to "Keys and Tokens" tab
4. Generate/Copy these keys:
   - API Key
   - API Secret Key
   - Access Token
   - Access Token Secret
   - Bearer Token

### Step 2: Fork & Configure Repository

1. **Fork this repository** to your GitHub account
2. In your forked repo, go to **Settings → Secrets and Variables → Actions**
3. Click **"New repository secret"** and add these secrets:

```
Name: TWITTER_API_KEY
Value: [Your API Key]

Name: TWITTER_API_SECRET  
Value: [Your API Secret Key]

Name: TWITTER_ACCESS_TOKEN
Value: [Your Access Token]

Name: TWITTER_ACCESS_TOKEN_SECRET
Value: [Your Access Token Secret]

Name: TWITTER_BEARER_TOKEN
Value: [Your Bearer Token]
```

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. The bot will now post daily at 9 AM UTC automatically!

## 🧪 Test Your Bot

### Test Locally (Optional)

1. Clone your repository:
```bash
git clone https://github.com/YOUR_USERNAME/motivational-twitter-bot.git
cd motivational-twitter-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Edit `.env` with your Twitter API keys

5. Run the bot:
```bash
python twitter_bot.py
```

### Test on GitHub

- Go to **Actions** tab → **Daily Motivational Quote Bot**
- Click **"Run workflow"** to test immediately

## ⚙️ Customization

### Change Posting Schedule

Edit `.github/workflows/daily-quote.yml`:

```yaml
schedule:
  # Post at 6 PM UTC (adjust as needed)
  - cron: '0 18 * * *'
```

**Cron Schedule Examples:**
- `0 9 * * *` - Daily at 9 AM UTC
- `0 6,18 * * *` - Twice daily (6 AM & 6 PM UTC)  
- `0 9 * * 1-5` - Weekdays only at 9 AM UTC

### Add Your Own Quotes

Edit `data/quotes.json`:

```json
{
  "quotes": [
    "Your custom motivational quote here! - Author Name",
    "Another inspiring quote - Another Author"
  ]
}
```

### Customize Hashtags

Edit `twitter_bot.py` in the `add_hashtags()` function:

```python
hashtags = [
    "#YourCustomTag", "#Motivation", "#Success", 
    "#PersonalBrand", "#Inspiration"
]
```

## 📊 Monitoring & Logs

- **GitHub Actions**: Check the Actions tab for execution logs
- **Rate Limits**: Bot automatically handles Twitter API rate limits
- **Error Handling**: Failed posts are logged with detailed error messages

## 🔧 Troubleshooting

### Common Issues:

**❌ "Authentication failed"**
- Double-check your Twitter API keys in GitHub Secrets
- Ensure you have the correct permissions in your Twitter Developer account

**❌ "Rate limit exceeded"** 
- Twitter Free tier: 50 tweets/month
- Bot automatically waits for rate limits to reset

**❌ "Workflow not running"**
- Ensure GitHub Actions are enabled in your repository
- Check if you've made at least one commit to trigger workflows

**❌ "Import errors"**
- Make sure `requirements.txt` is properly configured
- Check Python version compatibility (uses Python 3.9)

## 📈 Usage Stats

- **Free Tier Limits**: Up to 50 tweets per month (1.6 tweets per day)
- **GitHub Actions**: 2,000 free minutes per month (more than enough)
- **Storage**: Minimal - entire project is under 1MB

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 What's Next?

- **Image Quotes**: Generate quote images using Pillow
- **Engagement Tracking**: Monitor likes, retweets, and engagement
- **Multiple Categories**: Different themes for different days
- **Quote API Integration**: Pull from external quote APIs
- **Analytics Dashboard**: Track performance metrics

---

## 💡 Pro Tips

- **Engagement**: Post during your audience's active hours
- **Content**: Mix famous quotes with lesser-known gems
- **Consistency**: The bot ensures you never miss a day
- **Growth**: Engage with your audience beyond automated posts

**Made with ❤️ for the motivation community. Start inspiring others today!** 

---

### 🆘 Need Help?

- Check existing [Issues](../../issues) for common problems
- Create a new issue if you encounter bugs
- Star ⭐ this repository if it helps you!