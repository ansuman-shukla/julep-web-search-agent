from fastapi import FastAPI
from routes import askRoute

app = FastAPI(
    title="Julep Research Assistant API",
    description="Provides research on topics using a Julep AI agent.",
    version="1.0.0"
)


app.include_router(askRoute.router)


@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the Julep Research Assistant API!. Please use the /research endpoint for research queries. With a topic and a output format ('summary', 'bullet points', 'short report')."}