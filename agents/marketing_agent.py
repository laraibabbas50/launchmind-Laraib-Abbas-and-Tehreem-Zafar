import os
import requests
from message_bus import message_bus

class MarketingAgent:
    def __init__(self):
        self.name = "marketing"
        self.sendgrid_key = os.environ.get("SENDGRID_API_KEY")
        self.slack_token = os.environ.get("SLACK_BOT_TOKEN")
    
    def generate_mock_copy(self, spec):
        return {
            "tagline": "Learn Smarter, Not Harder",
            "description": "Connect with expert tutors in minutes.",
            "email_subject": "Revolutionizing education",
            "email_body": "Dear User,\n\nTry our platform today!\n\nBest,\nLaunchMind",
            "twitter": "🚀 Launching soon! #EdTech",
            "linkedin": "Building the future of education"
        }
    
    def send_email(self, to_email, subject, body):
        if not self.sendgrid_key:
            print("⚠️ No SendGrid key - email not sent")
            return False
        
        data = {
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": "laraibabbas50@gmail.com"},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}]
        }
        headers = {"Authorization": f"Bearer {self.sendgrid_key}", "Content-Type": "application/json"}
        
        r = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)
        if r.status_code == 202:
            print(f"✅ Email sent to {to_email}")
            return True
        print(f"❌ Email failed: {r.status_code}")
        return False
    
    def post_to_slack(self, tagline, description, pr_url):
        if not self.slack_token:
            print("⚠️ No Slack token - message not posted")
            return False
        
        payload = {
            "channel": "#launches",
            "blocks": [
                {"type": "header", "text": {"type": "plain_text", "text": f"🚀 {tagline}"}},
                {"type": "section", "text": {"type": "mrkdwn", "text": description}},
                {"type": "section", "fields": [{"type": "mrkdwn", "text": f"<{pr_url}|View PR>"}]}
            ]
        }
        headers = {"Authorization": f"Bearer {self.slack_token}", "Content-Type": "application/json"}
        
        r = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
        if r.status_code == 200 and r.json().get("ok"):
            print(f"✅ Slack message posted")
            return True
        print(f"❌ Slack failed: {r.json().get('error')}")
        return False
    
    def process_messages(self):
        print(f"\n🔍 MARKETING AGENT: Checking for messages...")
        messages = message_bus.get_messages_for_agent(self.name)
        for msg in messages:
            if msg["message_type"] == "result" and msg["from_agent"] == "product":
                print(f"\n📥 MARKETING AGENT: Received spec")
                copy = self.generate_mock_copy(msg["payload"])
                
                # For now, get the latest PR from GitHub directly
                # Or wait for CEO to send PR URL
                pr_url = "https://github.com/laraibabbas50/launchmind-Laraib-Abbas-and-Tehreem-Zafar/pull"
                
                self.send_email("i248060@isb.nu.edu.pk", copy["email_subject"], copy["email_body"])
                self.post_to_slack(copy["tagline"], copy["description"], pr_url)
                
                message_bus.send_message(self.name, "ceo", "confirmation", {"status": "marketing_done"})
        message_bus.clear_queue(self.name)