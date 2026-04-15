"""
seed_scenarios.py - Database seeding script for educational scenarios.

Populates the scenarios table with a set of labelled phishing and legitimate
email examples spanning beginner, intermediate, and advanced difficulty levels.

Run this script once after initialising the database:
    python seed_scenarios.py

It is idempotent - running it multiple times will not create duplicate
scenarios (it checks for existing data before inserting).
"""

import os
import sys
import json

# Ensure backend/ root is on the path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db
from app.models.progress import Scenario

SCENARIOS = [
    # ── BEGINNER (6 scenarios) ──────────────────────────────────────────
    {
        "title": "Nigerian Prince Lottery Win",
        "difficulty": "Beginner",
        "is_phishing": True,
        "email_content": """From: prince.ibrahim@yahoo.com
To: victim@example.com
Subject: URGENT: You Have Won $5,000,000 USD - Claim Now!

Dear Friend,

I am Prince Ibrahim Al-Hassan, son of the late King of Nigeria. I am writing
to inform you that you have been selected as the beneficiary of FIVE MILLION
US DOLLARS from my late father's estate.

To claim your inheritance, please send your:
- Full name
- Bank account number
- A processing fee of $500 USD

Act immediately! This offer expires in 48 HOURS.

God bless you,
Prince Ibrahim Al-Hassan
Royal Palace of Lagos
""",
        "indicators": json.dumps([
            "Advance fee fraud - asking for $500 processing fee",
            "Unrealistic prize claim from a stranger",
            "Free email address (yahoo.com) for supposed royalty",
            "Urgency language: 'expires in 48 HOURS'",
            "Requests sensitive bank account information",
        ]),
        "explanation": (
            "This is a classic advance fee fraud (419 scam). Legitimate prize "
            "notifications never ask for upfront fees, and no real prince would "
            "contact you via Yahoo Mail. The urgency ('expires in 48 HOURS') is "
            "designed to prevent you from thinking critically."
        ),
        "learning_points": json.dumps([
            "Legitimate prizes never require upfront payment fees.",
            "Real organisations don't use free email addresses (yahoo.com, gmail.com).",
            "Artificial urgency is a classic phishing tactic.",
            "Never share bank account details via email with unknown parties.",
        ]),
    },
    {
        "title": "Prize Notification",
        "difficulty": "Beginner",
        "is_phishing": True,
        "email_content": """From: prizes@mega-lottery-winners.tk
To: you@example.com
Subject: CONGRATULATIONS! You've Won an iPhone 15 Pro!

Dear Lucky Winner,

CONGRATULATIONS! Your email address was randomly selected in our
Monthly Mega Prize Draw. You have WON an Apple iPhone 15 Pro (worth $1,299)!

To claim your FREE prize, click the link below and fill in your details:
http://mega-lottery-winners.tk/claim?ref=WIN2024

Offer valid for 24 hours only. Act now or lose your prize!

The Mega Lottery Team
""",
        "indicators": json.dumps([
            "Suspicious .tk domain (free, commonly used for phishing)",
            "You didn't enter any lottery - unsolicited prize notification",
            "Urgency: '24 hours only'",
            "Requests personal details on an untrusted site",
            "Generic greeting: 'Dear Lucky Winner'",
        ]),
        "explanation": (
            "This is a classic phishing lure. The .tk top-level domain is free "
            "and heavily associated with phishing. You cannot win a lottery you "
            "didn't enter. The 24-hour deadline is designed to pressure you into "
            "handing over personal data without checking if this is legitimate."
        ),
        "learning_points": json.dumps([
            "You cannot win competitions you never entered.",
            "Free TLDs (.tk, .ml, .ga) are major phishing red flags.",
            "Hover over links to check the true URL before clicking.",
            "Legitimate companies do not pressure you with 24-hour countdown deadlines.",
        ]),
    },
    {
        "title": "PayPal Account Locked - Verify Now",
        "difficulty": "Beginner",
        "is_phishing": True,
        "email_content": """From: security@paypa1-support.com
To: customer@example.com
Subject: Your PayPal Account Has Been LOCKED

Dear PayPal Customer,

We have detected unusual activity on your PayPal account. For your security,
your account has been temporarily locked.

To restore access, you must verify your identity within 24 hours:

CLICK HERE TO VERIFY: http://paypa1-support.com/verify/login

You will need to confirm:
- Your full name
- Password
- Credit card number and CVV
- Social Security Number

Failure to verify will result in permanent account suspension.

PayPal Security Team
""",
        "indicators": json.dumps([
            "Lookalike domain: 'paypa1-support.com' (1 replacing l)",
            "Requests extremely sensitive data: password, SSN, CVV",
            "Threat language: 'permanent account suspension'",
            "Generic greeting: 'Dear PayPal Customer'",
            "Urgency: '24 hours'",
        ]),
        "explanation": (
            "PayPal would NEVER ask for your password, credit card CVV, or "
            "Social Security Number via email. The sender domain 'paypa1-support.com' "
            "uses a '1' to impersonate 'paypal' - this is called typosquatting. "
            "The threat of permanent suspension is designed to panic you into complying."
        ),
        "learning_points": json.dumps([
            "Legitimate services NEVER ask for passwords via email.",
            "Check URLs carefully - '1' replacing 'l' is a typosquatting technique.",
            "If unsure, log in directly at paypal.com - never via email links.",
            "No legitimate company needs your Social Security Number for account verification.",
        ]),
    },
    {
        "title": "Amazon Security Alert",
        "difficulty": "Beginner",
        "is_phishing": True,
        "email_content": """From: no-reply@amaz0n-security.com
To: shopper@example.com
Subject: [Action Required] Your Amazon account has been compromised

Hello Amazon Customer,

Our security systems have detected that your Amazon account was accessed from
an unknown device in Russia.

IMMEDIATE ACTION REQUIRED:
→ Click to secure your account: http://amaz0n-security.com/protect

You have 2 hours to act before your account is permanently deleted.

Amazon Security Centre
""",
        "indicators": json.dumps([
            "Spoofed domain: 'amaz0n-security.com' (0 replacing o)",
            "Threat of account deletion within 2 hours",
            "Generic greeting: 'Hello Amazon Customer'",
            "Suspicious redirect domain matching sender",
            "High urgency with specific fake time limit",
        ]),
        "explanation": (
            "This email impersonates Amazon using 'amaz0n' (with a zero) instead "
            "of 'amazon'. Amazon sends genuine alerts from @amazon.com - not "
            "third-party security domains. Amazon would also never threaten to "
            "delete your account within 2 hours."
        ),
        "learning_points": json.dumps([
            "Always check the sender's full email address domain.",
            "Legitimate Amazon emails come from @amazon.com only.",
            "Character substitution (0 for o, 1 for l) is a common spoofing technique.",
            "Go directly to amazon.com to check account security - never follow email links.",
        ]),
    },
    {
        "title": "GitHub Password Reset",
        "difficulty": "Beginner",
        "is_phishing": False,
        "email_content": """From: noreply@github.com
To: developer@example.com
Subject: [GitHub] Please reset your password

Hey developer,

We received a request to reset the password for your GitHub account.

Click the button below to create a new password:
https://github.com/password_reset?token=abc123xyz&expires=1h

This link will expire in 1 hour. If you didn't request a password reset,
you can safely ignore this email - your password will not be changed.

Thanks,
The GitHub Team

GitHub, Inc.
88 Colin P Kelly Jr St, San Francisco, CA 94107
""",
        "indicators": json.dumps([]),
        "explanation": (
            "This is a legitimate GitHub password reset email. Key indicators of "
            "legitimacy: the sender domain is @github.com (not a lookalike), the "
            "link goes to github.com (not a third-party site), it uses your actual "
            "username (not 'Dear Customer'), and it reassures you that ignoring the "
            "email is safe if you didn't request a reset."
        ),
        "learning_points": json.dumps([
            "Legitimate password reset emails use the company's real domain (@github.com).",
            "Real emails personalise with your actual username, not generic titles.",
            "Legitimate password resets link directly to the company's own website.",
            "A reassurance that ignoring the email is safe is a sign of legitimacy.",
        ]),
    },
    {
        "title": "IT Helpdesk Password Expiry",
        "difficulty": "Beginner",
        "is_phishing": True,
        "email_content": """From: helpdesk@it-support-helpdesk.com
To: employee@company.com
Subject: ACTION REQUIRED: Your email password expires TODAY

Dear User,

Your email account password will expire TODAY at 5:00 PM.

To avoid losing access to your email, click the link below to renew your password:
http://it-support-helpdesk.com/renew-password

Enter your current password to proceed with renewal.

IT Helpdesk Support
""",
        "indicators": json.dumps([
            "Third-party domain 'it-support-helpdesk.com' - not internal company domain",
            "Asks for current password (legitimate systems never do this)",
            "Urgency: 'expires TODAY at 5:00 PM'",
            "Generic greeting: 'Dear User'",
        ]),
        "explanation": (
            "A real IT helpdesk email would come from your company's own domain, "
            "not a generic third-party site. Password reset systems never ask for "
            "your CURRENT password - they let you create a new one. This is designed "
            "to steal your existing credentials."
        ),
        "learning_points": json.dumps([
            "Internal IT emails always come from your company's own email domain.",
            "Legitimate password change systems never ask for your current password.",
            "Contact your IT department directly if you receive suspicious helpdesk emails.",
        ]),
    },

    # ── INTERMEDIATE (5 scenarios) ──────────────────────────────────────
    {
        "title": "Order Confirmation",
        "difficulty": "Intermediate",
        "is_phishing": True,
        "email_content": """From: orders@amazon.com.order-confirm.net
To: customer@example.com
Subject: Your Amazon order #302-8473921-1029485 has shipped

Hello,

Your Amazon order has been shipped and is on its way!

Order #302-8473921-1029485
Item: Sony WH-1000XM5 Headphones
Estimated delivery: Thursday 27 February

Track your package: http://amazon.com.order-confirm.net/track?id=302-8473921-1029485

If you did not place this order, click here to cancel and get a refund:
http://amazon.com.order-confirm.net/cancel-order

Thank you for shopping with Amazon.
""",
        "indicators": json.dumps([
            "The From domain is 'amazon.com.order-confirm.net' - the real domain is 'order-confirm.net', not amazon.com",
            "All links go to order-confirm.net, not amazon.com",
            "Clone of a genuine Amazon shipping notification format",
            "Cancel/refund link designed to capture credentials",
        ]),
        "explanation": (
            "This is a clone phishing attack - it copies the style and format of a "
            "real Amazon shipping email. The critical giveaway is the sender domain: "
            "'amazon.com.order-confirm.net'. The real domain (after the last dot before "
            "the TLD) is 'order-confirm.net'. The 'amazon.com' part is just a subdomain "
            "prefix designed to look legitimate at a glance."
        ),
        "learning_points": json.dumps([
            "Read the sender domain from right to left: TLD → main domain → subdomains.",
            "'amazon.com.evil.net' is owned by evil.net, not amazon.com.",
            "Check every link by hovering - they should all go to amazon.com.",
            "If unexpected, verify orders directly at amazon.com - don't click email links.",
        ]),
    },
    {
        "title": "Finance Department Invoice",
        "difficulty": "Intermediate",
        "is_phishing": True,
        "email_content": """From: accounts@fast-invoice-solutions.com
To: finance@targetcompany.com
Subject: Invoice #INV-2024-0847 - Payment Due

Dear Finance Team,

Please find attached invoice #INV-2024-0847 for professional services
rendered in January 2024, totalling £4,750.00.

Payment is due within 7 days. Please use the updated bank details below:

Account Name:   Fast Business Solutions Ltd
Sort Code:      20-45-81
Account Number: 83927461

If you have any queries, contact billing@fast-invoice-solutions.com.

Kind regards,
David Harris
Accounts Manager
Fast Business Solutions Ltd
""",
        "indicators": json.dumps([
            "Unsolicited invoice - recipient may not recognise this vendor",
            "Requests transfer to a new/updated bank account (classic BEC tactic)",
            "Third-party invoicing domain, not a recognisable supplier",
            "Pressure: payment due in 7 days",
        ]),
        "explanation": (
            "Business Email Compromise (BEC) fraud often involves fake invoices with "
            "'updated' bank details. Always verify bank detail changes via a phone call "
            "to a known number - NEVER rely solely on an email. Finance teams should "
            "have a standing process to verify any new or changed payment details."
        ),
        "learning_points": json.dumps([
            "Always verify changed bank details via a known phone number - not email.",
            "Implement a 4-eyes (dual authorisation) policy for outgoing payments.",
            "Be suspicious of unsolicited invoices from unrecognised vendors.",
            "BEC attacks often involve very professional-looking emails - formatting is not proof of legitimacy.",
        ]),
    },
    {
        "title": "IT Department VPN Credentials",
        "difficulty": "Intermediate",
        "is_phishing": True,
        "email_content": """From: it-helpdesk@company-it-support.com
To: staff@targetcompany.com
Subject: Mandatory VPN System Update - Action Required by Friday

Hello,

As part of our ongoing infrastructure upgrade, all staff must re-authenticate
their VPN access credentials by this Friday.

Please log in to the new VPN portal to complete the update:
https://vpn-portal.company-it-support.com/login

Use your existing Active Directory username and password.

Failure to complete this by Friday will result in loss of remote access.

IT Infrastructure Team
Target Company
""",
        "indicators": json.dumps([
            "Sender domain 'company-it-support.com' is a third-party domain, not internal",
            "VPN portal on 'company-it-support.com' - not the company's own domain",
            "Asks for Active Directory (network) credentials",
            "Deadline threat: 'loss of remote access by Friday'",
        ]),
        "explanation": (
            "Real IT teams send emails from the company's own email domain and host "
            "portals on company-owned subdomains. This email asks you to enter your "
            "Active Directory credentials on a third-party site, giving attackers full "
            "network access. Always verify IT communications via Slack, Teams, or a "
            "direct call to IT."
        ),
        "learning_points": json.dumps([
            "Company IT emails always come from your company's own domain.",
            "Verify unexpected IT requests through a secondary channel (Teams, phone).",
            "Your Active Directory password should NEVER be entered on third-party websites.",
            "Legitimate VPN portals are hosted on company-owned subdomains.",
        ]),
    },
    {
        "title": "Dropbox Link",
        "difficulty": "Intermediate",
        "is_phishing": True,
        "email_content": """From: sharing@dropbox-notify.com
To: colleague@example.com
Subject: John Smith has shared a file with you

Hi,

John Smith has shared a document with you on Dropbox:

"Q4 Financial Report - CONFIDENTIAL.pdf"

Click to view: https://bit.ly/3xPhish9

This link will expire in 48 hours.

The Dropbox Team
""",
        "indicators": json.dumps([
            "Sender domain 'dropbox-notify.com' is not the real dropbox.com",
            "URL shortener (bit.ly) hides the true destination",
            "Creates urgency: 'expires in 48 hours'",
            "Shared file name invokes curiosity (financial report, confidential)",
        ]),
        "explanation": (
            "Legitimate Dropbox sharing links go directly to dropbox.com - they are "
            "never hidden behind URL shorteners. The sender domain 'dropbox-notify.com' "
            "is not affiliated with Dropbox. The bit.ly link could redirect anywhere, "
            "including a credential-harvesting login page."
        ),
        "learning_points": json.dumps([
            "Expand URL shorteners before clicking - use a tool like checkshorturl.com.",
            "Legitimate Dropbox links always go to dropbox.com or dl.dropboxusercontent.com.",
            "Be suspicious of shared file notifications from senders you don't recognise.",
            "Hover over links to check the real URL before clicking.",
        ]),
    },
    {
        "title": "Monthly Bank Statement",
        "difficulty": "Intermediate",
        "is_phishing": False,
        "email_content": """From: statements@notifications.barclays.co.uk
To: account.holder@example.com
Subject: Your Barclays statement is ready - February 2024

Dear Mr Smith,

Your February 2024 statement is now available to view online.

Log in to Online Banking to view your statement:
https://www.barclays.co.uk/online-banking/

For security, we have not attached your statement to this email.

Account ending: 4729
Statement period: 1 Feb 2024 – 29 Feb 2024

If you have any concerns about your account, please call us on
0800 400 100 (24/7).

Barclays Bank PLC
Registered in England. Registered No: 1026167
""",
        "indicators": json.dumps([]),
        "explanation": (
            "This is a legitimate bank statement notification. Key legitimacy signals: "
            "the sender uses the bank's real domain (@notifications.barclays.co.uk), "
            "it uses your real name (not 'Dear Customer'), it links only to barclays.co.uk, "
            "it explicitly does NOT attach the statement (good security practice), "
            "and it provides an official phone number."
        ),
        "learning_points": json.dumps([
            "Legitimate bank emails use the bank's verified domain.",
            "Good security practice: banks send statements online, not as email attachments.",
            "Personalisation with your real name is a positive legitimacy signal.",
            "An official phone number provides a verified alternative contact method.",
        ]),
    },

    # ── ADVANCED (5 scenarios) ──────────────────────────────────────────
    {
        "title": "HR Budget Approval Request",
        "difficulty": "Advanced",
        "is_phishing": True,
        "email_content": """From: c.morrison@targetcompany-hq.com
To: finance.manager@targetcompany.com
Subject: Re: Q3 Budget Review - Urgent Approval Needed

Hi Sarah,

Following on from our discussion at Monday's leadership meeting, I need you
to urgently approve a wire transfer for the Q3 contractor invoices before
the banking deadline at 3pm today.

Total amount: £87,500
Please transfer to: Account 73829401, Sort Code 40-28-19

I'm in back-to-back meetings until 4pm - please action this before
the banking cut-off. I'll confirm via phone once I'm free.

Thanks,
Caroline Morrison
Chief Financial Officer
Target Company
""",
        "indicators": json.dumps([
            "Sender domain 'targetcompany-hq.com' is slightly different from 'targetcompany.com' - a lookalike domain",
            "Requests an urgent wire transfer via email (never appropriate)",
            "Pressure: 'banking deadline at 3pm today'",
            "Uses CFO's real name and plausible context (leadership meeting, Q3 budget)",
            "Unavailability excuse: 'in back-to-back meetings until 4pm'",
        ]),
        "explanation": (
            "This is a sophisticated spear phishing attack using several advanced tactics: "
            "it references real people (CFO Caroline Morrison), real organisational context "
            "(Q3 budget review, leadership meetings), and creates a believable time pressure. "
            "The domain 'targetcompany-hq.com' differs from the real domain by adding '-hq'. "
            "The CFO's unavailability prevents a quick phone verification - always verify "
            "wire transfers via a second channel regardless of urgency."
        ),
        "learning_points": json.dumps([
            "Always verify wire transfer requests via a known phone number - regardless of apparent seniority.",
            "Spear phishing uses research about real people and internal context to appear legitimate.",
            "A claim of unavailability is a manipulation tactic to prevent verification.",
            "Hover over the sender's email to see the full domain - '-hq' suffix is a red flag.",
            "Your company should have a policy: no wire transfers approved by email alone.",
        ]),
    },
    {
        "title": "CEO Email",
        "difficulty": "Advanced",
        "is_phishing": True,
        "email_content": """From: james.thornton@targetcorp-executive.com
To: payroll@targetcorp.com
Subject: Confidential - Payroll Adjustment Required

Hi,

I need you to make an urgent and confidential payroll adjustment before
end of day. This relates to a sensitive acquisition matter that cannot
be discussed internally at this stage.

Please update the following employee's bank details immediately:
Employee ID: E-4829
New Account: 92847361
New Sort Code: 30-44-92

This is extremely time-sensitive and must be handled discreetly. Please
do not mention this to anyone - including HR - until I give further instruction.

James Thornton
CEO, TargetCorp
""",
        "indicators": json.dumps([
            "Sender domain 'targetcorp-executive.com' differs from the real company domain",
            "Requests secrecy - 'do not mention this to anyone including HR'",
            "Urgency: 'before end of day'",
            "Requests bank detail changes for 'confidential' reasons",
            "Impersonates the CEO with a plausible-sounding acquisition storyline",
        ]),
        "explanation": (
            "This is a CEO fraud (whaling) attack - targeting payroll staff by impersonating "
            "senior executives. The request for secrecy is the most alarming indicator: "
            "legitimate businesses never ask employees to bypass normal HR and finance controls. "
            "The urgency and 'acquisition' context are designed to make the request seem urgent "
            "and legitimate. Always escalate unusual payroll changes through official channels."
        ),
        "learning_points": json.dumps([
            "Any request to keep financial actions secret from HR or finance is a major red flag.",
            "Payroll changes should always go through established HR processes - not direct CEO emails.",
            "Verify requests from executives via the company switchboard or in person.",
            "Whaling attacks research the real CEO's name, title, and business context.",
        ]),
    },
    {
        "title": "PayPal.com Credential Verification",
        "difficulty": "Advanced",
        "is_phishing": True,
        "email_content": """From: service@paypal.com
To: paypal.user@example.com
Subject: Action Required: Complete your security verification

Dear John,

We recently updated our security systems and require all users to complete
a one-time identity verification to maintain full account access.

This is required due to a compliance update under PSD2 (Payment Services
Directive 2) regulations, which all European payment providers must implement.

To complete verification:
https://www.paypa1.com/verify/identity?customer=JohnSmith&token=PSD2-2024

Verification takes less than 2 minutes. Failure to complete by 5 March 2024
may result in sending and receiving restrictions on your account.

PayPal Customer Services
""",
        "indicators": json.dumps([
            "Link goes to 'paypa1.com' - '1' replacing 'l' (typosquatting)",
            "The FROM address shows paypal.com but the link goes elsewhere - possible header spoofing",
            "References a real regulation (PSD2) to add false legitimacy",
            "Personalised with real name - spear phishing element",
            "Deadline: '5 March 2024' creates urgency",
        ]),
        "explanation": (
            "This is an advanced phishing attack that correctly uses your real name and "
            "references actual EU payment regulations (PSD2) to seem legitimate. The "
            "critical flaw is the link: 'paypa1.com' with a '1' instead of 'l'. The "
            "From header can be forged - the actual indicator to check is where the "
            "link goes. PayPal would only ever link to paypal.com."
        ),
        "learning_points": json.dumps([
            "Your real name in a phishing email does NOT make it legitimate.",
            "Hover over links and read carefully - '1' vs 'l' and '0' vs 'o' are common substitutions.",
            "Real regulatory compliance emails never require you to click email links.",
            "Go to paypal.com directly in your browser to check for any real notifications.",
            "Email From headers can be forged - the link URL is more reliable.",
        ]),
    },
    {
        "title": "Simple Email",
        "difficulty": "Advanced",
        "is_phishing": True,
        "email_content": """From: david.chen@supplier-co.net
To: procurement@targetcompany.com
Subject: Re: Re: Re: Purchase Order PO-2024-0483 - Delivery Confirmation

Hi Rachel,

Thanks for the confirmation. As discussed, we've updated our banking details
as of 1st February - please ensure future payments use the new account below:

Account Name:  Supplier Co Ltd
Bank:          HSBC
Sort Code:     30-20-19
Account Number: 82736450

I've attached the updated invoicing instructions document for your records.

Best,
David Chen
Accounts Department
Supplier Co Ltd
Tel: +44 20 7946 0823

--- Original Message ---
From: rachel.jones@targetcompany.com
Sent: Monday, 19 February 2024 14:32
To: david.chen@supplier-co.net
Subject: Re: Re: Purchase Order PO-2024-0483 - Delivery Confirmation
...
""",
        "indicators": json.dumps([
            "Injected into a real email thread to appear credible",
            "Requests bank account change buried in an ongoing thread",
            "The supplier domain 'supplier-co.net' should be cross-checked against known supplier records",
            "Attachment claiming to contain invoicing instructions (potential malware)",
        ]),
        "explanation": (
            "Reply chain injection is one of the most sophisticated phishing attacks. "
            "The attacker compromises a real email account (or spoofs one) and injects "
            "messages into ongoing business threads. The context feels completely real because "
            "it IS part of a real conversation. The tell is the bank detail change request - "
            "always verify via phone using a number from your own records, not the email."
        ),
        "learning_points": json.dumps([
            "Being part of a real email thread does NOT make a message legitimate.",
            "Bank detail change requests in email threads are a major red flag.",
            "Always verify payment detail changes via a known phone number from your own records.",
            "Report suspicious emails to your IT security team even if they appear to be in real threads.",
            "Be wary of attachments even from known contacts whose email may be compromised.",
        ]),
    },
    {
        "title": "AWS Security Alert",
        "difficulty": "Advanced",
        "is_phishing": False,
        "email_content": """From: no-reply@sns.amazonaws.com
To: devops@company.com
Subject: [AWS] IAM Access Key Exposed - Action Required

Hello,

AWS has detected that an IAM access key associated with your AWS account
(Account ID: 123456789012) has been exposed publicly.

The exposed key is:
Access Key ID: AKIAIOSFODNN7EXAMPLE (now automatically deactivated)

This key appears in a public GitHub repository:
https://github.com/your-org/your-repo/blob/main/config.py

We have automatically deactivated this key to protect your account.
No further action is needed to deactivate it, but you should:
1. Review your account for any unauthorised activity in CloudTrail
2. Create a new access key if needed
3. Review the IAM Best Practices guide

To manage your IAM keys:
https://console.aws.amazon.com/iam/home#/security_credentials

For questions, contact AWS Support at:
https://aws.amazon.com/support/

AWS Security Team
""",
        "indicators": json.dumps([]),
        "explanation": (
            "This is a legitimate AWS security notification. AWS genuinely sends these "
            "alerts when exposed credentials are detected. Legitimacy signals: SNS sender "
            "domain (@sns.amazonaws.com), all links go to amazonaws.com or aws.amazon.com, "
            "the email provides specific account details, the action taken (deactivation) "
            "is explained, and it does NOT ask you to click a link to 'verify' - it tells "
            "you what was already done."
        ),
        "learning_points": json.dumps([
            "Legitimate security alerts describe the specific action taken - they don't ask you to 'click to fix'.",
            "AWS sends genuine automated security notifications via @sns.amazonaws.com.",
            "All links in legitimate AWS emails go to amazonaws.com or aws.amazon.com.",
            "Never commit credentials to public git repositories - use environment variables or secrets managers.",
        ]),
    },
]


