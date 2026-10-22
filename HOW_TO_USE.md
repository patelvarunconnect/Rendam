# 📘 Varun ke AI Projects — Poori Guide (Hinglish)

Is folder mein 4 ready-to-run projects hain:

| # | Project | Folder | API key chahiye? |
|---|---|---|---|
| 1 | 🎓 AI Study Chatbot | `ai-study-chatbot` | Haan (free Groq key) |
| 2 | 📄 AI Resume Analyzer | `ai-resume-analyzer` | Haan (free Groq key) |
| 3 | 📚 Chat with PDF (RAG) | `chat-with-pdf` | Haan (free Groq key) |
| 4 | 📊 Review Sentiment Analysis | `review-sentiment-analysis` | Nahi |

---

## Step 1: Python install karo (sirf ek baar)

1. <https://www.python.org/downloads/> se **Python 3.11 ya 3.12** download karo.
2. Install karte waqt sabse neeche **"Add python.exe to PATH"** pe ✅ tick zaroor lagao.
3. Check karne ke liye Command Prompt kholo aur likho:
   ```
   python --version
   ```
   `Python 3.12.x` jaisa kuch aana chahiye.

## Step 2: Free Groq API key lo (project 1, 2, 3 ke liye)

1. <https://console.groq.com/keys> pe jao aur Google ya email se free account banao / login karo.
2. **Create API key** pe click karo aur key copy kar lo.
3. ⚠️ Ye key kisi ko mat dikhana aur GitHub pe kabhi upload mat karna.

## Step 3: Key project mein daalo

Har project folder (1, 2, 3) mein:
1. `.env.example` file ki copy banao aur uska naam **`.env`** rakho.
2. `.env` ko Notepad se kholo aur `paste-your-key-here` ki jagah apni key paste karo:
   ```
   GROQ_API_KEY=gsk_...apni-key...
   ```
3. Save karo.

> `.env` na bhi banao to chalega — app khulne ke baad left sidebar mein key paste kar sakte ho.

## Step 4: Project chalao

**Sabse aasaan tareeka:** project folder mein **`run.bat`** pe double-click karo.
- Pehli baar 2–5 minute lagenge (packages install honge).
- Browser mein app apne aap khul jaayega: <http://localhost:8501>
- Band karne ke liye black window mein `Ctrl + C` dabao.

**Manual tareeka (Command Prompt se):**
```
cd ai-study-chatbot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Step 5: GitHub pe upload karo

> Har project ko **alag repository** banake upload karo — interviewer ko har project alag link pe dikhta hai.
> `.gitignore` file pehle se hai, isliye tumhari `.env` (API key) upload **nahi** hogi.

### Tareeka A: Website se (bina command ke, sabse aasaan)

1. <https://github.com> pe account banao (username professional rakho, jaise `varunpatel-dev`).
2. Upar right mein **+ → New repository** pe click karo.
3. Repository name: `ai-study-chatbot` (project folder ka naam), **Public** chuno,
   "Add a README" pe tick **mat** lagao → **Create repository**.
4. Agle page pe **"uploading an existing file"** link pe click karo.
5. Project folder ki **saari files aur folders** drag-and-drop karo.
   ⚠️ **`.env` file aur `.venv` folder ko mat daalna.**
   (Website pe `.streamlit` jaise dot wale folder kabhi-kabhi upload nahi hote — koi baat nahi, app bina usse bhi chalega.)
6. Neeche **Commit changes** pe click karo. Ho gaya! ✅
7. Baaki 3 projects ke liye yahi repeat karo.

### Tareeka B: Git commands se (professional tareeka)

1. <https://git-scm.com/download/win> se Git install karo.
2. Ek baar apna naam aur email set karo:
   ```
   git config --global user.name "Varun Patel"
   git config --global user.email "patelvarun07674@gmail.com"
   ```
3. GitHub pe khaali repository banao (upar Tareeka A ke step 2–3 jaisa).
4. Project folder mein Command Prompt kholo aur chalao (`USERNAME` ki jagah apna GitHub username):
   ```
   git init
   git add .
   git commit -m "Initial commit: AI Study Chatbot"
   git branch -M main
   git remote add origin https://github.com/USERNAME/ai-study-chatbot.git
   git push -u origin main
   ```
5. Pehli baar push pe browser mein GitHub login maangega — login kar do.

### Repository ko professional banao

- Repository page pe right side **⚙️ About** pe click karke ek line description aur topics daalo:
  `python`, `streamlit`, `groq`, `llama`, `ai`, `machine-learning`, `rag`, `langchain`
- App ka screenshot lo aur README mein daalo — isse repo bahut accha dikhta hai.
- Apne GitHub profile pe in 4 repositories ko **Pin** karo (Profile → Customize your pins).

---

## Step 6 (Bonus): Live link banao — Streamlit Cloud pe free deploy

Resume mein **live demo link** ho to bahut impression padta hai.

1. <https://share.streamlit.io> pe GitHub account se login karo.
2. **Create app → Deploy a public app from GitHub** chuno.
3. Repository, branch `main` aur file `app.py` chuno.
4. **Advanced settings → Secrets** mein ye daalo (project 1, 2, 3 ke liye):
   ```
   GROQ_API_KEY = "apni-key"
   ```
5. **Deploy** dabao. 2–3 minute mein `https://xyz.streamlit.app` jaisa live link mil jaayega.

---

## Step 7: Resume mein link daalo

Resume (`varun_resume_pro.tex`) mein:
- Header mein `varunpatel` ki jagah apna asli GitHub aur LinkedIn username daalo.
- Har project ke saath GitHub ya live link likh sakte ho.

## Interview mein kya bolna hai (short mein)

| Project | Ek line mein samjhao |
|---|---|
| AI Study Chatbot | "Groq API (Llama 3.3 model) se chatbot banaya jo Hindi/English mein padhata hai aur JSON output se MCQ quiz banata hai." |
| AI Resume Analyzer | "PDF se text nikaal ke, prompt engineering se resume aur job description compare karke match score aur missing skills deta hai." |
| Chat with PDF | "RAG app hai — PDF ko chunks mein todke FastEmbed se free local embeddings banaye, FAISS mein store kiye, aur sawaal pe sabse milte-julte chunks se Groq ka Llama model answer deta hai, page number ke saath." |
| Sentiment Analysis | "TF-IDF aur Logistic Regression se ML model train kiya, accuracy, precision, recall aur confusion matrix se evaluate kiya." |

👉 Har project ka code ek baar khud padh lo aur chala ke dekh lo — interview mein code ke baare mein sawaal zaroor aayenge.

## Common problems

| Problem | Solution |
|---|---|
| `python is not recognized` | Python dobara install karo, "Add to PATH" pe tick lagake |
| `API key not valid` | `.env` mein key sahi copy karo, aage-peeche space na ho |
| `429` / rate limit error | Groq free limit khatam — 1 minute ruk ke dobara try karo |
| Chat with PDF pehli baar slow | Pehli baar embedding model (~70 MB) download hota hai, baad mein fast chalega |
| Model not found error | `.env` mein `GROQ_MODEL=llama-3.3-70b-versatile` ko naye model naam se badlo (list: console.groq.com/docs/models) |
| Chat with PDF mein "No text found" | Scanned PDF hai — text wala PDF use karo |
