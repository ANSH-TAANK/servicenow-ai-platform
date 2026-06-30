"""
Incident Rule Engine

Purpose:
- Pure business rules for incident prediction.
- Contains no AI provider or infrastructure logic.
"""

from app.infrastructure.ai.enums import ImpactLevel, UrgencyLevel
from app.infrastructure.ai.models import IncidentPrediction

# ============================================================
# VPN
# ============================================================


def vpn_rule(
    text: str,
    issue: str,
) -> IncidentPrediction | None:

    if "vpn" not in text:
        return None

    return IncidentPrediction(
        short_description="VPN Connection Failure",
        description=issue,
        category="Network",
        subcategory="VPN",
        impact=ImpactLevel.MEDIUM,
        urgency=UrgencyLevel.MEDIUM,
        assignment_group="Network Team",
        confidence=0.60,
    )


# ============================================================
# Password
# ============================================================


def password_rule(
    text: str,
    issue: str,
) -> IncidentPrediction | None:

    if "password" not in text and "login" not in text:
        return None

    return IncidentPrediction(
        short_description="User Access Issue",
        description=issue,
        category="Access",
        subcategory="Password Reset",
        impact=ImpactLevel.LOW,
        urgency=UrgencyLevel.MEDIUM,
        assignment_group="Service Desk",
        confidence=0.60,
    )


# ============================================================
# Printer
# ============================================================


def printer_rule(
    text: str,
    issue: str,
) -> IncidentPrediction | None:

    if "printer" not in text:
        return None

    return IncidentPrediction(
        short_description="Printer Malfunction",
        description=issue,
        category="Hardware",
        subcategory="Printer",
        impact=ImpactLevel.LOW,
        urgency=UrgencyLevel.LOW,
        assignment_group="Desktop Support",
        confidence=0.60,
    )


# ============================================================
# Generic
# ============================================================


def generic_rule(
    issue: str,
) -> IncidentPrediction:

    return IncidentPrediction(
        short_description="General IT Issue",
        description=issue,
        category="General",
        subcategory="Other",
        impact=ImpactLevel.LOW,
        urgency=UrgencyLevel.LOW,
        assignment_group="Service Desk",
        confidence=0.50,
    )
