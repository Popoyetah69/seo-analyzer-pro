#!/usr/bin/env python3
"""
CUSTOMER ONBOARDING SYSTEM
Automated emails and tasks to convert new customers into paying, happy users
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json

# Install: pip install python-dotenv

from dotenv import load_dotenv
import os

load_dotenv()

# ============================================================================
# EMAIL TEMPLATES
# ============================================================================

ONBOARDING_EMAILS = {
    
    "welcome": {
        "subject": "✅ Welcome to SEO Analyzer Pro!",
        "delay_hours": 0,
        "body": """
Hi {name},

Welcome to SEO Analyzer Pro! 🎉

Your account is all set up and ready to use. Here's how to get started:

STEP 1: Log In
→ Visit: https://app.seoanalyzerpro.com
→ Email: {email}
→ Password: (use the one you created)

STEP 2: Complete Your Profile
→ Add your company size
→ Tell us your main industry
→ (takes 2 minutes, helps us personalize your experience)

STEP 3: Run Your First Analysis
→ Enter 3-5 keywords you want to rank for
→ Click "Analyze"
→ See instant insights!

STEP 4: Check Out These Features
→ Competitor Analysis: See what your rivals rank for
→ Content Generator: Get SEO-optimized outlines
→ Batch Upload: Analyze 100+ keywords at once

WHAT'S INCLUDED IN YOUR {plan} PLAN:
{features}

NEED HELP?
→ Check our guides: https://docs.seoanalyzerpro.com
→ Watch video tutorials: https://youtube.com/@seoanalyzerpro
→ Email support: support@seoanalyzerpro.com

You've got this! 🚀

Best,
The SEO Analyzer Pro Team
"""
    },
    
    "first_use_nudge": {
        "subject": "👋 Your first keyword analysis (takes 2 min)",
        "delay_hours": 2,
        "body": """
Hi {name},

Quick check-in: Have you had a chance to log in yet?

If not, no worries! Most people get their first "aha moment" within 2 minutes of using SEO Analyzer Pro.

Here's exactly what to do:

1. Log in: https://app.seoanalyzerpro.com
2. Enter any keyword (your business name works great)
3. Click "Analyze"
4. See your instant insights

That's it!

Want ideas? Try these keywords:
- "{keyword_1}"
- "{keyword_2}"
- Any keyword your competitors rank for

Questions? Just reply to this email.

Best,
{your_name}
SEO Analyzer Pro
"""
    },
    
    "tutorial_video": {
        "subject": "📹 How to use Competitor Analysis (3 min video)",
        "delay_hours": 24,
        "body": """
Hi {name},

The Competitor Analysis feature is usually where people find the most value.

Here's why: Most SEO tools show you keywords that rank. We show you keywords your COMPETITORS rank for.

Watch this 3-minute video to see it in action:
→ https://youtube.com/watch?v=seoanalyzerpro-competitor-analysis

You'll learn how to:
✓ Analyze your top 3 competitors
✓ Find keywords they rank for that you don't
✓ Discover content gaps you can exploit
✓ Steal their traffic (ethically! 😄)

After watching, try it on your own competitors.

Questions? Hit reply.

Best,
{your_name}
"""
    },
    
    "first_win": {
        "subject": "🎯 Found your first opportunity keyword!",
        "delay_hours": 72,
        "body": """
Hi {name},

Congrats! You've been using SEO Analyzer Pro for 3 days.

I wanted to check in: Have you found any useful keywords yet?

Most of our best customers find:
- 5-15 low-competition keywords in their first week
- 3-5 content gaps from competitors
- 2-3 trending keywords no one else is targeting yet

If you're seeing good data, here's what's next:

STEP 1: Pick 1 keyword you love
STEP 2: Use our Content Generator to create an outline
STEP 3: Write the article
STEP 4: Publish and watch the rankings climb

Have you tried the Content Generator yet?

It's one of the features that usually gets the most excitement.
→ https://app.seoanalyzerpro.com/content-generator

Let me know if you have questions!

Best,
{your_name}
SEO Analyzer Pro Support
"""
    },
    
    "upgrade_offer": {
        "subject": "⭐ Unlock 10x more keywords (upgrade special)",
        "delay_hours": 168,  # After 1 week
        "body": """
Hi {name},

Quick question: Are you hitting your keyword limit yet?

Most {plan} customers burn through their monthly keywords by week 2 of launching content.

Here's what we've seen work:
- Starter → Professional: Analyze 10x more keywords, get AI content generation
- Professional → Enterprise: Unlimited keywords + white-label option

Actually, here's a 30% upgrade discount valid through end of month:

Starter → Professional: $49 → $34.30/month
Professional → Enterprise: $199 → $139.30/month

Code: EXPAND30

→ Upgrade here: https://app.seoanalyzerpro.com/billing

This usually pays for itself on day 1 (you find that one high-traffic keyword).

