"""
app/services/explanation.py - Human-readable explanation engine.

Converts the raw feature vector produced by `ml_classifier.classify()`
into a list of user-facing threat flags plus a set of actionable
recommendations. This is what turns the model from a black box into
an educational tool - when a user sees "flagged as phishing", they
also see *why*.

The engine focuses exclusively on the 25 engineered features; TF-IDF
terms are deliberately omitted because they are dense, numerous, and
not meaningful to end users ("body_account: 0.17" explains nothing).

Output schema (matches the frontend's expected response shape):

    [
        {
            "category":       "url" | "header" | "content",
            "severity":       "high" | "medium" | "low",
            "title":          "Short human-readable name",
            "description":    "What was detected",
            "recommendation": "What the user should do",
        },
        ...
    ]
"""

from __future__ import annotations

from typing import Any

# Each rule: (feature_key, predicate, category, severity, title, description, recommendation)
# Predicates are callables so we can handle both flag features (value == 1)
# and threshold features (value > N).

# Features are grouped by category for display purposes. The category
# label is what the frontend uses to group flags in expandable cards.


def generate_flags(
    engineered: dict[str, Any],
    probability: float,
) -> list[dict[str, Any]]:
    """
    Build the list of threat flags triggered by the extracted features.

    Args:
        engineered: The 25 engineered features from the classifier.
        probability: The model's P(phishing) for this email.

    Returns:
        List of flag dicts. May be empty if nothing suspicious was found.
        Flags are sorted high → low severity.
    """
    flags: list[dict[str, Any]] = []

    # ── Header-derived flags ─────────────────────────────────────────────
    if engineered.get("display_name_spoofed", 0) == 1:
        flags.append({
            "category": "header",
            "severity": "high",
            "title": "Display name impersonates a known brand",
            "description": (
                "The sender name mentions a well-known company but the "
                "actual email domain does not belong to that company. "
                "This is a classic brand-impersonation technique."
            ),
            "recommendation": (
                "Never trust a display name alone - always check that the "
                "domain after '@' matches the company's real website."
            ),
        })

    if engineered.get("sender_reply_mismatch", 0) == 1:
        flags.append({
            "category": "header",
            "severity": "high",
            "title": "Reply-To address does not match sender",
            "description": (
                "The Reply-To header points to a different domain than "
                "the From address. Legitimate senders rarely do this; "
                "phishers use it to capture replies at an attacker-"
                "controlled inbox."
            ),
            "recommendation": (
                "Do not reply to this email. If you need to contact the "
                "organisation, use a phone number or URL you already "
                "trust - not anything from this email."
            ),
        })

    if engineered.get("has_spf", 0) == 0 and engineered.get("has_dkim", 0) == 0:
        # Only surface this as a flag if other suspicious signals exist too,
        # since pasted emails often lose their authentication headers.
        # We'll attach it as low severity.
        if probability > 0.5:
            flags.append({
                "category": "header",
                "severity": "low",
                "title": "No authentication headers detected",
                "description": (
                    "Neither SPF nor DKIM pass markers were found in the "
                    "email. This may simply mean the headers were stripped "
                    "when the email was pasted, but if present it would "
                    "help verify the sender's identity."
                ),
                "recommendation": (
                    "If you have access to the original .eml file, upload "
                    "that instead for a more thorough check."
                ),
            })

    # ── URL-derived flags ────────────────────────────────────────────────
    if engineered.get("url_uses_ip", 0) == 1:
        flags.append({
            "category": "url",
            "severity": "high",
            "title": "Link uses a raw IP address",
            "description": (
                "At least one link in this email points to a numeric IP "
                "address instead of a domain name. Legitimate services "
                "almost never do this - it's a way to hide the true "
                "destination of a link."
            ),
            "recommendation": (
                "Do not click the link. Navigate to the service's official "
                "website directly in your browser if you need to act."
            ),
        })

    if engineered.get("url_suspicious_tld", 0) == 1:
        flags.append({
            "category": "url",
            "severity": "medium",
            "title": "Link uses a high-risk top-level domain",
            "description": (
                "One or more links use a top-level domain (e.g. .tk, .ml, "
                ".xyz) that is frequently abused by phishing operators "
                "because it can be registered cheaply and anonymously."
            ),
            "recommendation": (
                "Treat the link with extreme suspicion. Brand-name "
                "organisations do not use these TLDs for official email."
            ),
        })

    if engineered.get("url_has_at_symbol", 0) == 1:
        flags.append({
            "category": "url",
            "severity": "medium",
            "title": "Link contains an '@' symbol",
            "description": (
                "The URL contains an '@' character, which causes most "
                "browsers to ignore everything before it. This trick is "
                "used to make a malicious URL look like it goes to a "
                "legitimate site."
            ),
            "recommendation": (
                "Do not click the link - inspect what comes *after* the "
                "'@' to see where it actually leads."
            ),
        })

    url_length = int(engineered.get("url_length", 0) or 0)
    if url_length > 100:
        flags.append({
            "category": "url",
            "severity": "low",
            "title": "Unusually long URL",
            "description": (
                f"A URL in this email is {url_length} characters long. "
                "Very long URLs are often used to bury the real "
                "destination behind parameters."
            ),
            "recommendation": (
                "Hover over the link (without clicking) to see where it "
                "really goes. When in doubt, visit the site directly."
            ),
        })

    ext_domains = int(engineered.get("external_domain_count", 0) or 0)
    if ext_domains >= 5:
        flags.append({
            "category": "url",
            "severity": "low",
            "title": f"Links to {ext_domains} different domains",
            "description": (
                "This email contains links to many unrelated domains. "
                "Legitimate transactional emails usually link to just "
                "one or two."
            ),
            "recommendation": (
                "Check whether the domains actually belong to the "
                "claimed sender's organisation."
            ),
        })

    # ── Content-derived flags ────────────────────────────────────────────
    urgency = int(engineered.get("urgency_keyword_count", 0) or 0)
    if urgency >= 5:
        severity = "high" if urgency >= 10 else "medium"
        flags.append({
            "category": "content",
            "severity": severity,
            "title": f"High use of urgency language ({urgency} occurrences)",
            "description": (
                "The email contains many urgency phrases such as 'verify "
                "immediately', 'act now', or 'account locked'. Creating "
                "a false sense of time pressure is a core social-"
                "engineering tactic."
            ),
            "recommendation": (
                "Pause before reacting. Real institutions give you time "
                "to verify requests through official channels."
            ),
        })
    elif urgency >= 2:
        flags.append({
            "category": "content",
            "severity": "low",
            "title": "Urgency language detected",
            "description": (
                f"The email contains {urgency} urgency-related phrases. "
                "This is not conclusive on its own but is a common "
                "phishing pattern."
            ),
            "recommendation": (
                "Take a moment to verify the claim independently before "
                "acting."
            ),
        })

    if engineered.get("credential_request", 0) == 1:
        flags.append({
            "category": "content",
            "severity": "high",
            "title": "Email asks for credentials",
            "description": (
                "The email references passwords, login details, or other "
                "credentials. Legitimate services do not ask you to send "
                "or enter credentials in response to an email."
            ),
            "recommendation": (
                "Never enter your password on a page you reached via an "
                "email link. Always navigate to the site directly."
            ),
        })

    if engineered.get("financial_threat", 0) == 1:
        flags.append({
            "category": "content",
            "severity": "high",
            "title": "Financial scam keywords detected",
            "description": (
                "The email contains language typical of advance-fee "
                "fraud or inheritance scams (e.g. 'wire transfer', "
                "'lottery', 'inheritance'). These are almost always "
                "scams."
            ),
            "recommendation": (
                "Do not respond. Do not send any money or personal "
                "information."
            ),
        })

    html_ratio = float(engineered.get("html_to_text_ratio", 0) or 0)
    if html_ratio > 0.5:
        flags.append({
            "category": "content",
            "severity": "low",
            "title": "Body is mostly HTML markup",
            "description": (
                f"Roughly {int(html_ratio * 100)}% of this email's body "
                "is HTML markup rather than readable text. Phishers often "
                "use heavy styling to mimic brand emails and hide content."
            ),
            "recommendation": (
                "Be extra cautious - view the email in plain text mode "
                "if your client supports it."
            ),
        })

    if engineered.get("exclamation_count", 0) and int(engineered["exclamation_count"]) >= 5:
        flags.append({
            "category": "content",
            "severity": "low",
            "title": "Excessive exclamation marks",
            "description": (
                "The email contains many exclamation marks, often used "
                "to manufacture excitement or urgency."
            ),
            "recommendation": (
                "Professional communication from banks, employers, and "
                "service providers rarely reads this way."
            ),
        })

    # Sort by severity (high first) for a sensible default display order
    severity_rank = {"high": 0, "medium": 1, "low": 2}
    flags.sort(key=lambda f: severity_rank.get(f["severity"], 3))

    return flags


