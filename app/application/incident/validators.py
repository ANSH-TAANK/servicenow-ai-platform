"""
Incident Application Validators

Purpose:
- Validate incident creation requests.
"""

from app.application.incident.requests import CreateIncidentRequest
from app.exceptions.validation import ValidationError

# ============================================================
# Request Validator
# ============================================================


def validate_create_incident_request(
    request: CreateIncidentRequest,
) -> None:
    """
    Validate a create incident request.
    """

    issue = request.issue.strip()

    if not issue:

        raise ValidationError("Issue description cannot be empty.")

    if len(issue) < 5:

        raise ValidationError("Issue description is too short.")

    if len(issue) > 5000:

        raise ValidationError("Issue description is too long.")
