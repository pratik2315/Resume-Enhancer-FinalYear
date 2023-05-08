import streamlit as st
import requests
from bs4 import BeautifulSoup
from pikepdf import Pdf
import io
import pandas as pd
import io
from pdfminer.high_level import extract_text_to_fp

# Define the URLs to scrape for each job profile
job_urls = {
    'Software Engineer': 'https://www.indeed.com/jobs?q=software+engineer&l=',
    'Data Scientist': 'https://www.indeed.com/jobs?q=data+scientist&l=',
    'Marketing Manager': 'https://www.indeed.com/jobs?q=marketing+manager&l='
}

# Define a function to extract text from the PDF file
def extract_text(pdf_file):
    with io.BytesIO(pdf_file.read()) as f:
        output_string = io.StringIO()
        extract_text_to_fp(f, output_string)
        return output_string.getvalue()

# Define a function to scrape job websites and calculate the applicant's chances
def calculate_chances(job_urls, resume_text):
    chances = {}
    for job_title, job_url in job_urls.items():
        # Scrape the job website and count the number of times the resume text appears
        response = requests.get(job_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        job_description = soup.find_all('div', {'class': 'jobsearch-JobComponent-description'})
        count = 0
        for jd in job_description:
            if resume_text in jd.text.lower():
                count += 1
        # Calculate the applicant's chances based on the number of times the resume text appears
        chances[job_title] = count / len(job_description) * 100
    return chances

# Set up the Streamlit app
st.title('Job Chances Calculator')
resume_file = st.file_uploader('Upload your resume in PDF format:', type='pdf')
if resume_file:
    resume_text = extract_text(resume_file)
    job_df = pd.read_csv("job_urls.csv") # Load the job URLs dataset
    job_urls = dict(zip(job_df['Job Title'], job_df['URL'])) # Convert the dataset to a dictionary
    chances = calculate_chances(job_urls, resume_text)
    st.write('Your chances of getting selected for each job profile are:')
    for job_title, chance in chances.items():
        st.write(f'{job_title}: {chance}%')
