# Julep AI Research Assistant 🤖

This project implements an AI-powered research assistant using the Julep AI platform. It exposes a simple web API endpoint built with FastAPI that accepts a research topic and a desired output format. The backend then utilizes a Julep Task, associated with a configured Julep Agent, to perform research (currently using the Wikipedia integration) and format the findings according to the user's request. The application is designed for deployment on platforms like Railway.

## ✨ Overview

The core task is to provide concise and accurately formatted information on a given topic. The system leverages Julep AI's capabilities for managing AI agent instructions, integrating external tools (Wikipedia), and orchestrating multi-step workflows (Tasks).

**Key Features:**

* Accepts `topic` and `output_format` via a POST request.
* Uses a Julep Task (`search_task.yaml`) to define the research workflow.
* Integrates with the Julep Wikipedia tool to fetch information.
* Utilizes a configured Julep Agent to process and format the fetched content based on instructions.
* Supports output formats: `summary`, `bullet points`, `short report`.
* Returns the formatted research result as a JSON response.
* Built with Python and FastAPI for easy deployment.

## 📁 Directory Structure

└── ansuman-shukla-julep-web-search-agent/├── readMe.md                 # This file├── main.py                   # FastAPI application entry point, handles setup & endpoint├── requirements.txt          # Python dependencies├── search_task.yaml          # Julep Task definition for the research workflow├── .env.example              # Example environment variables file├── models/                   # Pydantic models (likely for request/response)│   ├── queryModels.py        # Pydantic model for request data│   ├── responseModel.py      # Pydantic model for response data│   └── pycache/├── resources/                # Placeholder for any static resources (if needed)├── routes/                   # FastAPI router definitions│   ├── askRoute.py           # Defines the /research API route logic│   └── pycache/├── service/                  # Business logic, interaction with Julep│   ├── agent.py              # Contains logic for creating/managing Julep agent & task execution│   └── pycache/└── venv/                     # Virtual environment (if created locally, usually in .gitignore)
*(Note: The specific implementation details within `models/`, `routes/`, and `service/` might vary based on your final code structure, but this reflects the provided layout.)*

## 🛠️ Technology Stack

* **Backend:** Python 3.x
* **API Framework:** FastAPI
* **AI Platform:** Julep AI
    * Agents
    * Tasks
    * Executions
    * Wikipedia Integration
* **Deployment:** Railway.app (or similar PaaS)
* **Dependencies:** `julep-ai`, `fastapi`, `uvicorn`, `python-dotenv`, `pyyaml` (see `requirements.txt`)

## 🧠 Julep Agent Design

The core intelligence lies within the Julep Agent, configured to act as a research assistant specializing in processing Wikipedia content.

* **Name:** `Wikipedia Research Agent`
* **Model:** `gemini-1.5-flash` (or your chosen model)
* **Role:** To process pre-fetched Wikipedia content and format it according to specific user requirements.
* **Instructions:** The agent is guided by layered instructions provided during its creation. These instructions are crucial for the LLM's behavior within the `prompt` step of the Julep Task:
    1.  **Core Task:** "You are processing content fetched from Wikipedia. Format this content strictly according to the user's request ('summary', 'bullet points', 'short report')."
    2.  **Formatting Constraints:** "Adhere to length and style constraints: summary (3-4 sentences), bullet points (max 5, use '*'), short report (under 150 words)."
    3.  **Error Handling:** "If the provided content is insufficient or indicates an error, state that clearly."
* **Agent ID:** `YOUR_JULEP_AGENT_ID` (Replace with the actual ID generated when you create the agent. This is needed in the environment variables).

## 📝 Julep Task (`search_task.yaml`)

The research process is defined as a Julep Task, which orchestrates the interaction between the input, tools, and the agent.

* **Name:** `Wikipedia Research Task`
* **Purpose:** To fetch Wikipedia content for a given topic and then use the associated Julep Agent to format that content.
* **Input Schema:** Expects `topic` (string) and `output_format` (string: "summary", "bullet points", or "short report").
* **Tools Used:** `wikipedia` (Julep Integration)
* **Workflow:**
    1.  **Tool Call:** Executes the `wikipedia` tool using the input `topic` as the query.
    2.  **Prompt:** Takes the output from the Wikipedia tool and sends it, along with the original topic and desired format, to the associated Julep Agent (LLM) for processing and formatting according to the agent's instructions. The `unwrap: true` setting ensures the LLM's direct text response is the final output.
