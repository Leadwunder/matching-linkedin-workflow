# openai_imprint_scraper.py
import asyncio
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
org_id = os.getenv("OPENAI_ORG_ID")
client = OpenAI(api_key=api_key, organization=org_id)

def extract_text_from_url(url, max_words=600):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        words = soup.get_text(separator=' ').split()
        return ' '.join(words[:max_words]) if words else None
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

async def call_openai_api(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini"
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred with OpenAI API: {e}")
        return "Error fetching data from OpenAI API"

async def process_imprint_urls(input_csv, is_whitelist=True):
    extracted_data = {}
    with open(input_csv, 'r') as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]

    for url in urls:
        print(f"Processing URL: {url}")
        text_content = extract_text_from_url(url)
        
        if text_content:
            prompt = (
                f"Extract the following information from the text:\n"
                f"{text_content}\n\n"
                "Provide the details in this format:\n"
                "Company Name: [full company name]\n"
                "CEO: [name]\n"
                "Email Address: [email]\n"
                "Postal Address: [address]\n"
                "Phone Number: [phone]\n"
            )

            response = await call_openai_api(prompt)
            if response and "Error" not in response:
                company_name = ""
                for line in response.split('\n'):
                    if 'Company Name:' in line:
                        company_name = line.split(':')[1].strip()
                        extracted_data[company_name] = is_whitelist
    return extracted_data

async def main():
    if len(sys.argv) < 3:
        print("Usage: python openai_imprint_scraper.py <whitelist_csv> <blacklist_csv>")
        sys.exit(1)

    whitelist_csv = sys.argv[1]
    blacklist_csv = sys.argv[2]

    whitelist_data = await process_imprint_urls(whitelist_csv, is_whitelist=True)
    blacklist_data = await process_imprint_urls(blacklist_csv, is_whitelist=False)

    all_company_names = list(whitelist_data.keys()) + list(blacklist_data.keys())
    from company_url_bot_optimized_search import search_linkedin_urls
    await search_linkedin_urls(all_company_names, whitelist_data, blacklist_data)

asyncio.run(main())
