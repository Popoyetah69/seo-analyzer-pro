#!/usr/bin/env python3
"""
Cold Email Automation Script
Sends personalized cold emails in batches with follow-up sequences
"""

import json
import csv
import time
from datetime import datetime, timedelta
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict

class ColdEmailCampaign:
    def __init__(self, smtp_server: str, email_from: str, password: str):
        self.smtp_server = smtp_server
        self.email_from = email_from
        self.password = password
        self.campaign_log = []
        self.load_campaign_data()
    
    def load_campaign_data(self):
        """Load campaign templates and tracking data"""
        self.templates = {
            "agency": {
                "subject": "92% cheaper than Semrush (no BS)",
                "body": """Hi {name},

I saw your blog post on "{topic}" – solid insights.

Quick question: Are you (or your team) using Semrush?

If yes, you're probably spending $300-1,000/month on features you never use.

I built SEO Analyzer Pro specifically for this. Same features. 92% cheaper.

Your team keeps using the same tools. Your costs drop 90%.

I'm offering 50 agencies a 50% discount for their first 3 months. Not a pitch – just wanted you to see the numbers.

If curious, reply to this email. If not, no worries.

Best,
{sender_name}

P.S. – Your blog mentions "{insight}". I'd love to get your thoughts on how AI content generation is changing the game. Lmk."""
            },
            "freelancer": {
                "subject": "Stealing this from Semrush",
                "body": """Hi {name},

I stalked your website and saw you're an SEO freelancer. Good taste.

I was too, until I built SEO Analyzer Pro. Now I spend $15/month instead of $120 and my margins are insane.

Thought you might care.

The deal:
- Everything Semrush does
- 1/10th the price
- Full API (this is the magic)

I'm giving away 50 free Professional accounts for the first month. No catch. Just want to see if freelancers like it.

Want in?

https://analyzerseo.store

Cheers,
{sender_name}

P.S. – If you build client dashboards, the API access is game-changing. Built my first one in 2 hours."""
            },
            "ecommerce": {
                "subject": "Cut your SEO tool costs by 90% (literally)",
                "body": """Hey {name},

Your {product} ranks for {keyword}. Great work.

I'm guessing you're tracking that via Semrush ($120/month or more).

What if I told you there's a tool that does the same thing for $15/month?

I'm not exaggerating. Full keyword research, rank tracking, content generation. Everything.

The catch? You have to be willing to move off Semrush.

But here's the upside:
- $105/month saved
- Same (or better) data
- Full API if you want to build custom dashboards

I'm running a beta. 50 spots. First month free to prove it works.

Want to see it?

https://analyzerseo.store

–{sender_name}

P.S. – The savings alone could cover your monthly SEO budget. Just saying."""
            }
        }
    
    def send_email(self, to_email: str, subject: str, body: str, template_type: str = None) -> bool:
        """Send single email"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.email_from
            msg["To"] = to_email
            
            text_part = MIMEText(body, "plain")
            msg.attach(text_part)
            
            with smtplib.SMTP_SSL(self.smtp_server, 465) as server:
                server.login(self.email_from, self.password)
                server.sendmail(self.email_from, to_email, msg.as_string())
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "recipient": to_email,
                "subject": subject,
                "template": template_type,
                "status": "sent",
                "retry_count": 0
            }
            self.campaign_log.append(log_entry)
            return True
        except Exception as e:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "recipient": to_email,
                "subject": subject,
                "template": template_type,
                "status": "failed",
                "error": str(e),
                "retry_count": 0
            }
            self.campaign_log.append(log_entry)
            return False
    
    def personalize_template(self, template_type: str, data: Dict) -> tuple:
        """Personalize email template with recipient data"""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        template = self.templates[template_type]
        subject = template["subject"].format(**data)
        body = template["body"].format(**data)
        
        return subject, body
    
    def send_batch(self, contacts: List[Dict], template_type: str, delay: int = 5):
        """Send batch of emails with delay between each"""
        sent_count = 0
        failed_count = 0
        
        for i, contact in enumerate(contacts, 1):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending {i}/{len(contacts)} to {contact['email']}...")
            
            try:
                subject, body = self.personalize_template(template_type, contact)
                if self.send_email(contact['email'], subject, body, template_type):
                    sent_count += 1
                    print(f"  ✓ Sent successfully")
                else:
                    failed_count += 1
                    print(f"  ✗ Failed to send")
                
                if i < len(contacts):
                    time.sleep(delay)
            except Exception as e:
                failed_count += 1
                print(f"  ✗ Error: {e}")
        
        print(f"\nBatch complete: {sent_count} sent, {failed_count} failed")
        return sent_count, failed_count
    
    def save_campaign_log(self, filename: str = "campaign_log.json"):
        """Save campaign log to file"""
        with open(filename, 'w') as f:
            json.dump(self.campaign_log, f, indent=2)
        print(f"Campaign log saved to {filename}")
    
    def send_followup(self, opened_but_no_reply: List[Dict], delay: int = 5):
        """Send follow-up email to contacts with no reply after 5 days"""
        followup_template = """Hi {name},

Just following up on my previous email about SEO Analyzer Pro.

I know you're busy, but wanted to make sure it didn't get buried.

Quick recap:
- Same as Semrush
- 92% cheaper ($15/mo instead of $120)
- Full API access

No pressure – just wanted to make sure you saw it.

Link: https://analyzerseo.store

Best,
{sender_name}

P.S. – If you replied and I missed it, my apologies! Let me know your thoughts."""
        
        sent_count = 0
        for i, contact in enumerate(opened_but_no_reply, 1):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending follow-up {i}/{len(opened_but_no_reply)} to {contact['email']}...")
            
            try:
                subject = f"Quick follow-up: SEO Analyzer Pro"
                body = followup_template.format(
                    name=contact.get('name', 'there'),
                    sender_name=contact.get('sender_name', 'Team')
                )
                
                if self.send_email(contact['email'], subject, body, "followup"):
                    sent_count += 1
                    print(f"  ✓ Follow-up sent")
                
                if i < len(opened_but_no_reply):
                    time.sleep(delay)
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        print(f"Follow-up complete: {sent_count} sent")
        return sent_count


def main():
    """Main execution"""
    print("""
╔════════════════════════════════════════════════════════════╗
║          COLD EMAIL AUTOMATION - SEO Analyzer Pro          ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Configuration
    SMTP_SERVER = "smtp.gmail.com"  # Change to your provider
    EMAIL_FROM = input("Enter your email: ")
    PASSWORD = input("Enter your email password (or app password): ")
    SENDER_NAME = input("Enter sender name: ")
    
    # Initialize campaign
    campaign = ColdEmailCampaign(SMTP_SERVER, EMAIL_FROM, PASSWORD)
    
    # Example: Send batch to agencies
    agencies = [
        {
            "name": "Alice Johnson",
            "email": "alice@seoagency.com",
            "topic": "10 SEO trends 2026",
            "insight": "Schema markup",
            "sender_name": SENDER_NAME
        },
        # Add more contacts from CSV...
    ]
    
    print(f"\n📧 Sending to {len(agencies)} agencies...")
    sent, failed = campaign.send_batch(agencies, template_type="agency", delay=10)
    
    # Save log
    campaign.save_campaign_log("campaign_log.json")
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║                      CAMPAIGN SUMMARY                      ║
╠════════════════════════════════════════════════════════════╣
║ Sent:      {sent}
║ Failed:    {failed}
║ Total:     {sent + failed}
║ Success:   {(sent/(sent+failed)*100):.1f}% if sent+failed > 0 else 0
╚════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
