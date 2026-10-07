# 🏥 VinCare Hospital Information Assistant

A lightweight **RAG-based hospital information assistant** built with **Python, Streamlit, Google Gemini, CSV data, and PDF-based hospital policies**.

The assistant helps users quickly find general information about VinCare Hospital, including doctors, departments, schedules, contact numbers, and hospital policies.

> ⚠️ This project is designed for **hospital information retrieval only**. It does not provide medical diagnosis, prescriptions, treatment recommendations, or medical-test interpretation.

---

## 🚀 Live Demo

**Coming Soon**

---

## ✨ Features

- 🏥 Hospital information and operating hours
- 👨‍⚕️ Doctor directory
- 🏢 Department information
- 🗓️ Doctor schedules
- 📞 Hospital contact numbers
- 📜 Hospital policy information
- 🔎 Retrieval-Augmented Generation (RAG)
- 🤖 Gemini-powered natural language responses
- 🛡️ Basic medical-safety filtering
- 📚 Source references for retrieved information
- ☁️ Streamlit Community Cloud deployment

---

## 🧠 How It Works

The application follows a simple RAG pipeline:

```text
User Question
      ↓
Streamlit Interface
      ↓
Safety Check
      ↓
Intent Detection
      ↓
Hospital Data Retrieval
   ↙          ↘
CSV Files    Policy PDF
      ↓
Relevant Context
      ↓
Google Gemini
      ↓
Grounded Answer
      ↓
Sources
```

The system retrieves relevant hospital information before sending the context to Gemini. This helps reduce hallucinations and keeps responses grounded in the provided hospital data.

---

## 📂 Project Structure

```text
hospital-information-assistant/
│
├── data/
│   ├── hospital_info.csv
│   ├── departments.csv
│   ├── doctors.csv
│   ├── doctor_schedule.csv
│   └── contacts.csv
│
├── policy/
│   └── VinCare_Hospital_Policies.pdf
│
├── app.py
├── rag.py
├── safety.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| Google Gemini | Natural language generation |
| Pandas | CSV data processing |
| PyPDF | PDF extraction |
| python-dotenv | Environment variable management |
| RAG | Grounded information retrieval |

---

## 🔍 Supported Questions

The assistant can answer questions such as:

```text
What departments are available?

List all doctors.

Who are the cardiologists?

What is Dr. Arjun Mehta's schedule?

What is the emergency phone number?

What are the hospital timings?

What are the appointment rules?

What are the hospital policies?
```

---

## 🛡️ Safety

The assistant intentionally does **not** provide:

- Medical diagnosis
- Prescription recommendations
- Medication advice
- Treatment recommendations
- Medical-test interpretation

For example, questions such as:

```text
What medicine should I take?

Do I have diabetes?

What does my blood test mean?

What treatment should I take?
```

are redirected toward professional medical consultation.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/encrypt2004/hospital-information-assistant1.git
```

### 2. Move into the project

```bash
cd hospital-information-assistant1
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

> ⚠️ Never commit your `.env` file or expose your API key publicly.

### 6. Run the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## ☁️ Deployment

This project can be deployed using **Streamlit Community Cloud**.

Deployment flow:

```text
GitHub Repository
       ↓
Streamlit Community Cloud
       ↓
Select main branch
       ↓
Select app.py
       ↓
Add GEMINI_API_KEY as a Secret
       ↓
Deploy
```

The Gemini API key should be added through Streamlit's **Secrets** settings instead of being committed to GitHub.

---

## 📊 Data Sources

The project uses fictional training data for **VinCare Multispeciality Hospital**.

The information is stored in:

- `hospital_info.csv`
- `departments.csv`
- `doctors.csv`
- `doctor_schedule.csv`
- `contacts.csv`
- `VinCare_Hospital_Policies.pdf`

The dataset is intended for demonstration and educational purposes.

---

## 🎯 Project Goals

This project demonstrates how a simple RAG application can combine:

- Structured data retrieval
- PDF document retrieval
- Intent detection
- LLM-based answer generation
- Safety filtering
- Source attribution
- Streamlit deployment

The focus is on building a **simple and understandable RAG architecture** rather than over-engineering the system with unnecessary agents or complex orchestration.

---

## 🔮 Future Improvements

- Semantic/vector search
- Embedding-based retrieval
- LangChain integration
- LangGraph-based workflows
- Appointment booking integration
- Real-time doctor availability
- Authentication
- Hospital database integration
- Multilingual support
- Better query understanding
- Conversation-aware follow-up questions

---

## 👨‍💻 Author

**Sudhanshu Kumar**

B.Tech — Electronics & Communication Engineering  
Birla Institute of Technology, Mesra

---

## 📄 Disclaimer

This project is an educational/demo application using fictional hospital data.

It should not be used for real medical decisions, diagnosis, prescriptions, emergency medical advice, or patient care.