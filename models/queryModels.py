from pydantic import BaseModel, Field


class QueryModel(BaseModel):
    topic: str = Field(..., description="The topic to research.") # Renamed from 'query' to 'topic'
    output_format: str = Field(..., description="The desired format of the output ('summary', 'bullet points', 'short report').") # Made required and updated description