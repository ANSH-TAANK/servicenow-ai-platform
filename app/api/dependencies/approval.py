"""
Approval Dependencies

Purpose:
- Provide approval-related dependencies.
- Construct approval services.
- Support dependency injection for approval workflows.

This module DOES NOT:
- Contain business logic.
- Access HTTP requests directly.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.approval.service import ApprovalService
from app.infrastructure.database.session import get_db

# ============================================================
# Approval Service Dependency
# ============================================================


async def get_approval_service(
    db: AsyncSession = Depends(get_db),
) -> ApprovalService:
    """
    Provide an approval service.
    """

    return ApprovalService(db)
