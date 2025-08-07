# 📨 HR Connect Pro – Find & Email HRs in Minutes

**HR Connect Pro** is your job search assistant. It automates one of the most time-consuming parts of the job hunt: **finding HR contacts** and **sending personalized outreach emails** — all from a single app.

---

## 🚨 The Problem

You’re a job seeker. You’ve built the resume. You’ve identified your dream companies. But:

- ❌ You don’t have HR contacts  
- ❌ Cold applying isn’t working  
- ❌ Writing personalized emails every time takes hours  

**That’s where HR Connect Pro comes in.**

---

## ✅ What It Does

✨ **Enter a company and job role**  
🔍 **Find HR/recruiter profiles on LinkedIn (via Google search using SerpAPI)**  
📧 **Find verified emails using Hunter.io Email Finder**  
📩 **Auto-generate personalized outreach emails using your profile**  
📤 **Send emails in bulk using Gmail SMTP**  
📁 **Export contact info to CSV for your own tracking**

---

## 🛠 Tech Stack

| Layer            | Tool                         |
|------------------|------------------------------|
| UI               | Streamlit                    |
| Search Backend   | SerpAPI (Google Search API)  |
| Email Discovery  | Hunter.io Email Finder API   |
| Email Sending    | Python SMTP (Gmail)          |
| Templating       | Custom Python logic          |
| Env Management   | `python-dotenv`              |

---

## 🔐 Why Not LinkedIn API?

I initially planned to integrate LinkedIn directly. But due to **API access restrictions**, I used **SerpAPI** to search LinkedIn profiles via Google.

This gives you:  
- ✅ Publicly available profile data  
- ✅ Zero scraping or login issues  
- ❌ No access to emails (unless public)

To overcome this, I added **Hunter.io** — a verified email discovery tool that finds **professional work emails** based on the HR’s name and company domain.

This gives you:  
- ✅ Accurate and verified emails  
- ✅ High deliverability  
- ✅ No guesswork

---

## 🧪 Demo Use Case

> 💡 Let’s say you're applying for a Software Engineer role at **Google**.

1. Enter "Google" as company, "Software Engineer" as role  
2. App finds real LinkedIn profiles of HR professionals at Google using SerpAPI  
3. Uses Hunter.io to fetch their work email (e.g., `sarah@google.com`)  
4. Auto-generates an email like:

```text
Subject: Application for Software Engineer at Google

Dear Sarah,

I hope this message finds you well. I’m a Software Engineer with 3 years of experience in scalable backend systems and cloud infrastructure...

(Your email continues here with full personalization.)
