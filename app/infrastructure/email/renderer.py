"""
Email Template Renderer

Purpose:
- Render HTML email templates.
- Replace template placeholders.
- Build complete email HTML.
"""

# Standard Library Imports
from datetime import datetime
from pathlib import Path

# ============================================================
# Email Template Renderer
# ============================================================


class EmailTemplateRenderer:
    """
    Responsible for rendering HTML email templates.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the template renderer.
        """

        self._templates_directory = Path(__file__).parent / "templates"

    # ============================================================
    # Render Template
    # ============================================================

    def render(
        self,
        *,
        template: str,
        title: str,
        context: dict[str, str],
    ) -> str:
        """
        Render an email template.
        """

        # --------------------------------------------------------
        # Load Templates
        # --------------------------------------------------------

        base_html = self._load_template(
            "base.html",
        )

        content_html = self._load_template(
            template,
        )

        # --------------------------------------------------------
        # Replace Content Variables
        # --------------------------------------------------------

        content_html = self._replace_variables(
            content_html,
            context,
        )

        # --------------------------------------------------------
        # Build Final HTML
        # --------------------------------------------------------

        html = self._replace_variables(
            base_html,
            {
                "title": title,
                "content": content_html,
                "year": str(
                    datetime.now().year,
                ),
            },
        )

        return html

    # ============================================================
    # Load Template
    # ============================================================

    def _load_template(
        self,
        template: str,
    ) -> str:
        """
        Load an HTML template.
        """

        return (self._templates_directory / template).read_text(
            encoding="utf-8",
        )

    # ============================================================
    # Replace Variables
    # ============================================================

    def _replace_variables(
        self,
        html: str,
        variables: dict[str, str],
    ) -> str:
        """
        Replace template placeholders.
        """

        for key, value in variables.items():

            html = html.replace(
                f"{{{{ {key} }}}}",
                str(value),
            )

        return html
