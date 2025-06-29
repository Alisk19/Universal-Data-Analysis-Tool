# Deployment Information

This document provides step-by-step instructions for deploying the Universal Data Analysis Tool both locally and on popular cloud platforms.

---

## 🚀 Local Deployment

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit app:**
   ```bash
   streamlit run main.py
   ```
4. **Open your browser** to the local URL provided by Streamlit (usually http://localhost:8501).

---

## ☁️ Deploying on Streamlit Cloud

1. **Push your code to a public GitHub repository.**
2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)** and sign in.
3. **Click 'New app'** and connect your GitHub repo.
4. **Set the main file path** to `main.py`.
5. **(Optional) Add a requirements.txt** if not already present.
6. **Click 'Deploy'.**

Your app will be live on a public URL!

---

## ☁️ Deploying on Heroku

1. **Install the Heroku CLI** if you haven't already.
2. **Create a `Procfile`** in your project root with this line:
   ```
   web: streamlit run main.py --server.port=$PORT
   ```
3. **Add all files to git and commit:**
   ```bash
   git add .
   git commit -m "Initial deploy"
   ```
4. **Create a Heroku app:**
   ```bash
   heroku create your-app-name
   ```
5. **Push to Heroku:**
   ```bash
   git push heroku main
   ```
6. **Open your app:**
   ```bash
   heroku open
   ```

---

## 📝 Notes
- Make sure your `requirements.txt` includes all necessary dependencies (e.g., streamlit, pandas, matplotlib, openpyxl).
- For cloud deployment, ensure your app does not require local file access outside the project directory.
- For private data, consider deploying on a private server or using authentication.

---

For more help, see the [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud/deploy) or [Heroku Python Docs](https://devcenter.heroku.com/categories/python-support). 