def risk_score(probability: float) -> int:
    """
    Convert the model's phishing probability into a 0–100 risk score.

    We use a simple linear mapping because the model is already well-
    calibrated (ROC-AUC ≈ 0.998 on the held-out test set). Rounding to
    an integer avoids implying false precision in the UI.
    """
    return int(round(probability * 100))


def verdict(probability: float) -> str:
    """
    Map the risk score to one of four user-facing verdict bands.

    The bands are chosen to give a more informative display than a flat
    "phishing / legitimate" flip, while still being anchored to the
    model's 0.5 decision threshold.
    """
    if probability >= 0.80:
        return "High Risk - Likely Phishing"
    if probability >= 0.50:
        return "Elevated Risk - Suspicious"
    if probability >= 0.20:
        return "Low Risk - Probably Safe"
    return "Minimal Risk - Likely Legitimate"


def summary_recommendations(
    flags: list[dict[str, Any]],
    probability: float,
) -> list[str]:
    """
    Produce the short, top-level recommendation bullets shown at the
    bottom of the analysis panel. These are condensed guidance, not
    per-flag explanations.
    """
    recs: list[str] = []

    if probability >= 0.5:
        recs.append("Do not click any links or download attachments from this email.")
        recs.append("Do not reply or provide personal information.")
        recs.append("Report the email to your IT or security team if applicable.")
        if any(f["category"] == "url" for f in flags):
            recs.append(
                "If you need to act, visit the service's official website "
                "directly by typing the URL into your browser."
            )
    else:
        recs.append(
            "No strong phishing indicators were found, but always remain "
            "cautious with unexpected messages."
        )
        if flags:
            recs.append(
                "Some lower-severity signals were detected - review the "
                "flags above before trusting the message."
            )

    return recs
