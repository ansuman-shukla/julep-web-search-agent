from fastapi import APIRouter, HTTPException
from models.queryModels import QueryModel
from models.responseModel import ResponseModel # Import ResponseModel for response validation
from service.agent import execute_research_task # Import the new function

router = APIRouter(
    tags=["ask"],
    responses={404: {"description": "Not found"}}
)


@router.post("/research",
          # Use ResponseModel to define the successful response structure
          response_model=ResponseModel,
          summary="Perform research on a topic using Julep Agent",
          tags=["Research"])
# Make the endpoint asynchronous
async def get_response(
    query : QueryModel
    ):
    """
    Endpoint to get a research response from the Julep agent
    based on the provided topic and desired output format.
    """
    # Call the asynchronous function from agent.py
    result = await execute_research_task(topic=query.topic, output_format=query.output_format)

    # Check if the result contains an error
    if isinstance(result, dict) and "error" in result:
        # Raise HTTPException for errors
        raise HTTPException(status_code=500, detail=result)

    # If successful, return the result which should match ResponseModel
    # FastAPI will automatically validate against ResponseModel
    return result