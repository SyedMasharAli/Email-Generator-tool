import streamlit as st
import os
import json
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize LangChain and OpenAI
llm = None  # Define llm here initially as None

# Create a Streamlit app with page navigation
st.title("📧 Email Generator")

# Function to load email history from file
def load_email_history():
    if os.path.exists(email_history_file):
        with open(email_history_file, "r") as f:
            email_history = json.load(f)
    else:
        email_history = []
    return email_history

# Function to save email history to file
def save_email_history(email_history):
    with open(email_history_file, "w") as f:
        json.dump(email_history, f)

# Function to generate an email and store it in the email history
def generate_email(sender, subject, receiver_name, email_tone, email_length, purpose):
    email_template = f"You are a professional email writer with a decade of experience. Your expertise is to write professional and eye-catching emails. Please write a professional-looking email for receiver: {receiver_name} from sender: {sender} with the subject: {subject}. Tone should be: {email_tone} and the length must be: {email_length}. Here is the purpose of this email: {purpose}"
    chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(email_template))
    generated_email = chain.run(sender=sender, subject=subject)
    
    # Load the email history
    email_history = load_email_history()
    
    # Append the generated email to the history
    email_history.append(generated_email)

    # Save the updated email history
    save_email_history(email_history)

    return generated_email

# Function to retrieve and display email history
def get_email_history():
    email_history = load_email_history()
    return email_history

# File path for email history
email_history_file = "email_history.json"

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Generate Email", "Reply to Email", "Email History"])

# Check if the API key is provided
api_key = st.text_input("Enter your OpenAI API Key:")
if api_key:
    llm = OpenAI(openai_api_key=api_key)

# Page for generating emails
if page == "Generate Email":
    st.subheader("Generate Email Page")
    col1, col2 = st.columns(2) 

    # Input fields for sender (recipient) and subject
    sender = col1.text_input("📤Sender")
    subject = st.text_input("Subject")

    col3, col4 = st.columns(2)
    receiver_name = col2.text_input("📨Receiver's Name")
    email_tone = col3.selectbox("Email Tone", ["🎩 Formal", "😄 Informal","😊 Friendly Tone:","⚠️ Urgent Tone:","📊 Professional Tone","❤️ Sincere Tone","🙇‍♂️🙇‍♀️Apologetic Tone"])
    email_length = col4.selectbox("Email Length", ["📝Short", "📃Medium", "📄Long"])
    purpose = st.text_area("What's this Email about.")

    if st.button("Generate Email Content", key="generate_email_content"):
        generated_email = generate_email(sender, subject, receiver_name, email_tone, email_length, purpose)
        
        # Display the generated email
        st.subheader("Generated Email:")
        st.write(generated_email)

# Page for replying to emails
elif page == "Reply to Email":
    st.subheader("Reply to Email Page")
    col1, col2 = st.columns(2)
    # Input fields for user inputs
    recipientname = col1.text_input("Recipient's Name")
    sendername = col2.text_input("Sender's Name")
    reply_subject = st.text_input("Subject for Reply")
    reply_tone = col1.selectbox("Email Tone", ["🎩 Formal", "😄 Informal", "😊 Friendly Tone:", "⚠️ Urgent Tone:", "📊 Professional Tone", "❤️ Sincere Tone", "🙇‍♂️🙇‍♀️Apologetic Tone"])
    reply_length = col2.selectbox("Email Length", ["📝Short", "📃Medium", "📄Long"])
    
    # Input fields for received email and response goals
    received_email = st.text_area("Received Email")
    response_goals = st.text_area("Response Goals (optional)")

    if st.button("Generate Reply", key="generate_reply_email"):
        reply_email_template = f"You received an email with the following content:\n\n---\n\n{received_email}\n\n---\n\nResponse Goals:\n{response_goals}\n\nPlease craft a thoughtful response to the sender. Here are the details for your reply:\n\nRecipient: {recipientname}\nSender Name: {sendername}\nSubject: {reply_subject}\nEmail Tone: {reply_tone}\nEmail Length: {reply_length}"
        
        # Create a LangChain chain with the LangModel and PromptTemplate for generating the reply email
        chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(reply_email_template))
        
        # Generate the reply email content
        generated_reply_email = chain.run()

        # Load the email history
        email_history = load_email_history()
        
        # Append the generated reply email to the history
        email_history.append(generated_reply_email)

        # Save the updated email history
        save_email_history(email_history)

        st.subheader("Generated Reply Email:")
        st.write(generated_reply_email)

# Page for email history
elif page == "Email History":
    st.subheader("Email History Page")

    # Retrieve email history
    email_history = get_email_history()

    # Display email history
    if email_history:
        st.write("Generated Emails:")
        for i, email in enumerate(email_history):
            st.subheader(f"Email {i+1}:")
            st.write(email)
    else:
        st.write("No emails in the history yet.")
