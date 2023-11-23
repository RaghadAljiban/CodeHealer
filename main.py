import os
import openai
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv

openai.api_key=st.secrets["auth_key"]

load_dotenv()

def load_files():
    text=""
    data_dir=os.path.join(os.getcwd(), "data")
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir,filename),"r")as f:
                text+=f.read()
    return text

def extract_text_from_pdf(pdf_file):
    reader=PdfReader(pdf_file)
    raw_text=""
    for page in reader.pages:
        content=page.extract_text()
        if content:
            raw_text+=content
    return raw_text

def get_response(text):
    prompt= f"""
            You specialize in error checking for code. When presented with code enclosed by four backquotes,
              your task is to identify and rectify any errors, returning the corrected, error-free code.

            text: ''''{text}'''' 
            """
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role":"system",
                "content":prompt,
            },
        ],
    )
    return response["choices"][0]["message"]["content"]
def main():

    st.set_page_config(
        page_title="CodeHealer",
        page_icon="💯"
        
    )
    st.title("Code Healer app")
    st.write("this app takes your buggy code and returns it error-free. No more head-scratching over syntax issues. Just submit, and get back code that works.")
    st.divider()

    option=st.radio("Select Input Type",("Text","PDF"))
    if option =="Text":
        user_input=st.text_area("Write your code","")

        if st.button("Submit")and user_input !="":
            response=get_response(user_input)
            st.subheader("Error free")
            st.markdown(f">{response}")
        else:
            st.error("Please enter code.")
    else:
        uploaded_file=st.file_uploader("Choose a PDF file", type="pdf")
        if st.button("Submit")and uploaded_file is not None:
            text=extract_text_from_pdf(uploaded_file)

            response=get_response(text=text)
            st.subheader("Error free")
            st.markdown(f">{response}")
        else:
            st.error("Please upload a PDF file.")


if __name__=="__main__":
    main()
