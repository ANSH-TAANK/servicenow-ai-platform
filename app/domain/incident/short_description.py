"""
Incident Short Description Generator

Purpose:
- Generate standardized ServiceNow
  short descriptions.

Business rules are defined in
templates.py.

Business logic is defined here.
"""

import re

from app.domain.incident.templates import SHORT_DESCRIPTION_TEMPLATES

# ============================================================
# Short Description Generator
# ============================================================


def generate_short_description(
    category: str,
    subcategory: str,
    description: str,
) -> str:
    """
    Generate a professional ServiceNow
    short description.
    """

    category = category.strip().lower()

    subcategory = subcategory.strip().lower()

    # --------------------------------------------------------
    # Template Lookup
    # --------------------------------------------------------

    template = SHORT_DESCRIPTION_TEMPLATES.get(
        (
            category,
            subcategory,
        )
    )

    if template:

        return template

    # --------------------------------------------------------
    # Generic Category Fallback
    # --------------------------------------------------------

    category_titles = {
        "network": "Network Connectivity Issue",
        "hardware": "Hardware Issue",
        "software": "Software Application Issue",
        "email": "Email Service Issue",
        "access": "User Access Issue",
    }

    if category in category_titles:

        return category_titles[category]

    # --------------------------------------------------------
    # Description Fallback
    # --------------------------------------------------------

    description = re.sub(
        r"\s+",
        " ",
        description.strip(),
    )

    description = (
        description.replace(
            "User reports",
            "",
        )
        .replace(
            "The user",
            "",
        )
        .strip()
    )

    return description[:80]