* **Task ID:** `YOUR_JULEP_TASK_ID` (Replace with the actual ID generated when the task is created via the script. Storing this might be useful but the current `main.py` creates it on startup).

## ⚙️ Setup and Running Locally

1.  **Prerequisites:**
    * Python 3.9+
    * `pip` package installer

2.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd ansuman-shukla-julep-web-search-agent
    ```

3.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    # Activate (Linux/macOS)
    source venv/bin/activate
    # Activate (Windows)
    .\venv\Scripts\activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Variables:**
    * Create a `.env` file in the project root.
    * Copy the contents of `.env.example` (if provided) or add the following:
        ```dotenv
        JULEP_API_KEY=your_actual_julep_api_key
        JULEP_AGENT_ID=your_actual_julep_agent_id # Get this after running the agent creation part of the script once
        # Add any other required keys like BRAVE_API_KEY if you switch tools
        ```
    * Replace placeholders with your actual credentials. **Never commit your `.env` file!**

6.  **Run the Application:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will be available at `http://localhost:8000`.

## 🔌 API Endpoint

### `/research`

* **Method:** `POST`
* **Description:** Submits a research topic and desired format to the Julep agent task.
* **Request Body:** (`application/json`)
    ```json
    {
      "topic": "String: The subject to research",
      "format": "String: 'summary' | 'bullet points' | 'short report'"
    }
    ```
* **Example Request (`curl`):**
    ```bash
    curl -X POST "http://localhost:8000/research" \
         -H "Content-Type: application/json" \
         -d '{
               "topic": "Theory of Relativity",
               "format": "summary"
             }'
    ```
* **Success Response:** (`application/json`)
    ```json
    {
      "result": "String: The formatted research result from the agent.",
      "status": "succeeded",
      "execution_id": "String: The Julep execution ID for tracking."
    }
    ```
* **Error Response:** Returns appropriate HTTP status codes (e.g., 422, 500, 502, 504) with a JSON body containing `{"detail": "Error message"}`.

## 🚀 Deployment (Railway)

This application is configured for deployment on Railway.app.

1.  Push your code to a GitHub/GitLab repository.
2.  Create a new project on Railway and connect it to your repository.
3.  Railway should automatically detect the `Procfile` (`web: uvicorn main:app --host 0.0.0.0 --port $PORT`) and Python environment.
4.  **Add Environment Variables** in the Railway service settings:
    * `JULEP_API_KEY`
    * `JULEP_AGENT_ID`
    * *(Any other necessary keys like `BRAVE_API_KEY` if used)*
5.  Railway will build and deploy the application.
6.  **Live API Endpoint:** `https://your-app-name.up.railway.app/research` (Replace `your-app-name` with your actual Railway service URL).

## 📚 `docs.julep.ai` Usage

The official Julep AI documentation ([docs.julep.ai](https://docs.julep.ai/)) was consulted for:

* Understanding core concepts: Agents, Tasks, Sessions, Executions, Tools.
* Agent configuration options and instruction design.
* Task definition syntax (YAML), including input schema, tools integration (Wikipedia), and workflow steps (`tool`, `prompt`).
* Using Python expressions (`$`, `_`) within task definitions.
* Python SDK usage for creating Agents, Tasks, and Executions, and for polling execution status.
* API reference for specific SDK methods and parameters.

## 🤔 Challenges (Example)

* **Task vs. Session:** Initially considered using Julep Sessions, but Tasks proved more suitable for this defined, multi-step workflow (tool call -> LLM processing) triggered by an API, rather than an ongoing conversation.
* **YAML Syntax:** Ensuring correct indentation and Python expression syntax (`$ f'...'`, accessing step outputs like `steps[0].output`) within the `search_task.yaml` required careful checking against documentation.
* **API Key Management:** Deciding how to securely provide API keys (like Brave's, if used) to the Julep Task. Using environment variables passed during application startup to modify the YAML dictionary in memory was one approach, though configuring secrets directly on the Julep Agent/Tool might be preferable if supported.
* **Output Parsing:** Understanding the exact structure of the `result.output` from a task execution, especially when the last step uses `unwrap: true`.

---

*This README provides a comprehensive guide to understanding, setting up, and using the Julep AI Research Assistant.*
