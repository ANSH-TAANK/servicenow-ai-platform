"""
Username Suggestion Generator

Purpose:
- Generate deterministic username suggestions.
- Produce clean username candidates.
- Avoid database access.

This module DOES NOT:
- Access the database.
- Check username availability.
- Validate usernames.
"""

import hashlib
import re
from datetime import datetime

from app.core.constants import USERNAME_MAX_LENGTH

# ============================================================
# Username Suggestion Generator
# ============================================================


class UsernameSuggestionGenerator:
    """
    Generate deterministic username candidates.
    """

    WORD_SUFFIXES = (
        "official",
        "team",
        "dev",
        "labs",
        "hq",
        "pro",
    )

    def generate(
        self,
        username: str,
        *,
        limit: int = 10,
    ) -> list[str]:
        """
        Generate username candidates.
        """

        if limit <= 0:
            return []

        base = self._sanitize(
            username,
        )

        if not base:
            return []

        compact = base.replace(
            "_",
            "",
        )

        candidates: list[str] = []

        self._add_numeric_candidates(
            candidates,
            base,
            limit,
        )

        self._add_compact_candidate(
            candidates,
            base,
            compact,
        )

        self._add_year_candidates(
            candidates,
            compact,
        )

        self._add_word_candidates(
            candidates,
            compact,
        )

        self._add_hash_candidates(
            candidates,
            compact,
        )

        return self._deduplicate(
            candidates,
        )[:limit]

    # ============================================================
    # Candidate Builders
    # ============================================================

    def _add_numeric_candidates(
        self,
        candidates: list[str],
        base: str,
        limit: int,
    ) -> None:
        """
        Add sequential numeric candidates.
        """

        for number in range(
            1,
            limit + 1,
        ):
            candidates.append(
                self._build_candidate(
                    base,
                    str(number),
                ),
            )

    def _add_compact_candidate(
        self,
        candidates: list[str],
        base: str,
        compact: str,
    ) -> None:
        """
        Add an underscore-free variation.
        """

        if compact != base:
            candidates.append(
                compact,
            )

    def _add_year_candidates(
        self,
        candidates: list[str],
        compact: str,
    ) -> None:
        """
        Add nearby year variations.
        """

        current_year = datetime.now().year

        for year in (
            current_year - 1,
            current_year,
            current_year + 1,
        ):
            candidates.append(
                self._build_candidate(
                    compact,
                    str(year),
                ),
            )

    def _add_word_candidates(
        self,
        candidates: list[str],
        compact: str,
    ) -> None:
        """
        Add human-readable suffixes.
        """

        for suffix in self.WORD_SUFFIXES:
            candidates.append(
                self._build_candidate(
                    compact,
                    f"_{suffix}",
                ),
            )

    def _add_hash_candidates(
        self,
        candidates: list[str],
        compact: str,
    ) -> None:
        """
        Add deterministic hash-based candidates.
        """

        seed = int(
            hashlib.sha256(
                compact.encode(),
            ).hexdigest(),
            16,
        )

        values = (
            seed % 89 + 10,
            (seed // 7) % 899 + 100,
        )

        for value in values:
            candidates.append(
                self._build_candidate(
                    compact,
                    str(value),
                ),
            )

    # ============================================================
    # Helpers
    # ============================================================

    def _sanitize(
        self,
        username: str,
    ) -> str:
        """
        Normalize a username.
        """

        username = username.lower().strip()

        username = re.sub(
            r"[^a-z0-9_]",
            "",
            username,
        )

        username = re.sub(
            r"_+",
            "_",
            username,
        )

        return username.strip(
            "_",
        )

    def _build_candidate(
        self,
        base: str,
        suffix: str,
    ) -> str:
        """
        Build a username candidate while
        preserving the suffix.
        """

        available = USERNAME_MAX_LENGTH - len(
            suffix,
        )

        if available < 1:
            return suffix[:USERNAME_MAX_LENGTH]

        return f"{base[:available]}{suffix}"

    def _deduplicate(
        self,
        candidates: list[str],
    ) -> list[str]:
        """
        Remove duplicate candidates while
        preserving insertion order.
        """

        unique: list[str] = []

        seen: set[str] = set()

        for candidate in candidates:

            if candidate in seen:
                continue

            seen.add(
                candidate,
            )

            unique.append(
                candidate,
            )

        return unique
