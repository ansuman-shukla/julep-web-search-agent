from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    result: str = Field(..., description="The research result from the Julep agent.")