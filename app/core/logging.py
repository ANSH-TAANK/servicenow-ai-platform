"""
Application Logging

Purpose:
- Configure the application's logging system.
- Provide a logger for every module.
"""

import logging

# ============================================================
# Configure Logging
# ============================================================


def configure_logging() -> None:
    """
    Configure the application's logging system.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s | " "%(levelname)-8s | " "%(name)s | " "%(message)s"),
    )


# ============================================================
# Logger Factory
# ============================================================


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger instance for the given module.

    Args:
        name: Usually pass __name__.

    Returns:
        Configured Logger instance.
    """

    return logging.getLogger(name)


# ============================================================
# Initialize Logging
# ============================================================

configure_logging()
