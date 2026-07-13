# Summative Lab: Local RAG-Powered Knowledge Assistant

## Overview

In this summative lab, you will complete a local full-stack AI application that helps users ask questions about a small approved knowledge base.

The starter app includes a React frontend, a Flask backend, starter API routes, knowledge base files, environment configuration, and TODO comments in the key backend files. Your job is to complete the backend AI workflow so the frontend can send a question, the backend can retrieve relevant context, and the app can return a source-backed answer.

You will not deploy this application. You will run it locally and focus on connecting the frontend, backend, vector database, model service, and RAG workflow.

## Scenario

Your team is building a local prototype of an internal knowledge assistant. Employees need quick answers from a small set of approved documents, such as onboarding notes, product support guidance, security expectations, and workplace FAQs.

The frontend team has already created a simple chat interface. A user can type a question and submit it. However, the backend AI workflow is incomplete. The app still needs to retrieve relevant knowledge base content, send that context to the model, and return an answer with supporting sources.

Your role is to complete the backend AI functionality so the team can review whether the prototype is useful before deciding what to improve next.

## Learning Goal

You will complete a local full-stack AI application by connecting a React frontend, Flask backend, vector database, knowledge base, and model service into a working RAG workflow that returns useful answers with supporting sources.

By completing this lab, you will:

- Complete a Flask API route that receives user questions.
- Connect the backend to a local model service.
- Store and retrieve knowledge base chunks using a vector database.
- Build a RAG workflow that uses retrieved context to generate an answer.
- Return both an answer and supporting sources to the frontend.
- Use environment variables for key configuration values.
- Document how to install, run, and check the application.

## Scope

This lab focuses on building a local RAG-powered full-stack application.

You are not required to add:

- Authentication
- Pagination
- Deployment
- A new frontend from scratch
- A large custom knowledge base
- Automated test files

When this lab asks you to test or check your work, it means you should run the app locally, try sample questions, review the output, and refine the code based on what you observe.

## Tools and Resources

You will use:

- Python 3.10+
- Flask
- React + Vite
- Node.js and npm
- Chroma or the approved local vector store included in the starter
- Ollama or another approved local model service
- Git and GitHub
- A `.env` file for configuration

Recommended Ollama models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Project Structure

```text
summative-rag-knowledge-assistant-starter/
├── client/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── styles.css
├── server/
│   ├── app.py
│   ├── config.py
│   ├── documents.py
│   ├── rag_service.py
│   ├── seed_knowledge_base.py
│   ├── vector_store.py
│   ├── requirements.txt
│   ├── Pipfile
│   ├── .env.example
│   └── knowledge_base/
│       ├── onboarding.txt
│       ├── product_support.txt
│       ├── security_guidelines.txt
│       └── workplace_faq.txt
└── README.md
```

## What Is Already Provided

The starter repository includes:

- A React frontend interface
- A Flask backend structure
- A working `/api/health` route
- A starter `/api/ask` route
- Knowledge base documents in plain text format
- A document loading and chunking helper
- Starter files for vector retrieval and RAG workflow code
- Environment variable examples
- TODO comments showing where you need to complete the implementation

## What You Need to Complete

You are responsible for completing the main backend AI workflow.

You will complete TODOs in:

- `server/app.py`
- `server/vector_store.py`
- `server/rag_service.py`

Your completed app should allow a user to:

1. Open the React frontend.
2. Type a question about the knowledge base.
3. Submit the question to the Flask backend.
4. Retrieve relevant knowledge base chunks from the vector database.
5. Send the question and retrieved context to the model service.
6. Receive a generated answer.
7. View supporting sources in the frontend.

---

## Instructions

### Task 1: Define the Problem

Start by reviewing the starter app, scenario, and provided knowledge base documents.

Identify the problem your AI assistant is designed to solve:

- Who will use this assistant?
- What kind of questions should the assistant help answer?
- What approved knowledge base content will the assistant use?
- What should a useful answer include?
- Why is a source-backed answer important for this use case?

In this README, replace the placeholder section below with a short description of the user need and the purpose of your assistant.

#### Response: Problem Definition

This assistant helps employees query approved internal knowledge base documents such as onboarding guidance, product support information, security expectations, and workplace FAQs. It is designed to answer operational questions quickly and with source-backed context so users can trust the response. A useful answer includes a clear recommendation, references to the relevant document, and metadata showing where the supporting information was retrieved.

---

### Task 2: Determine the Design

Plan how the provided frontend, Flask backend, vector database, RAG workflow, and model service will work together.

Review the starter code and identify:

