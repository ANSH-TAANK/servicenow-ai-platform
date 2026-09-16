"""
Approval Response Models

Purpose:
- Define response models for approval workflows.
"""

from pydantic import BaseModel, ConfigDict


class ApprovalCallbackResponse(BaseModel):
    """
    Response returned after successfully processing
    an approval callback.
    """

    model_config = ConfigDict(
        frozen=True,
    )

    message: str
