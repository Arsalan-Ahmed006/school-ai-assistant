# 🎓 School AI Assistant

> **A grounded, secure, multi-agent AI assistant for modern schools built with Google Agent Development Kit (ADK) 2.3 and Gemini 2.5 Flash.**

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Google ADK 2.3.0](https://img.shields.io/badge/Google%20ADK-2.3.0-4285F4?style=flat-square&logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Gemini 2.5 Flash](https://img.shields.io/badge/Gemini-2.5%20Flash-8E24AA?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Apache 2.0 License](https://img.shields.io/badge/License-Apache%202.0-green?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://img.shields.io/badge/Tests-8%20Passing-success?style=flat-square)](https://pytest.org/)

### 🏆 Google × Kaggle AI Agents Intensive Capstone Project (2026)

### 👥 Team

**👨‍💻 Arsalan Ahmed (Team Lead)**

**👨‍💻 Manzar Rasool**

---

Routes parent enquiries and teacher lesson-planning requests to specialist AI agents using native Google ADK routing, grounded PDF retrieval (RAG), secure tool calling, and layered security guardrails.

</div>

---

# 🔗 Quick Links

| Resource | Link |
|----------|------|
| 🎥 Project Demonstration | https://youtu.be/e-SdcYphtFI |
| 💻 GitHub Repository | https://github.com/Arsalan-Ahmed006/school-ai-assistant |
| 🏆 Kaggle Competition | https://www.kaggle.com/competitions/vibecoding-agents-capstone-project |

---

# 🎥 Project Demo

📺 **Watch the complete project walkthrough on YouTube**

https://youtu.be/e-SdcYphtFI

---

### 📥 Repository Demo Video

If you'd like to download the demonstration video directly from this repository:

[▶️ Capstone-gif.mp4](documents/GIF/Capstone-gif.mp4)

---

# 📖 About this Project

Schools frequently receive repetitive parent enquiries while teachers spend valuable time preparing structured lesson plans.

Instead of building a single monolithic chatbot, this project demonstrates how **multiple specialized AI agents** collaborate safely inside one intelligent educational assistant.

The system contains:

- 👨‍👩‍👧 Parent FAQ Agent
- 👩‍🏫 Teacher Lesson Planning Agent
- 🧠 Google ADK Root Orchestrator
- 📄 Grounded PDF Knowledge Retrieval (RAG)
- 🔒 Regex-based Security Guardrails
- 🛠️ Native Tool Calling
- ⚡ FastAPI Backend

Developed as part of the **Google × Kaggle AI Agents Intensive Capstone**, this project demonstrates the core concepts taught throughout the course, including:

- ✅ Multi-Agent Systems
- ✅ Google Agent Development Kit (ADK)
- ✅ Tool Calling
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Gemini 2.5 Flash
- ✅ Security Guardrails

---

# 📸 Interface Walkthrough

The following screenshots demonstrate the application's interface, intelligent routing, specialist agents, and security mechanisms.

> **Note:** All screenshots were captured directly from the Google ADK Playground while interacting with the live multi-agent system.

---

## 1️⃣ Application Interface

The Google ADK Playground serves as the primary interface for interacting with the School AI Assistant.

![Application Interface](documents/screenshots/ScreenSHot-UI.png)

---

## 2️⃣ Initial Greeting

The assistant welcomes users and intelligently determines whether the request belongs to the Parent FAQ Agent or the Teacher Lesson Planning Agent.

![Welcome Screen](documents/screenshots/Hello-prompt.png)

---

## 3️⃣ Parent FAQ Agent

Example showing the Parent Specialist Agent answering a school-related enquiry using grounded school documents retrieved through RAG.

![Parent FAQ](documents/screenshots/ScreenShot-PARENT-FAQ.png)

---

### 4️⃣ Teacher Lesson Planning Agent

The Teacher Specialist Agent receives a lesson planning request and prepares a structured lesson using the curriculum documents.

![Teacher Prompt](documents/screenshots/Teacher-prompt.png)

> **Generated Lesson Plan**

The Teacher Agent generates a structured lesson plan grounded in curriculum guidance and educational best practices.

![Generated Lesson Plan](documents/screenshots/LessonPlan.png)

---

## 5️⃣ Security Guardrails

Prompt injection and jailbreak attempts are intercepted before any request reaches Gemini.

![Guardrails](documents/screenshots/Guardrails.png)

---

## 🎥 Demonstration Video

📺 YouTube

https://youtu.be/e-SdcYphtFI

or download directly:

[▶️ Capstone-gif.mp4](documents/GIF/Capstone-gif.mp4)

---

# 👥 Team

This project was developed as part of the **Google × Kaggle AI Agents Intensive Capstone Project (2026).**

| Role | Name |
|------|------|
| 🏆 Team Lead | **Arsalan Ahmed** |
| 👨‍💻 Team Member | **Manzar Rasool** |

---

# 🛠 Responsibilities

## 👨‍💻 Arsalan Ahmed (Team Lead)

- Project planning and architecture
- Multi-Agent System design
- Google ADK implementation
- Parent FAQ Agent
- Tool Calling implementation
- Retrieval-Augmented Generation (RAG)
- FastAPI backend integration
- GitHub repository management
- Video demonstration
- Documentation review

---

## 👨‍💻 Manzar Rasool

- Project planning and architecture
- Multi-Agent System design
- Teacher Lesson Planning Agent
- Security Guardrails
- Documentation
- Testing and debugging
- Feature validation
- UI testing
- Presentation preparation


---

# ✨ Key Features

The School AI Assistant demonstrates the core concepts taught throughout Google's **5-Day AI Agents Intensive Course** by combining multiple specialized AI agents, grounded knowledge retrieval, secure tool execution, and production-ready backend architecture.

---

# 🤖 Multi-Agent Architecture

Instead of relying on one large chatbot, the application is built around a **specialized multi-agent architecture** using the **Google Agent Development Kit (ADK)**.

A central routing agent analyzes every incoming request before delegating it to the most appropriate specialist agent.

Current specialist agents include:

- 👨‍👩‍👧 Parent FAQ Agent
- 👩‍🏫 Teacher Lesson Planning Agent

This modular architecture improves:

- Higher response accuracy
- Better maintainability
- Easier future expansion
- Stronger security boundaries
- Cleaner separation of responsibilities

---

# 👨‍👩‍👧 Parent FAQ Agent

The Parent FAQ Agent is responsible for answering common school-related questions using grounded school policy documents.

Example queries include:

- School timings
- Admission procedure
- Uniform policy
- Fee structure
- Attendance policy
- Examination schedule
- General school information

Instead of generating answers purely from the language model, the agent retrieves relevant information from school documents before responding.

This significantly reduces hallucinations while ensuring answers remain consistent with school policies.

---

# 👩‍🏫 Teacher Lesson Planning Agent

The Teacher Lesson Planning Agent assists teachers by automatically generating structured lesson plans using curriculum documents.

Capabilities include:

- Topic-based lesson planning
- Learning objectives
- Classroom activities
- Teaching methodology
- Assessment strategy
- Homework suggestions
- Learning outcomes

Rather than relying solely on Gemini's internal knowledge, lesson plans are grounded using curriculum resources retrieved through RAG.

---

# 🔍 Retrieval-Augmented Generation (RAG)

To improve factual accuracy, the assistant uses **Retrieval-Augmented Generation (RAG)**.

Before Gemini generates a response, the relevant school documents are retrieved and supplied as context.

Benefits include:

- Grounded responses
- Reduced hallucinations
- School-specific information
- Higher factual accuracy
- More trustworthy educational responses

This allows the assistant to answer questions using the school's own documentation instead of relying exclusively on pretrained knowledge.

---

# 🛠 Tool Calling

The project demonstrates native **Tool Calling**, one of the core concepts covered during the Google × Kaggle AI Agents Intensive Course.

Specialized tools are invoked dynamically during execution, including:

- Knowledge Retrieval
- Prompt Validation
- Lesson Plan Formatting
- Response Formatting

Separating these responsibilities into reusable tools keeps the system modular, scalable, and easier to maintain.

---

# 🛡 Security Guardrails

Security is enforced before any request reaches Gemini.

The assistant automatically detects and blocks:

- Prompt Injection
- Jailbreak Attempts
- Unsafe Instructions
- Irrelevant Requests
- Malicious Inputs

These layered security guardrails ensure that the assistant remains focused on educational tasks while protecting the underlying model from unsafe interactions.

---

# ⚡ Google Gemini 2.5 Flash

The School AI Assistant is powered by **Google Gemini 2.5 Flash**.

The model provides:

- Fast response generation
- Strong reasoning capabilities
- Reliable instruction following
- High-quality educational content
- Efficient tool orchestration

Gemini 2.5 Flash was selected because it offers an excellent balance between performance, reasoning quality, latency, and cost for production-ready educational assistants.

---

# 🚀 FastAPI Backend

The assistant is deployed through a **FastAPI** backend, making it easy to integrate with future web applications, mobile applications, or external services.

Benefits include:

- REST API support
- Streaming responses
- Production-ready deployment
- Easy frontend integration
- Scalable architecture

This separation between the backend API and the AI agents makes the project easier to extend and maintain in real-world deployments.

---
# 🏗️ System Architecture

The School AI Assistant follows a modular **multi-agent architecture** built with the **Google Agent Development Kit (ADK)**.

Instead of relying on a single AI assistant, incoming requests are intelligently classified and routed to specialized agents responsible for different educational tasks.

This architecture improves scalability, maintainability, response quality, and security while demonstrating modern AI agent orchestration principles taught during the **Google × Kaggle AI Agents Intensive Course**.

---

## Request Flow

```text
User
        │
        ▼
Input Validation & Security Guardrails
        │
        ▼
Request Classifier
        │
 ┌──────┴────────┐
 ▼               ▼
Parent Agent   Teacher Agent
 │               │
 └──────┬────────┘
        ▼
Tool Calling
        │
        ▼
Knowledge Retrieval (RAG)
        │
        ▼
Gemini 2.5 Flash
        │
        ▼
Formatted Response
        │
        ▼
User
```

---

## Architecture Highlights

- ✅ Google ADK Multi-Agent Orchestration
- ✅ Intelligent Request Routing
- ✅ Parent FAQ Specialist Agent
- ✅ Teacher Lesson Planning Specialist Agent
- ✅ Native Tool Calling
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Gemini 2.5 Flash Reasoning Engine
- ✅ Layered Security Guardrails
- ✅ FastAPI Backend Integration

---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Agent Framework | Google Agent Development Kit (ADK) |
| AI Model | Gemini 2.5 Flash |
| Backend | FastAPI |
| Programming Language | Python 3.11+ |
| Knowledge Retrieval | Retrieval-Augmented Generation (RAG) |
| Agent Architecture | Multi-Agent System |
| Security | Input Validation & Guardrails |
| Tool Calling | Custom Python Tools |
| Version Control | Git & GitHub |
| Documentation | Markdown |
| Presentation | Microsoft PowerPoint |
| Demo Video | YouTube (Unlisted) |

---

# 🎯 Course Concepts Demonstrated

This capstone project demonstrates the major concepts covered during Google's **5-Day AI Agents Intensive Course**.

| Concept | Status |
|---------|:------:|
| ✅ Google Agent Development Kit (ADK) | ✔ |
| ✅ Multi-Agent Systems | ✔ |
| ✅ Tool Calling | ✔ |
| ✅ Retrieval-Augmented Generation (RAG) | ✔ |
| ✅ Gemini 2.5 Flash | ✔ |
| ✅ Security Guardrails | ✔ |
| ✅ FastAPI Integration | ✔ |

---

# 🚀 Quick Start

Get the School AI Assistant running locally in just a few minutes.

---

## Prerequisites

Before starting, install the following software.

| Software | Version |
|----------|---------|
| Python | 3.11+ |
| Google Agent Development Kit | Latest |
| uv | Latest |
| Git | Latest |

You'll also need a **Google AI Studio API Key**.

---

## 1. Clone the Repository

```bash
git clone https://github.com/Arsalan-Ahmed006/school-ai-assistant.git

cd school-ai-assistant
```

> **Note:** Replace the repository name if you publish it under a different name.

---

## 2. Install Dependencies

Using ADK

```bash
agents-cli install
```

or using uv

```bash
uv sync
```

---

## 3. Configure Environment Variables

Create:

```text
app/.env
```

Add:

```env
GOOGLE_API_KEY=YOUR_API_KEY

GOOGLE_GENAI_MODEL=gemini-2.5-flash
```

---

## 4. Launch the ADK Playground

```bash
agents-cli playground
```

Open your browser:

```text
http://localhost:8000
```

---

# ▶ Running the Project

The School AI Assistant can be used in three different ways.

---

## 1. Google ADK Playground

Recommended during development.

```bash
agents-cli playground
```

---

## 2. Terminal Interface

Run prompts directly from the terminal.

Example:

```bash
agents-cli run "What is the admission procedure?"
```

or

```bash
agents-cli run "Create a Grade 5 lesson plan on fractions."
```

---

## 3. FastAPI Server

Launch the backend API.

```bash
uv run app/fast_api_app.py
```

The FastAPI server exposes the assistant for integration with web or mobile applications.

---

# 🧪 Running Tests

Execute all unit tests.

```bash
pytest
```

or

```bash
pytest tests/unit
```

---
# 📂 Repository Structure

```text
school-ai-assistant/
│
├── app/
│   ├── agent.py
│   ├── agents/
│   ├── tools/
│   ├── app_utils/
│   └── fast_api_app.py
│
├── knowledge/
│   ├── parents/
│   └── teachers/
│
├── documents/
│   ├── screenshots/
│   └── GIF/
│       └── Capstone-gif.mp4
│
├── tests/
│
├── README.md
│
└── pyproject.toml
```

---

# ⭐ Project Highlights

This capstone demonstrates the complete workflow of a secure, production-ready educational AI assistant using Google's latest AI agent technologies.

✔ Google Agent Development Kit (ADK)

✔ Multi-Agent Architecture

✔ Intelligent Request Routing

✔ Parent FAQ Specialist Agent

✔ Teacher Lesson Planning Specialist Agent

✔ Native Tool Calling

✔ Retrieval-Augmented Generation (RAG)

✔ Gemini 2.5 Flash

✔ Layered Security Guardrails

✔ FastAPI Backend

✔ Modular Python Architecture

✔ Production-Ready Design

✔ Unit Testing

✔ Grounded Educational Responses

---

# 📈 Future Improvements

The current implementation focuses on demonstrating the concepts taught during the Google × Kaggle AI Agents Intensive Course.

Potential future enhancements include:

- 🌐 Web-based frontend interface
- 📱 Mobile application integration
- 👨‍🎓 Student Assistant Agent
- 📅 School Calendar Agent
- 📊 Teacher Analytics Dashboard
- 🗄️ Database-backed knowledge storage
- 🔐 User authentication and authorization
- ☁️ Cloud deployment on Google Cloud
- 🔊 Voice interaction support
- 🌍 Multi-language support

---

# 🏆 Google × Kaggle AI Agents Intensive Capstone

This project was created as the final submission for the **Google × Kaggle AI Agents Intensive Capstone Project (2026)**.

The objective of this capstone was to apply the concepts learned throughout the intensive course by building a real-world AI agent capable of solving practical problems using Google's Agent Development Kit.

The School AI Assistant demonstrates all major concepts covered throughout the course, including:

- Google ADK
- Multi-Agent Systems
- Tool Calling
- Retrieval-Augmented Generation (RAG)
- Gemini 2.5 Flash
- Security Guardrails
- FastAPI Integration

---

# 👥 Team

| Name | Role |
|------|------|
| **Arsalan Ahmed** | Team Lead |
| **Manzar Rasool** | Team Member |

---

# 🔗 Project Links

### 🎥 Project Demonstration

https://youtu.be/e-SdcYphtFI

---

### 💻 GitHub Repository
https://github.com/Arsalan-Ahmed006/school-ai-assistant

> 
---

### 🏆 Kaggle Competition

https://www.kaggle.com/competitions/vibecoding-agents-capstone-project
---

# 🙏 Acknowledgements

We would like to thank **Google** and **Kaggle** for organizing the **5-Day AI Agents Intensive Course** and providing the opportunity to apply cutting-edge AI agent concepts through this capstone project.

Special thanks to the teams behind:

- Google Agent Development Kit (ADK)
- Google Gemini
- FastAPI
- Python
- Google AI Studio

for making modern AI application development more accessible.

---

# 📄 License

This project is released under the **Apache 2.0 License**.

---

<div align="center">

## ⭐ If you found this project interesting, please consider giving it a star!

### Built with ❤️ using Google ADK, Gemini 2.5 Flash, FastAPI, and Python.

**Google × Kaggle AI Agents Intensive Capstone Project (2026)**

</div>