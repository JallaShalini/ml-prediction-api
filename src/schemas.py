from typing import List

from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    class_label: str = Field(description="Predicted class label")
    probabilities: List[float] = Field(description="Class probabilities for each label")


class ErrorResponse(BaseModel):
    detail: str = Field(description="Error details")