- Where the frontend sends user questions
- Which backend route receives the question
- Where the RAG workflow should be completed
- Where the knowledge base files are stored
- How source information should be returned
- Which environment variables are needed

Your design should account for:

- The backend question route
- Knowledge base loading and chunking
- Vector database setup
- Retrieval of relevant chunks
- Prompt construction
- Model service connection
- JSON response format for the frontend
- Display of answers and sources in the frontend

You do not need to build a new frontend from scratch. Use the provided frontend and make only the adjustments needed to connect it to your completed backend workflow.

#### Response: Design Notes

User browser
→ React frontend submits question to `/api/ask`
→ Flask backend validates the question
→ `rag_service.answer_question` retrieves context from Chroma
→ `vector_store.retrieve_relevant_chunks` queries embeddings
→ `rag_service.build_prompt` builds a grounded prompt
→ `rag_service.call_generation_model` sends the prompt to Ollama
→ backend returns answer, sources, and metadata to frontend

The knowledge base files are stored in `server/knowledge_base`. The backend uses environment variables in `server/.env` to configure model URLs, Chroma storage, collection name, and retrieval settings.

---

### Task 3: Develop, Test, and Refine the Code

Complete the required code so the local full-stack AI assistant works from the frontend through the backend RAG workflow.

Your implementation should:

- Configure your local `.env` file using `.env.example`.
- Complete the backend route that receives a user question.
- Load the provided knowledge base documents.
- Create or update retrievable chunks in the vector database.
- Preserve source information for returned chunks.
- Retrieve relevant context based on the user’s question.
- Build a prompt using the retrieved context.
- Send the prompt to the model service.
- Return a JSON response with:
  - The generated answer
  - Supporting sources
  - Any relevant metadata included in the starter structure
- Connect the backend response to the frontend display.

After developing the core workflow, run the application locally and try at least three sample questions.

For each sample question, check:

- Does the frontend submit the question successfully?
- Does the backend return a response?
- Is the answer relevant to the question?
- Does the response include useful supporting sources?
- Are there errors in the terminal or browser console?
- Does anything need to be refined for clarity, relevance, or reliability?

Refine your code based on what you find.

#### Response: Sample Questions and Observations

| Sample Question | Was the Answer Relevant? | Were Useful Sources Returned? | Notes |
|---|---|---|---|
| What should employees do if they receive a suspicious email? | Pending model service | Pending model service | The backend retrieval path is implemented; full generation requires Ollama running. |
| Why are source-backed answers important? | Pending model service | Pending model service | Source metadata is returned from retrieved chunks once the model is available. |
| What should I do if I cannot log into the product dashboard? | Pending model service | Pending model service | Product support content is available in `product_support.txt`; answer generation is blocked by local service availability. |

---

### Task 4: Document and Maintain

Prepare your project for review and submission.

Your GitHub repository should include:

- Completed backend question route
- Completed RAG workflow
- Vector database setup or setup instructions
- Provided knowledge base documents
- Working frontend/backend connection
- `.env.example`
- Dependency files
- README
- Meaningful Git commit history

Your README should include:

- Project title
- Project description
- User need or scenario
- Installation instructions
- Run instructions
- Required environment variables
- API route descriptions
- Description of the RAG workflow
- At least three sample questions you tried
- Notes about whether the answers and sources were relevant
- Known limitations or future improvements

Before submitting:

1. Save your work with Git.
2. Commit your changes with meaningful commit messages.
3. Push your final work to GitHub.
4. Submit your GitHub repository link in Canvas.

---

## Setup Instructions

### 1. Start Ollama

