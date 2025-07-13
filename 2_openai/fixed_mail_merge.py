# Fixed Mail Merge Functionality for 2_lab2.ipynb
# Copy these functions into your notebook to replace the broken ones

import json
from typing import Dict
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from agents import Agent, function_tool

# Fixed Mail Merge Function (corrected version)
@function_tool
def send_bulk_emails_fixed(template_name: str, contact_list: str, custom_subject: str = None) -> Dict[str, str]:
    """Send personalized emails to a list of contacts using a template"""
    try:
        contacts = json.loads(contact_list)
        
        # Define templates directly in the function to avoid FunctionTool issues
        templates = {
            "soc2_compliance": """Subject: Simplify Your SOC 2 Compliance Journey

Hi {name},

I hope this message finds you well. As the {role} at {company}, I'm sure you understand the importance of SOC 2 compliance and the challenges that come with audit preparation.

At ComplAI, we've developed an AI-powered SaaS solution that streamlines the entire SOC 2 compliance process. Our platform helps companies like yours:

• Automate documentation and evidence collection
• Monitor compliance in real-time
• Prepare for audits with confidence
• Reduce manual effort by up to 80%

Would you be interested in a brief 15-minute call to discuss how we can help {company} simplify its compliance workflow?

Best regards,
[Your Name]
ComplAI Team""",

            "audit_preparation": """Subject: Streamline Your SOC 2 Audit Preparation

Dear {name},

Preparing for SOC 2 audits can be overwhelming, especially when you're juggling multiple priorities as {role} at {company}. The manual processes, documentation gaps, and last-minute scrambles are all too familiar.

ComplAI's AI-powered platform transforms audit preparation from a stressful ordeal into a smooth, automated process. We help you:

• Identify compliance gaps before they become audit issues
• Automate evidence collection and documentation
• Generate audit-ready reports
• Maintain continuous compliance monitoring

I'd love to show you how we've helped similar companies reduce their audit preparation time by 60%.

Would you be available for a quick call this week?

Best regards,
[Your Name]
ComplAI Team""",

            "compliance_automation": """Subject: Automate Your Compliance Workflow

Hello {name},

Is your team spending too much time on manual compliance tasks? We've helped companies like {company} reduce compliance overhead by 80% while improving audit readiness.

As {role}, you know that compliance isn't just about checking boxes—it's about building a robust security foundation that supports your business growth.

ComplAI's platform provides:

• Automated compliance monitoring
• Real-time risk assessment
• Streamlined audit preparation
• Continuous improvement insights

Let's discuss how we can help {company} turn compliance from a burden into a competitive advantage.

Best regards,
[Your Name]
ComplAI Team"""
        }
        
        if template_name not in templates:
            return {"status": "error", "message": f"Template '{template_name}' not found"}
        
        template = templates[template_name]
        sent_count = 0
        
        for contact in contacts:
            # Personalize the template
            personalized_content = template.format(
                name=contact["name"],
                company=contact["company"],
                role=contact["role"]
            )
            
            # Extract subject from template or use custom subject
            lines = personalized_content.split('\n')
            subject = custom_subject if custom_subject else lines[0].replace("Subject: ", "")
            body = '\n'.join(lines[1:])  # Remove subject line from body
            
            # Send the email
            sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email("kyra.nankivell@gmail.com")
            to_email = To(contact["email"])
            content = Content("text/plain", body)
            mail = Mail(from_email, to_email, subject, content).get()
            response = sg.send(mail)
            sent_count += 1
        
        return {"status": "success", "message": f"Sent {sent_count} personalized emails"}
        
    except Exception as e:
        return {"status": "error", "message": f"Error sending bulk emails: {str(e)}"}

# Contact List Management (unchanged)
@function_tool
def get_contact_list() -> Dict[str, str]:
    """Get the current contact list for mail merge"""
    sample_contacts = [
        {"name": "John Smith", "email": "john.smith@techcorp.com", "company": "TechCorp", "role": "CTO"},
        {"name": "Sarah Johnson", "email": "sarah.j@startupinc.com", "company": "StartupInc", "role": "CEO"},
        {"name": "Mike Chen", "email": "mchen@enterprise.com", "company": "Enterprise Solutions", "role": "VP Engineering"}
    ]
    return {"status": "success", "contacts": json.dumps(sample_contacts)}

# Updated Mail Merge Agent with fixed function
def create_fixed_mail_merge_agent():
    """Create a mail merge agent with the fixed function"""
    return Agent(
        name="Mail Merge Specialist (Fixed)",
        instructions="""You are a mail merge specialist for ComplAI. You help send personalized email campaigns.
You can:
1. Get contact lists
2. Send personalized bulk emails using templates

Available templates: soc2_compliance, audit_preparation, compliance_automation

Keep your responses focused and efficient.""",
        tools=[get_contact_list, send_bulk_emails_fixed],
        model="gpt-4o-mini"
    )

# Enhanced Sales Manager with fixed mail merge
def create_enhanced_sales_manager_fixed(original_tools, original_handoffs):
    """Create enhanced sales manager with fixed mail merge capabilities"""
    enhanced_tools = [
        *original_tools,  # Original sales agent tools and email tools
        get_contact_list, send_bulk_emails_fixed  # Fixed mail merge tools
    ]
    
    return Agent(
        name="Enhanced Sales Manager (Fixed)",
        instructions="""You are an enhanced sales manager for ComplAI. You can:
1. Use the original sales agent tools to generate cold emails
2. Use mail merge tools to send personalized campaigns

Available templates: soc2_compliance, audit_preparation, compliance_automation

Keep your workflow simple and focused.""",
        tools=enhanced_tools,
        handoffs=original_handoffs,
        model="gpt-4o-mini"
    )

# Example usage functions
def test_mail_merge():
    """Test the fixed mail merge functionality"""
    agent = create_fixed_mail_merge_agent()
    message = "Send a SOC2 compliance email campaign to the contact list"
    
    from agents import Runner, trace
    import asyncio
    
    async def run_test():
        with trace("Fixed Mail Merge Test"):
            result = await Runner.run(agent, message)
            print(result)
    
    return asyncio.run(run_test())

def test_enhanced_sales_manager(original_tools, original_handoffs):
    """Test the enhanced sales manager with fixed mail merge"""
    agent = create_enhanced_sales_manager_fixed(original_tools, original_handoffs)
    message = "Generate a cold email and send it to the contact list using the SOC2 compliance template"
    
    from agents import Runner, trace
    import asyncio
    
    async def run_test():
        with trace("Enhanced Sales Manager Test (Fixed)"):
            result = await Runner.run(agent, message, max_turns=15)
            print(result)
    
    return asyncio.run(run_test()) 