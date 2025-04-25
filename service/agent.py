import yaml
from julep import Client
import time
import json
import os
from dotenv import load_dotenv
import asyncio # Import asyncio for potential async sleep

# --- Configuration ---
load_dotenv() # Load .env file for API Keys if present
JULEP_API_KEY = os.getenv("JULEP_API_KEY")
TASK_YAML_FILE = 'search_task.yaml' # Make sure this filename matches

# --- Julep Client Initialization ---
try:
    if not JULEP_API_KEY:
        print("Error: JULEP_API_KEY not found in environment variables or .env file.")
        print("Please ensure your Julep API key is set.")
        exit(1)
    client = Client(api_key=JULEP_API_KEY)
    print("Julep client initialized.")
except Exception as e:
    print(f"Error initializing Julep client: {e}")
    exit(1)

# --- Agent Creation ---
# Agent instructions guide the LLM during the 'prompt' step within the task
AGENT_INSTRUCTIONS = [
    "You are processing content fetched from Wikipedia. Format this content strictly according to the user's request ('summary', 'bullet points', 'short report').",
    "Adhere to length and style constraints: summary (3-4 sentences), bullet points (max 5, use '*'), short report (under 150 words).",
    "If the provided content is insufficient or indicates an error, state that clearly."
]
AGENT_NAME = "Wikipedia Research Agent" # Corrected typo
AGENT_MODEL = "gemini-2.0-flash" # Using a known model, adjust if needed

# --- Task Creation ---
# Keep agent and task creation outside the function for now
# In a production app, consider how to manage these resources (e.g., cache, retrieve by ID)
agent = None
task = None
try:
    # Consider finding agent by name first in a real application to avoid duplicates
    print(f"Creating/Ensuring Julep Agent: '{AGENT_NAME}'...")
    agent = client.agents.create(
        name=AGENT_NAME,
        model=AGENT_MODEL,
        about="You are Research Assistant. Your primary goal is to provide accurate and concise information based on user requests by processing Wikipedia content.",
        instructions=AGENT_INSTRUCTIONS,
    )
    print(f"Agent created/retrieved with ID: {agent.id}")

    print(f"Loading task definition from {TASK_YAML_FILE}...")
    with open(TASK_YAML_FILE, 'r') as file:
        task_definition = yaml.safe_load(file)
    print("Task definition loaded.")

    # Ensure the task name in the YAML matches what you expect
    task_name_from_yaml = task_definition.get('name', 'Unknown Task Name')
    print(f"Creating/Ensuring Julep Task '{task_name_from_yaml}' associated with Agent ID {agent.id}...")

    # Create the task, associating it with the agent
    task = client.tasks.create(
        agent_id=agent.id,
        **task_definition # Unpack the loaded dictionary
    )
    print(f"Task created/retrieved with ID: {task.id}")

except Exception as e:
    print(f"Error during initial setup (agent/task creation): {e}")
    # Decide if the application should exit or handle this differently
    exit(1)

# --- Task Execution Function ---
async def execute_research_task(topic: str, output_format: str):
    """
    Executes the Julep research task for a given topic and output format.
    """
    if not agent or not task:
        return {"error": "Agent or Task not initialized properly."}

    try:
        execution_input = {"topic": topic, "output_format": output_format}

        print(f"\nCreating execution for Task ID: {task.id} with input: {execution_input}")
        execution = client.executions.create(
            task_id=task.id,
            input=execution_input,
        )
        print(f"Execution created with ID: {execution.id}. Polling status...")

        # --- Polling for Result ---
        while True:
            result = client.executions.get(execution.id)
            print(f"Execution status: {result.status}") # Provide continuous feedback
            if result.status in ['succeeded', 'failed', 'cancelled']:
                break
            # Use asyncio.sleep for non-blocking wait in async context
            await asyncio.sleep(3) # Wait for a few seconds before polling again

        # --- Handling Final Output ---
        if result.status == "succeeded":
            print("\nExecution succeeded!")
            content = result.output
            final_content_str = str(content) if content is not None else ""
            output_json = {"result": final_content_str}
            print("\nFinal Output (JSON):")
            print(json.dumps(output_json, indent=2))
            return output_json # Return the successful result

        else:
            print(f"\nExecution finished with status: {result.status}")
            error_details = result.error if result.error else "No specific error details provided."
            print(f"Error details: {error_details}")
            # Return an error dictionary
            return {"error": f"Execution failed with status: {result.status}", "details": error_details}

    except Exception as e:
        print(f"\nAn unexpected error occurred during execution: {e}")
        # Return an error dictionary for unexpected errors
        return {"error": "An unexpected error occurred during execution.", "details": str(e)}

# --- Example Usage (Optional - can be removed if only used by the route) ---
# async def main():
#     # Example call
#     response = await execute_research_task(topic="Quantum Computing", output_format="bullet points")
#     print("\n--- Function Call Result ---")
#     print(response)

# if __name__ == "__main__":
#     asyncio.run(main())