In a terminal, confirm Ollama is running and pull the recommended models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
ollama run llama3.2 "Reply with one short sentence."
```

### 2. Set Up the Flask Backend

From the project root:

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Complete the Backend TODOs

Open these files and complete the TODO comments:

- `server/app.py`
- `server/vector_store.py`
- `server/rag_service.py`

The app will not fully work until these TODOs are completed.

### 4. Seed the Knowledge Base

After completing the vector store TODOs, run:

```bash
python seed_knowledge_base.py
```

This script loads the provided knowledge base files, chunks the text, creates embeddings, and stores the chunks in the vector database.

### 5. Run the Flask Backend

```bash
flask --app app run --debug --port 5555
```

You should be able to visit:

```text
http://localhost:5555/api/health
```

Expected response:

```json
{
  "message": "Backend is running.",
  "status": "ok"
}
```

### 6. Set Up and Run the React Frontend

Open a second terminal from the project root:

```bash
cd client
npm install
npm run dev
```

Open the local frontend URL shown in your terminal. It is usually:

```text
http://localhost:5173
```

---

## API Routes

### GET `/api/health`

Confirms that the backend is running.

Expected response:

```json
{
  "status": "ok",
  "message": "Backend is running."
}
```

### POST `/api/ask`

Receives a user question and returns an answer with sources.

Expected request body:

```json
{
  "question": "What should I do if I cannot log into the product dashboard?"
}
```

Expected response format:

```json
{
  "answer": "A helpful answer grounded in the knowledge base.",
  "sources": [
    {
      "title": "Product Support Guide",
      "source": "product_support.txt",
      "chunk_index": 0,
      "excerpt": "Relevant source excerpt..."
    }
  ]
}
```

---

## Environment Variables

Create your local `.env` file from `server/.env.example`.

| Variable | Purpose |
|---|---|
| `OLLAMA_BASE_URL` | URL for the local model service |
| `GENERATION_MODEL` | Model used to generate answers |
| `EMBEDDING_MODEL` | Model used to create embeddings |
| `CHROMA_PATH` | Local folder where Chroma stores vector data |
| `COLLECTION_NAME` | Name of the vector collection |
| `KNOWLEDGE_BASE_PATH` | Folder containing source documents |
| `TOP_K` | Number of chunks to retrieve |
| `TEMPERATURE` | Controls response variation |
| `CLIENT_ORIGIN` | Local frontend origin allowed by the backend |

Example values:

```text
OLLAMA_BASE_URL=http://localhost:11434
GENERATION_MODEL=llama3.2
EMBEDDING_MODEL=nomic-embed-text
CHROMA_PATH=./chroma_db
COLLECTION_NAME=knowledge_assistant
KNOWLEDGE_BASE_PATH=./knowledge_base
TOP_K=3
TEMPERATURE=0.2
CLIENT_ORIGIN=http://localhost:5173
```

---

## Knowledge Base Files

The starter app includes these source files:

- `server/knowledge_base/onboarding.txt`
- `server/knowledge_base/product_support.txt`
- `server/knowledge_base/security_guidelines.txt`
- `server/knowledge_base/workplace_faq.txt`

These files are the approved source content for the assistant. The RAG workflow should retrieve from these files and return sources that help users understand where the answer came from.

You may make small edits to the source files if allowed or instructed to by your instructor.

---

## RAG Workflow Description

The frontend sends the user's question to the Flask `/api/ask` route. The backend validates the request and forwards the question to `server/rag_service.py`. The RAG service retrieves relevant document chunks from the Chroma vector database using `server/vector_store.py`. The retrieved chunks are combined into a prompt that asks the model to answer only from the provided context. The prompt is sent to the local Ollama generation service. The backend returns the generated answer along with supporting source metadata and excerpt information to the frontend.

---

## Sample Questions

The following sample questions were prepared for manual verification. Full model response validation is pending because the local Ollama service was not available during this review.

| Sample Question | Was the Answer Relevant? | Were Useful Sources Returned? | Notes |
|---|---|---|---|
| What should employees do if they receive a suspicious email? | Pending model service | Pending model service | The backend retrieval path is implemented; full generation requires Ollama running. |
| Why are source-backed answers important? | Pending model service | Pending model service | Source metadata is returned from retrieved chunks once the model is available. |
| What should I do if I cannot log into the product dashboard? | Pending model service | Pending model service | Product support content is available in `product_support.txt`; answer generation is blocked by local service availability. |

## Known Limitations or Future Improvements

- The app requires a local Ollama model service to be installed and running at `OLLAMA_BASE_URL` for embeddings and generation.
- The current manual verification is limited by the unavailable local model service; once Ollama is running, the prompt generation and source-backed answer flow can be validated end to end.
- Future improvements could include better chunking for longer documents, richer source attribution in the frontend, and caching or seeding the vector store ahead of time.
- Add user feedback for helpful or unhelpful answers.
- Improve prompt instructions for unsupported questions.
- Expand the knowledge base with additional approved documents.
- Improve error handling when the model service is unavailable.

---

## Submission Checklist

Before submitting, confirm that:

- The backend starts successfully.
- The frontend loads successfully.
- The frontend can submit a question to the backend.
- The backend retrieves relevant context from the vector database.
- The model service returns an answer.
- The answer is displayed in the frontend.
- Supporting sources are displayed in the frontend.
- Your `.env.example` is included.
- Your actual `.env` file is not committed.
- Your README is updated with required sections.
- Your Git commits have meaningful messages.
- Your final work is pushed to GitHub.

Submit your public GitHub repository link in Canvas.