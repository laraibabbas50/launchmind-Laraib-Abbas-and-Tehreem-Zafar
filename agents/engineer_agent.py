"""
Engineer Agent - Creates REAL GitHub pull requests with auto-delete
"""

import os
import base64
import requests
from message_bus import message_bus

class EngineerAgent:
    def __init__(self):
        self.name = "engineer"
        self.github_token = os.environ.get("GITHUB_TOKEN")
        # CHANGE THIS to your repo
        self.repo_name = "laraibabbas50/launchmind-Laraib-Abbas-and-Tehreem-Zafar"
    
    def generate_html(self, product_spec):
        """Generate HTML landing page from product spec"""
        
        value_prop = product_spec.get("value_proposition", "Amazing Product")
        features = product_spec.get("features", [])
        
        features_html = ""
        for f in features:
            features_html += f"""
                <li>
                    <h3>{f.get('name', 'Feature')}</h3>
                    <p>{f.get('description', 'Description here')}</p>
                </li>
            """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LaunchMind - {value_prop}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 80px 20px; text-align: center; }}
        h1 {{ font-size: 48px; margin-bottom: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}
        .features {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 40px 0; }}
        .feature {{ background: #f4f4f4; padding: 20px; border-radius: 8px; }}
        .cta {{ background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
        footer {{ text-align: center; padding: 20px; background: #333; color: white; }}
    </style>
</head>
<body>
    <header>
        <h1>{value_prop}</h1>
        <p>Your solution for modern learning</p>
        <a href="#" class="cta">Get Started →</a>
    </header>
    <div class="container">
        <h2>Features</h2>
        <div class="features">
            {features_html}
        </div>
    </div>
    <footer>
        <p>Built by LaunchMind AI Agents</p>
    </footer>
</body>
</html>"""
    
    def delete_branch(self, branch_name):
        """Delete existing branch if it exists (to avoid 422 error)"""
        url = f"https://api.github.com/repos/{self.repo_name}/git/refs/heads/{branch_name}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github+json"
        }
        
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            print(f"✅ Deleted existing branch '{branch_name}'")
            return True
        elif response.status_code == 404:
            print(f"ℹ️ Branch '{branch_name}' did not exist (clean slate)")
            return True
        else:
            print(f"⚠️ Could not delete branch: {response.status_code}")
            return False
    
    def create_branch(self, branch_name):
        """Create a new branch on GitHub"""
        url = f"https://api.github.com/repos/{self.repo_name}/git/refs"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github+json"
        }
        
        # Get main branch SHA
        main_url = f"https://api.github.com/repos/{self.repo_name}/git/refs/heads/main"
        response = requests.get(main_url, headers=headers)
        
        if response.status_code != 200:
            # Try 'master' instead of 'main'
            main_url = f"https://api.github.com/repos/{self.repo_name}/git/refs/heads/master"
            response = requests.get(main_url, headers=headers)
            if response.status_code != 200:
                print(f"❌ Could not find main or master branch")
                return None
        
        main_sha = response.json()["object"]["sha"]
        
        # Create branch
        payload = {"ref": f"refs/heads/{branch_name}", "sha": main_sha}
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            print(f"✅ Branch '{branch_name}' created")
            return main_sha
        else:
            print(f"❌ Branch creation failed: {response.status_code}")
            return None
    
    def commit_file(self, branch_name, file_path, content, commit_message):
        """Commit a file to GitHub"""
        url = f"https://api.github.com/repos/{self.repo_name}/contents/{file_path}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github+json"
        }
        
        encoded_content = base64.b64encode(content.encode()).decode()
        
        payload = {
            "message": commit_message,
            "content": encoded_content,
            "branch": branch_name
        }
        
        response = requests.put(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"✅ File '{file_path}' committed")
            return True
        else:
            print(f"❌ Commit failed: {response.status_code}")
            return False
    
    def create_pull_request(self, branch_name, title, body):
        """Open a Pull Request on GitHub"""
        url = f"https://api.github.com/repos/{self.repo_name}/pulls"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github+json"
        }
        
        payload = {
            "title": title,
            "body": body,
            "head": branch_name,
            "base": "main"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            pr_url = response.json()["html_url"]
            print(f"✅ Pull Request created: {pr_url}")
            return pr_url
        else:
            # Try with 'master' as base
            payload["base"] = "master"
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                pr_url = response.json()["html_url"]
                print(f"✅ Pull Request created: {pr_url}")
                return pr_url
            
            print(f"❌ PR creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    
    def process_messages(self):
        """Check for and process incoming messages"""
        
        messages = message_bus.get_messages_for_agent(self.name)
        
        for msg in messages:
            if msg["message_type"] == "result" and msg["from_agent"] == "product":
                print(f"\n📥 ENGINEER AGENT: Received product spec")
                
                product_spec = msg["payload"]
                
                # Generate HTML
                html_content = self.generate_html(product_spec)
                
                # Create branch (delete old one first if exists)
                branch_name = "agent-landing-page"
                
                # STEP 1: Delete existing branch (to avoid 422 error)
                self.delete_branch(branch_name)
                
                # STEP 2: Create fresh branch
                sha = self.create_branch(branch_name)
                
                if sha:
                    # Commit HTML file
                    if self.commit_file(branch_name, "index.html", html_content, "Add AI-generated landing page"):
                        # Create Pull Request
                        pr_url = self.create_pull_request(
                            branch_name,
                            "Initial Landing Page - AI Generated",
                            f"""## 🤖 AI-Generated Pull Request

This PR was automatically created by the Engineer Agent.

### Product Value Proposition:
{product_spec.get('value_proposition', 'N/A')}

### Features Included:
{', '.join([f.get('name', '') for f in product_spec.get('features', [])])}

### Next Steps:
1. Review the landing page
2. Merge if approved
3. Deploy to production

---
*Generated by LaunchMind Multi-Agent System*"""
                        )
                        
                        # Send PR URL back to CEO
                        if pr_url:
                            message_bus.send_message(
                                from_agent=self.name,
                                to_agent="ceo",
                                message_type="result",
                                payload={
                                    "pr_url": pr_url,
                                    "branch": branch_name,
                                    "status": "success"
                                }
                            )
                            print(f"✅ ENGINEER AGENT: PR URL sent to CEO")
                        else:
                            # Send failure message
                            message_bus.send_message(
                                from_agent=self.name,
                                to_agent="ceo",
                                message_type="result",
                                payload={
                                    "status": "failed",
                                    "error": "Could not create PR"
                                }
                            )
                    else:
                        print(f"❌ ENGINEER AGENT: Commit failed")
                else:
                    print(f"❌ ENGINEER AGENT: Branch creation failed")
        
        message_bus.clear_queue(self.name)