def seed_database(force: bool = False) -> None:
    """
    Seed the database with all predefined phishing and legitimate scenarios.

    Args:
        force: If True, clears all existing scenarios before re-seeding.
               Defaults to False (skip if data already exists).
    """
    existing_count = Scenario.query.count()
    if existing_count > 0:
        if not force:
            print(f"Database already contains {existing_count} scenarios. Skipping seed.")
            print("Re-run with --force to clear and re-seed.")
            return
        print(f"Force mode: deleting {existing_count} existing scenarios...")
        Scenario.query.delete()
        db.session.commit()

    print(f"Seeding {len(SCENARIOS)} scenarios...")

    for scenario_data in SCENARIOS:
        scenario = Scenario(
            title=scenario_data["title"],
            difficulty=scenario_data["difficulty"],
            email_content=scenario_data["email_content"],
            is_phishing=scenario_data["is_phishing"],
            indicators=scenario_data["indicators"],
            explanation=scenario_data["explanation"],
            learning_points=scenario_data["learning_points"],
        )
        db.session.add(scenario)

    db.session.commit()
    print(f"Successfully seeded {len(SCENARIOS)} scenarios.")
    print(f"   Beginner:     {sum(1 for s in SCENARIOS if s['difficulty'] == 'beginner')}")
    print(f"   Intermediate: {sum(1 for s in SCENARIOS if s['difficulty'] == 'intermediate')}")
    print(f"   Advanced:     {sum(1 for s in SCENARIOS if s['difficulty'] == 'advanced')}")
    print(f"   Phishing:     {sum(1 for s in SCENARIOS if s['is_phishing'])}")
    print(f"   Legitimate:   {sum(1 for s in SCENARIOS if not s['is_phishing'])}")


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    app = create_app("development")
    with app.app_context():
        db.create_all()
        seed_database(force=force)
