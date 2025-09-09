# CognAI – AI-Powered Gmail Assistant

## 📧 Project Description

CognAI intelligently connects with Gmail (via Descope and direct OAuth fallback), fetches and summarizes emails using Gemini LLM, and provides a conversational interface for email insights. A smart assistant to manage your inbox efficiently.

---

## 👨‍💻 Solo Developer

- **Developer**: [Your Name] (solo project)

---

## 🎯 Challenge Theme

**Theme Addressed**: Smart Productivity / AI+Productivity – enabling intelligent email workflows.

---

## 🚀 What We Built & How to Run It

### Overview

- **Authentication Flow**:

  1. **Primary**: Descope Outbound App
  2. **Fallback**: Direct Google OAuth if Descope flow fails

- **Features**:
  - 🔐 Securely fetch Gmail messages
  - 📋 Summarize email threads via Gemini LLM
  - 💬 Chat interface for natural language interactions

### 🏃‍♂️ Run Locally

#### Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate     # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

Create `backend/.env`:

```env
DESCOPE_PROJECT_ID=your_project_id
DESCOPE_MANAGEMENT_KEY=your_management_key
OUTBOUND_APP_ID=gmail
FRONTEND_ORIGIN=http://localhost:8080
GOOGLE_REDIRECT_URI=http://localhost:8000/google/callback
OAUTHLIB_INSECURE_TRANSPORT=1
```

Start server:

```bash
uvicorn app.main:app --reload --port 8000
```

#### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

**Access**: http://localhost:8080

### 📋 Usage Flow

1. Sign in via Descope
2. Click **Connect Gmail** → goes through Descope / fallback Google OAuth
3. Access summarized emails and chat interactively with your LLM assistant

---

## 🛠️ Tech Stack

### Frontend

- **React** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **shadcn/ui** - UI components
- **Descope React SDK** - Authentication
- **Axios** - HTTP client

### Backend

- **FastAPI** - Python web framework
- **Descope Python SDK** - Authentication management
- **Google OAuth** - Gmail access (google-auth, google-auth-oauthlib, google-api-python-client)

### AI/LLM

- **Gemini** - via google.generativeai SDK

---

## 🎥 Demo Video (Required)

Watch the functionality walkthrough in under 5 minutes:

[![CognAI Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://youtube.com/watch?v=YOUR_VIDEO_ID)

**[🎬 YouTube Demo Link](https://youtube.com/watch?v=YOUR_VIDEO_ID)**

---

## 📂 GitHub Repository

Access full project code and documentation here:

**[🔗 GitHub Repository](https://github.com/yourusername/cognai)**

---

## 🔮 What I'd Do with More Time

- [ ] **Persistent Sessions**: Store Gmail tokens in a secure database (persistent user sessions)
- [ ] **Email Composition**: Enable email composition and sending via LLM prompts
- [ ] **Enhanced UI**: Improve the UI with inbox categorization and notifications
- [ ] **Production Deploy**: Deploy to a secure HTTPS domain with proper OAuth support
- [ ] **Advanced AI Features**:
  - Smart email categorization
  - Priority inbox suggestions
  - Auto-reply generation
- [ ] **Multi-platform Support**: Mobile app development
- [ ] **Security Enhancements**: End-to-end encryption for sensitive data

---

## 📁 Project Structure

```
cognai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── auth/
│   │   ├── gmail/
│   │   └── llm/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Gmail API credentials
- Descope account

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/cognai.git
   cd cognai
   ```

2. **Set up backend**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Fill in your environment variables
   uvicorn app.main:app --reload --port 8000
   ```

3. **Set up frontend**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Open your browser** and navigate to `http://localhost:8080`

---

## 🤝 Contributing

This is a solo project, but contributions are welcome! Please feel free to submit a Pull Request.

---

## 📞 Support

If you have any questions or issues, please open an issue on GitHub or contact [vinitpandey2306@gmail.com].

---

**Made with ❤️ by [Vinit Pandey]**