Questions? Just reply!

Best,
{your_name}
"""
    },
    
    "feature_highlight": {
        "subject": "💡 Most customers miss this feature",
        "delay_hours": 240,  # After 10 days
        "body": """
Hi {name},

I was reviewing your account and noticed you haven't used the Batch Upload feature yet.

This is usually where customers save 10+ hours per month.

Here's why: Instead of analyzing keywords one-by-one, you can:
✓ Upload 100+ keywords via CSV
✓ Get results in 60 seconds
✓ Export everything to a spreadsheet

It's a game-changer for agencies.

How to use it:
1. Download this sample CSV: https://docs.seoanalyzerpro.com/batch-example.csv
2. Edit with your keywords
3. Upload to https://app.seoanalyzerpro.com/batch-upload
4. Boom - instant analysis

Try it out!

Questions? Reply!

Best,
{your_name}
"""
    },
    
    "success_story": {
        "subject": "📈 Look what this customer found",
        "delay_hours": 336,  # After 2 weeks
        "body": """
Hi {name},

One of our customers (Sarah, from a digital agency) just shared this win:

"Using SEO Analyzer Pro's Competitor Analysis, I found 15 keywords that our competitors rank for but we don't. I created content for 3 of them last week, and we're already ranking #8-#12. This tool literally paid for itself in week 1."

This is pretty typical for our Professional plan users.

Have you tried the Competitor Analysis yet?

It usually takes 15 minutes and you'll find 5-10 keywords to target.

→ Try it: https://app.seoanalyzerpro.com/competitor-analysis

Let me know what you find!

Best,
{your_name}
"""
    },
    
    "churn_prevention": {
        "subject": "👋 Before you go... (special offer inside)",
        "delay_hours": 600,  # If inactive after 25 days
        "body": """
Hi {name},

I noticed you haven't logged in for a few days. No stress - happens to everyone!

But before you forget about us, I wanted to share something:

The biggest ROI from SEO Analyzer Pro comes in weeks 2-4, when you:
✓ Find your winning keywords
✓ Create content around them
✓ Start seeing rankings jump

Most people give up too early.

Here's what you're probably missing:
- 1-2 keywords worth $5K+/month in traffic
- 3-5 competitor gaps nobody's targeting
- A month-by-month content roadmap

Plus, we just added new AI features that make content creation 10x faster.

Here's what I want to do: Give you a free 20-minute strategy call.

I'll look at your niche, find 3 opportunities you're missing, and show you exactly how to use SEO Analyzer Pro to capitalize on them.

→ Book here: https://calendly.com/seoanalyzerpro/strategy-call

No sales pitch. Just strategy.

If you still want to cancel after that, no hard feelings!

But I think you'll see why people love this tool.

Best,
{your_name}
SEO Analyzer Pro Team
"""
    },
    
    "customer_appreciation": {
        "subject": "🙏 Thank you for 1 month with us!",
        "delay_hours": 720,  # After 1 month
        "body": """
Hi {name},

Today marks 1 month of you using SEO Analyzer Pro!

Thank you! 🎉

I wanted to check in: How's it going?

Are you:
✓ Finding keywords you can rank for?
✓ Analyzing competitors successfully?
✓ Using the AI content generator?

