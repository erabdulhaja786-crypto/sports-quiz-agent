# 🏆 AI-Powered Sports Quiz Generator

An AI-powered sports quiz generation application that combines **Retrieval-Augmented Generation (RAG)**, vector search, and live web search to create engaging sports quizzes at different difficulty levels.

**Generate a quiz. Challenge your knowledge. Enter the arena.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/AI-Groq-orange" alt="Groq">
  <img src="https://img.shields.io/badge/RAG-Enabled-7C3AED" alt="RAG">
  <img src="https://img.shields.io/badge/Vector%20Database-ChromaDB-00A67E" alt="ChromaDB">
</p>

## 📌 Overview

The AI-Powered Sports Quiz Generator creates sports quizzes based on a selected sport and difficulty level. It combines information retrieved from a knowledge base with web search results to provide relevant context for AI-generated questions.

The application uses a Streamlit interface, a Groq-compatible language model, ChromaDB for vector storage, and web search to support quiz generation.

## ✨ Features

- **AI-Powered Quiz Generation:** Generate quizzes using a language model.
- **RAG Pipeline:** Retrieve relevant information to provide context for quiz generation.
- **Vector Database:** Store and retrieve knowledge using ChromaDB.
- **Web Search Integration:** Gather additional sports information from the web.
- **Multiple Sports:** Choose Cricket, Football, or Badminton.
- **Difficulty Levels:** Select Easy, Medium, or Hard.
- **Interactive Web Interface:** Use the application through Streamlit.
- **Download Quizzes:** Save generated quizzes as text files.
- **Context Inspection:** Review the retrieved context used during generation.
- **Custom Dark Theme:** A sports-arena-inspired interface.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Groq API | Language model inference |
| LangChain (if used in the implementation) | LLM and retrieval integration |
| ChromaDB | Vector database |
| DuckDuckGo Search (if used in the implementation) | Web search |
| HTML and CSS | Interface styling |
| Git and GitHub | Version control and source hosting |
| Streamlit Community Cloud | Application deployment |

## 🏗️ Application Architecture

```text
User
  |
  v
Streamlit Web Interface
  |
  v
Select Sport and Difficulty
  |
  v
Quiz Generation Pipeline
  |
  +----------------------+
  |                      |
  v                      v
ChromaDB Retrieval    Web Search
  |                      |
  +----------+-----------+
             |
             v
      Relevant Context
             |
             v
        Groq LLM
             |
             v
      Generated Quiz
             |
       +-----+------+
       |            |
       v            v
  Display Quiz   Download Quiz
             |
             v
     Inspect RAG Context
```

## 📂 Project Structure

```text
sports-quiz-agent/
│
├── app.py
├── style.css
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── config.toml
│
└── src/
    ├── __init__.py
    ├── generator.py
    ├── database.py
    └── web_search.py
```

*Note: Your repository may contain additional files depending on your implementation.*

## ⚙️ How It Works

1. **User Input:** The user selects a sport and difficulty level.
2. **Knowledge Retrieval:** The application retrieves relevant information from the ChromaDB knowledge base.
3. **Web Search:** The search component obtains additional information when configured.
4. **Context Preparation:** Retrieved information is passed to the quiz-generation pipeline.
5. **AI Generation:** The configured Groq model generates the quiz.
6. **Quiz Display:** The application presents the generated content in Streamlit.
7. **Download and Inspection:** The user can download the quiz and inspect the retrieved context.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/erabdulhaja786-crypto/sports-quiz-agent.git
cd sports-quiz-agent
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root if your implementation loads environment variables from it:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_supported_groq_model
```

Replace the placeholders with your actual credentials and a model supported by your Groq account.

**Security:** Never commit `.env` files, API keys, or other secrets to GitHub.

### 5. Start the application

```bash
streamlit run app.py
```

The application will provide a local URL in your terminal, usually `http://localhost:8501`.

## ☁️ Deployment

The application can be deployed using Streamlit Community Cloud.

1. Push the project to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create an app and select your repository.
4. Set the main file path to `app.py`.
5. Add the required credentials in the app's **Secrets** settings.

Example secrets configuration:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
GROQ_MODEL = "your_supported_groq_model"
```

6. Deploy the application.

Use the exact model name and configuration expected by your `src/generator.py` implementation.

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used to access Groq |
| `GROQ_MODEL` | Language model identifier, if configurable in your code |

Keep your credentials private. If an API key is accidentally exposed, revoke it and generate a replacement.

## 🧪 Example Usage

1. Open the Sports Quiz Arena.
2. Select **Cricket**, **Football**, or **Badminton**.
3. Choose **Easy**, **Medium**, or **Hard**.
4. Click **Generate Fresh Quiz**.
5. Review the generated quiz.
6. Download the quiz or inspect the RAG context.

## 🎯 Project Objectives

- Apply Retrieval-Augmented Generation to a practical use case.
- Integrate an LLM API into a Python application.
- Use a vector database for semantic retrieval.
- Combine retrieved knowledge with web search.
- Build and deploy an interactive AI application.
- Demonstrate practical skills in AI engineering and application development.

## 🔮 Future Enhancements

- Add more sports and specialized quiz categories.
- Present questions as interactive multiple-choice quizzes.
- Track user scores and performance.
- Add user accounts and quiz history.
- Introduce source links and citations for factual verification.
- Add automated tests and retrieval-quality evaluation.
- Improve error handling, caching, and API usage monitoring.

## 👨‍💻 Author

**Abdul Rahman**  
Aspiring AI Engineer

- **GitHub:** [erabdulhaja786-crypto](https://github.com/erabdulhaja786-crypto)
- **Project Repository:** [AI-Powered Sports Quiz Generator](https://github.com/erabdulhaja786-crypto/sports-quiz-agent)

## 📄 License

Choose a license before distributing this project. For an open-source release, you can add a `LICENSE` file using a license such as the MIT License, provided its terms suit your intended use.

---

<p align="center">
  <b>Built with Python, RAG, vector search, and generative AI.</b>
</p>
