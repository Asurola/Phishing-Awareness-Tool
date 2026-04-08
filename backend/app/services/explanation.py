"""
app/services/explanation.py — Human-readable explanation engine.
Converts ML output + feature values into structured flag cards for the UI.
"""

from __future__ import annotations
from typing import Any

RISK_LOW_THRESHOLD    = 35
RISK_MEDIUM_THRESHOLD = 65


def confidence_to_risk_score(prediction: str, confidence: float) -> int:
    if prediction == 'phishing':
        return round(confidence * 100)
    return round((1 - confidence) * 100)


def get_verdict(risk_score: int) -> str:
    if risk_score < RISK_LOW_THRESHOLD:
        return 'Low Risk — Likely Legitimate'
    elif risk_score < RISK_MEDIUM_THRESHOLD:
        return 'Medium Risk — Treat with Caution'
    return 'High Risk — Likely Phishing'


def generate_explanation(
    prediction_result: dict[str, Any],
    subject: str,
    body: str,
) -> dict[str, Any]:
    """
    Generate structured flags and recommendations from model output.

    Args:
        prediction_result: Output from ml_classifier.predict()
        subject:           Email subject string
        body:              Email body string

    Returns:
        Full explanation dict ready for the frontend.
    """
    prediction  = prediction_result['prediction']
    confidence  = prediction_result['confidence']
    eng_feats   = prediction_result.get('engineered_features', {})

    risk_score = confidence_to_risk_score(prediction, confidence)
    verdict    = get_verdict(risk_score)
    flags      = _build_flags(eng_feats, subject, body, prediction)

    recommendations = _build_recommendations(prediction, flags)

    return {
        'risk_score':             risk_score,
        'verdict':                verdict,
        'prediction':             prediction,
        'confidence':             round(confidence * 100, 1),
        'flags':                  flags,
        'summary_recommendations': recommendations,
    }


# ── Private helpers ──────────────────────────────────────────────────────────

def _build_flags(
    eng: dict,
    subject: str,
    body: str,
    prediction: str,
) -> list[dict]:
    """Build individual threat flag cards from feature values."""
    flags = []
    body_lower  = body.lower()
    subject_low = subject.lower()

    # ── Content flags ─────────────────────────────────────────────────────

    urgency = eng.get('urgency_keyword_count', 0)
    if urgency >= 2:
        flags.append({
            'category':       'Content',
            'severity':       'high' if urgency >= 4 else 'medium',
            'finding':        f'Urgency language detected ({urgency} instances)',
            'explanation':    (
                f'This email contains {urgency} urgency phrases such as '
                '"urgent", "verify", "suspend", or "click". Phishing emails '
                'create false time pressure to prevent careful thinking.'
            ),
            'recommendation': (
                'Slow down. Legitimate organisations rarely threaten '
                'immediate account suspension via email.'
            ),
        })

    if eng.get('url_count', 0) > 0:
        url_count = eng['url_count']
        flags.append({
            'category':       'URL',
            'severity':       'high' if url_count >= 3 else 'medium',
            'finding':        f'{url_count} URL(s) detected in email body',
            'explanation':    (
                'The email contains embedded links. Phishing emails use '
                'links to direct victims to fake login pages or malware downloads.'
            ),
            'recommendation': (
                'Hover over links to check the real destination. '
                'Navigate to websites directly by typing in your browser — '
                'never click links in unexpected emails.'
            ),
        })

    if eng.get('has_html', 0):
        flags.append({
            'category':       'Content',
            'severity':       'low',
            'finding':        'HTML content detected',
            'explanation':    (
                'The email contains HTML formatting. HTML emails can hide '
                'the true destination of links behind display text.'
            ),
            'recommendation': (
                'Be extra vigilant with HTML emails — the visible link text '
                'may differ from the actual URL destination.'
            ),
        })

    # ── Header flags ──────────────────────────────────────────────────────

    if eng.get('sender_reply_mismatch', 0):
        flags.append({
            'category':       'Header',
            'severity':       'high',
            'finding':        'Reply-To address differs from sender',
            'explanation':    (
                'The Reply-To header points to a different address than the From field. '
                'This is a common tactic to ensure replies go to the attacker '
                'rather than the stated sender.'
            ),
            'recommendation': (
                'Do not reply to this email. Verify the sender\'s identity '
                'through a separate, trusted channel.'
            ),
        })

    if not eng.get('has_spf', 0) and not eng.get('has_dkim', 0):
        # Only flag missing auth if email appears to be phishing
        if prediction == 'phishing':
            flags.append({
                'category':       'Header',
                'severity':       'medium',
                'finding':        'No SPF or DKIM authentication detected',
                'explanation':    (
                    'Legitimate organisations use SPF and DKIM to authenticate their emails. '
                    'The absence of these records increases the risk that this email '
                    'is spoofed or from an unverified sender.'
                ),
                'recommendation': (
                    'Treat unauthenticated emails claiming to be from well-known '
                    'organisations with extra suspicion.'
                ),
            })

    if eng.get('display_name_spoofed', 0):
        flags.append({
            'category':       'Header',
            'severity':       'high',
            'finding':        'Potential display name spoofing',
            'explanation':    (
                'The sender\'s display name appears to contain a domain name, '
                'which is a tactic used to make emails appear to come from '
                'a trusted source like "PayPal Support <attacker@evil.com>".'
            ),
            'recommendation': (
                'Always check the full email address in angle brackets, '
                'not just the display name.'
            ),
        })

    # ── Subject-line flags ────────────────────────────────────────────────

    subject_triggers = [
        ('action required', 'Action Required subject line'),
        ('verify', 'Verification request in subject'),
        ('suspended', 'Account suspension mentioned'),
        ('winner', 'Prize/lottery language in subject'),
        ('congratulations', 'Prize/lottery language in subject'),
        ('invoice', 'Financial document reference'),
        ('urgent', 'Urgency language in subject'),
    ]
    for trigger, label in subject_triggers:
        if trigger in subject_low:
            flags.append({
                'category':       'Content',
                'severity':       'medium',
                'finding':        label,
                'explanation':    (
                    f'The subject line contains "{trigger}", which is commonly '
                    'used in phishing emails to create urgency or curiosity.'
                ),
                'recommendation': (
                    'Treat emails with alarming or enticing subject lines with '
                    'extra scepticism — verify with the sender through a separate channel.'
                ),
            })
            break  # Only flag one subject trigger

    return flags


def _build_recommendations(prediction: str, flags: list[dict]) -> list[str]:
    """Generate top-level summary recommendations."""
    if prediction == 'legitimate':
        return [
            'This email appears legitimate, but always stay vigilant.',
            'Verify unexpected requests through a separate communication channel.',
            'Never share passwords or sensitive data via email.',
        ]

    recs = [
        'Do not click any links in this email.',
        'Do not provide any personal or financial information.',
        'Report this email as phishing to your email provider.',
    ]
    if any(f['category'] == 'URL' for f in flags):
        recs.append(
            'If you already clicked a link, change your passwords immediately '
            'and check your accounts for unauthorised activity.'
        )
    recs.append(
        'If the email claims to be from a company you use, '
        'contact them directly via their official website.'
    )
    return recs