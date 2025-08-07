import streamlit as st
import pandas as pd
import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

st.set_page_config(page_title="HR Connect Pro", layout="wide", page_icon="📩")

def send_email(to_email, subject, body):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email send failed: {str(e)}")
        return False

def generate_mock_hr_data(company, role):
    domains = {
        "Google": "google.com",
        "Microsoft": "microsoft.com",
        "Amazon": "amazon.com",
        "Apple": "apple.com",
        "Meta": "fb.com"
    }
    domain = domains.get(company, "example.com")
    company_key = company.lower().replace(" ", "")
    return pd.DataFrame([
        {
            "Name": f"Sarah {company.split()[0]}ski",
            "Title": f"Senior {role.split()[0]} Recruiter",
            "Email": f"sarah.recruiting@{domain}",
            "LinkedIn": f"https://linkedin.com/in/sarah-{company_key}-recruiter",
            "Company": company,
            "Department": "Talent Acquisition"
        },
        {
            "Name": f"David {company.split()[-1]}son",
            "Title": f"HR Business Partner",
            "Email": f"david.hr@{domain}",
            "LinkedIn": f"https://linkedin.com/in/david-{company_key}-hr",
            "Company": company,
            "Department": "Human Resources"
        }
    ])

def search_linkedin_hr(company_name, job_title):
    serpapi_key = os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        st.warning("⚠️ SerpAPI key missing. Using mock data.")
        return None

    query = f"{job_title} at {company_name} site:linkedin.com"
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "api_key": serpapi_key,
        "num": "10"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        people = []

        for result in data.get("organic_results", []):
            title = result.get("title", "")
            link = result.get("link", "")
            if "linkedin.com/in" in link:
                people.append({
                    "Name": title.split(" - ")[0].strip(),
                    "Title": title.split(" - ")[1].strip() if " - " in title else "Unknown",
                    "Email": "Not available",
                    "LinkedIn": link,
                    "Company": company_name,
                    "Department": "Unknown"
                })

        return pd.DataFrame(people)

    except Exception as e:
        st.error(f"SerpAPI error: {str(e)}")
        return None

def generate_email_template(contact, job_role, your_info):
    company = contact.get('Company', 'your target company')
    return f"""
Subject: {your_info.get('email_subject', f'Application for {job_role} at {company}')}

Dear {contact.get('Name', 'Hiring Manager')},

I hope this message finds you well. I'm writing to express my enthusiasm for the {job_role} position at {company}.

As a {your_info.get('your_title', '[Your Profession]')} with {your_info.get('your_experience', '[X]')} years of experience in {your_info.get('your_skills', '[relevant skills]')}, I've successfully {your_info.get('your_achievement', '[key achievement]')}.

What excites me about {company}:
- {your_info.get('reason1', '[Reason 1]')}
- {your_info.get('reason2', '[Reason 2]')}

I've attached my resume and would welcome the opportunity to discuss how I could contribute to your team. Please let me know if we might schedule a conversation.

Best regards,  
{your_info.get('your_name', 'Your Name')}  
{your_info.get('your_email', 'your.email@example.com')}  
Phone: {your_info.get('your_phone', '+1 (XXX) XXX-XXXX')}  
LinkedIn: {your_info.get('your_linkedin', 'linkedin.com/in/yourprofile')}
"""

def main():
    st.title("📨 HR Connect Pro")
    st.markdown("### Find HR contacts & automate your job search outreach")

    with st.sidebar:
        st.header("⚙️ Settings")
        use_mock_data = st.toggle("Use mock data", True)

        st.header("👤 Your Profile")
        your_info = {
            "your_name": st.text_input("Your Full Name"),
            "your_title": st.text_input("Your Profession", "Software Engineer"),
            "your_email": st.text_input("Your Email"),
            "your_phone": st.text_input("Your Phone"),
            "your_linkedin": st.text_input("LinkedIn Profile URL"),
            "your_experience": st.number_input("Years of Experience", 1, 30, 3),
            "your_skills": st.text_input("Key Skills", "Python, Data Analysis, Machine Learning"),
            "your_achievement": st.text_area("Key Achievement", "Built systems that improved efficiency by 30%"),
            "email_subject": st.text_input("Default Email Subject", "Application for {role} at {company}"),
            "reason1": st.text_input("Reason 1 for applying", "Innovative approach to AI technology"),
            "reason2": st.text_input("Reason 2 for applying", "Strong engineering culture")
        }

    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("🏢 Company Name", "Google")
    with col2:
        role = st.text_input("💼 Job Role", "Software Engineer")

    if st.button("🔍 Find HR Contacts", type="primary"):
        with st.spinner(f"Searching HR contacts at {company}..."):
            if use_mock_data:
                hr_data = generate_mock_hr_data(company, role)
            else:
                results = search_linkedin_hr(company, role)
                hr_data = results if results is not None and not results.empty else generate_mock_hr_data(company, role)

            st.session_state.hr_data = hr_data

        if not st.session_state.hr_data.empty:
            st.success(f"✅ Found {len(st.session_state.hr_data)} HR contacts at {company}")
            st.dataframe(st.session_state.hr_data, use_container_width=True)

            st.download_button(
                label="📥 Download Contacts as CSV",
                data=st.session_state.hr_data.to_csv(index=False),
                file_name=f"hr_contacts_{company}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv'
            )

    if 'hr_data' in st.session_state and not st.session_state.hr_data.empty:
        st.divider()
        st.subheader("✉️ Email Automation")

        selected = st.multiselect(
            "Select contacts to email",
            options=st.session_state.hr_data['Name'].tolist(),
            default=st.session_state.hr_data['Name'].tolist()[:2]
        )

        if selected:
            selected_contacts = st.session_state.hr_data[st.session_state.hr_data['Name'].isin(selected)].to_dict('records')

            with st.expander("📝 Email Preview"):
                preview = generate_email_template(selected_contacts[0], role, your_info)
                st.text_area("Edit template", preview, height=300)

            col1, col2 = st.columns(2)
            with col1:
                st.date_input("Start date", datetime.now())
            with col2:
                st.slider("Emails per day", 1, 20, 5)

            if st.button("🚀 Schedule Emails", type="primary"):
                progress = st.progress(0)
                status = st.empty()

                for i, contact in enumerate(selected_contacts):
                    email_body = generate_email_template(contact, role, your_info)
                    subject = your_info.get("email_subject", f"Application for {role} at {company}")
                    recipient = contact.get('Email', None)

                    if recipient and "@" in recipient:
                        success = send_email(recipient, subject, email_body)
                    else:
                        success = False

                    status.markdown(f"""
                    **Sending to:** {contact['Name']}  
                    **Status:** {"✅ Sent" if success else "❌ Failed"}  
                    **Email:** {recipient or 'Not available'}
                    """)
                    time.sleep(1)
                    progress.progress((i + 1) / len(selected_contacts))

                st.success(f"🎉 Finished sending {len(selected_contacts)} emails!")


if __name__ == "__main__":
    main()