I'd love to hear what's working (and what isn't).

Just hit reply and let me know!

INSIDER TIP: You're eligible for our "1-Month Success Bonus"
✓ 50% off next month if you refer a friend
✓ Free access to our Advanced Reports feature
✓ Priority support upgrade

→ See details: https://app.seoanalyzerpro.com/referrals

Most people who stick with us past 30 days end up staying for years. The data gets better, your system gets more refined, and results compound.

Looking forward to seeing your wins!

Best,
{your_name}
"""
    }
}

# ============================================================================
# ONBOARDING TASK SYSTEM
# ============================================================================

ONBOARDING_TASKS = {
    
    "setup_profile": {
        "title": "Complete Your Profile",
        "description": "Add company info so we can personalize recommendations",
        "due_days": 1,
        "priority": "high"
    },
    
    "first_analysis": {
        "title": "Run Your First Keyword Analysis",
        "description": "Enter 3-5 keywords and see instant insights",
        "due_days": 1,
        "priority": "high"
    },
    
    "competitor_analysis": {
        "title": "Analyze Your Top 3 Competitors",
        "description": "Find keywords they rank for that you don't",
        "due_days": 3,
        "priority": "medium"
    },
    
    "content_generation": {
        "title": "Generate AI Content",
        "description": "Create SEO-optimized content outline",
        "due_days": 5,
        "priority": "medium"
    },
    
    "batch_upload": {
        "title": "Try Batch Analysis",
        "description": "Upload 10+ keywords at once",
        "due_days": 7,
        "priority": "low"
    }
}

# ============================================================================
# SEND EMAIL FUNCTION
# ============================================================================

def send_onboarding_email(
    to_email: str,
    template_name: str,
    customer_data: dict
):
    """Send automated onboarding email"""
    
    if template_name not in ONBOARDING_EMAILS:
        print(f"❌ Email template '{template_name}' not found")
        return False
    
    template = ONBOARDING_EMAILS[template_name]
    
    # Fill in variables
    subject = template["subject"].format(**customer_data)
    body = template["body"].format(**customer_data)
    
    try:
        # Email configuration
        sender_email = os.getenv("SENDGRID_FROM_EMAIL", "noreply@seoanalyzerpro.com")
        sender_name = "SEO Analyzer Pro"
        
        # Using SendGrid API (recommended for production)
        # pip install sendgrid
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        message = Mail(
            from_email=(sender_email, sender_name),
            to_emails=to_email,
            subject=subject,
            plain_text_content=body,
        )
        
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        
        print(f"✅ Email sent to {to_email} (template: {template_name})")
        return True
    
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

# ============================================================================
# SCHEDULE ONBOARDING SEQUENCE
# ============================================================================

def schedule_onboarding_sequence(customer_data: dict):
    """
    Schedule all onboarding emails for a new customer
    
    customer_data should include:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "plan": "professional",
        "signup_time": datetime.now(),
        "features": "5,000 keywords/month, AI content generation, etc."
    }
    """
    
    print(f"\n📧 Scheduling onboarding sequence for {customer_data['name']}...")
    
    for email_key, email_config in ONBOARDING_EMAILS.items():
        # Calculate send time
        delay = timedelta(hours=email_config["delay_hours"])
        send_time = customer_data["signup_time"] + delay
        
        # In production, you'd queue this in a job scheduler (Celery, APScheduler, etc.)
        print(f"  → {email_key}: scheduled for {send_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # For testing, send immediately
        send_onboarding_email(
            customer_data["email"],
            email_key,
            customer_data
        )
    
    print("✅ Onboarding sequence scheduled!\n")

# ============================================================================
# CREATE CUSTOMER DASHBOARD CHECKLIST
# ============================================================================

def create_onboarding_checklist(customer_id: str):
    """Generate personalized onboarding checklist"""
    
    checklist = {
        "customer_id": customer_id,
        "created_at": datetime.now().isoformat(),
        "completion_percentage": 0,
        "tasks": []
    }
    
    for task_key, task_config in ONBOARDING_TASKS.items():
        task = {
            "id": task_key,
            "title": task_config["title"],
            "description": task_config["description"],
            "due_date": (datetime.now() + timedelta(days=task_config["due_days"])).isoformat(),
            "priority": task_config["priority"],
            "completed": False,
            "completed_at": None
        }
        checklist["tasks"].append(task)
    
    return checklist

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # Example new customer
    new_customer = {
        "name": "Sarah Johnson",
        "email": "sarah@agency.com",
        "plan": "professional",
        "keyword_1": "SEO services",
        "keyword_2": "content marketing",
        "your_name": "Your Support Team",
        "features": """
✓ 5,000 keywords/month
✓ Advanced competitor analysis
✓ AI content generation
✓ Priority support
✓ API access
✓ Zapier integrations""",
        "signup_time": datetime.now()
    }
    
    # Schedule onboarding sequence
    schedule_onboarding_sequence(new_customer)
    
    # Generate checklist
    checklist = create_onboarding_checklist("customer_12345")
    
    print("📋 ONBOARDING CHECKLIST")
    print(json.dumps(checklist, indent=2, default=str))

"""
IMPLEMENTATION GUIDE:

1. Connect to Your Database
   - When a new customer signs up, call schedule_onboarding_sequence()
   - This will queue up all emails based on their signup time

2. Set Up Email Service
   - Use SendGrid (recommended): $20/month for 100K emails
   - Or use your email provider's API
   - Update SENDGRID_API_KEY in environment

3. Create Job Scheduler
   - Use Celery + Redis: Great for production
   - Or use APScheduler: Lighter weight alternative
   - Schedule emails to send at correct times

4. Display Checklist in App
   - Show onboarding_checklist.json in user dashboard
   - Mark tasks complete as users use features
   - Celebrate progress with encouraging messages

5. Track Completion
   - Monitor which tasks users complete
   - Track time to first keyword analysis
   - Track time to first content creation
   - Use this data to improve onboarding

EXPECTED OUTCOMES:
- 80% of users complete profile setup (Day 1)
- 70% run first analysis (Day 1)
- 50% analyze competitors (Day 3)
- 35% create content (Day 5)
- 20% use batch upload (Day 7)
- 90% retention after 30 days (if they complete onboarding)

OPTIMIZATION TIPS:
- Personalize with their keywords
- Celebrate small wins
- Ask for feedback
- Offer help proactively
- Remove friction (one-click features)
"""
