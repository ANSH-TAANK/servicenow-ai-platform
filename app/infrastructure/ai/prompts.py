"""
AI Prompt Builder

Purpose:
- Build prompts for AI providers.
- Keep prompt templates centralized.
"""

# ============================================================
# Incident Prompt
# ============================================================


def build_incident_prompt(
    issue: str,
) -> str:
    """
    Build the prompt used for
    incident prediction.
    """

    return f"""
You are an expert IT Service Management (ITSM) engineer.

Your task is to analyze the user's issue and generate the fields required
to create a ServiceNow incident.

Return ONLY valid JSON.

Do NOT wrap the JSON inside markdown.

Do NOT add explanations.

Return exactly this schema:

{{
    "short_description": "...",
    "description": "...",
    "category": "...",
    "subcategory": "...",
    "impact": "1",
    "urgency": "1",
    "assignment_group": "...",
    "confidence": 0.95
}}

Field Guidelines:

- short_description:
  Generate a professional ServiceNow incident title.

Requirements:
- 5 to 10 words
- Maximum 80 characters
- Start with the affected system, service, or application whenever possible
- Do not start with "User reports", "The user", "Issue with", or "Problem with"
- Use clear technical wording
- Avoid unnecessary adjectives
- Make it searchable for IT support engineers

Good examples:
- VPN connection failure
- Outlook crashes during startup
- Unable to access shared network drive
- Active Directory password reset required
- Wi-Fi authentication failure
- Email delivery delayed
- Network printer unavailable

- description:
  A detailed explanation of the user's issue suitable for the
  ServiceNow Description field.

- category:
  Best matching ServiceNow category.

- subcategory:
  Appropriate subcategory.

- assignment_group:
  Most appropriate resolver group.

- impact:
    1 = High
    2 = Medium
    3 = Low

- urgency:
    1 = High
    2 = Medium
    3 = Low

- confidence:
  Decimal value between 0 and 1.

User Issue:

{issue}
"""
