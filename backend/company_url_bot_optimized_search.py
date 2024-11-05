'''
# backend/company_url_bot_optimized_search.py
import csv
import time
import random
import os
from dotenv import load_dotenv
from seleniumbase import SB

# Load LinkedIn credentials
load_dotenv()
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin(sb):
    sb.open("https://www.linkedin.com/login")
    sb.type('input[name="session_key"]', linkedin_username)
    sb.type('input[name="session_password"]', linkedin_password)
    sb.click('button[type="submit"]')
    time.sleep(random.uniform(3, 6))  # Wait for login to complete

def search_for_company(sb, company_name):
    search_url = f"https://www.linkedin.com/search/results/companies/?keywords={company_name}"
    sb.open(search_url)
    time.sleep(2)  # Wait for results to load

    try:
        # Select the first result's URL
        company_link = sb.get_attribute(
            'ul.reusable-search__entity-result-list li.reusable-search__result-container a.app-aware-link', 'href'
        )
        return company_link
    except Exception as e:
        print(f"Error finding company link for {company_name}: {e}")
        return None

async def search_linkedin_urls(company_names):
    output_file = "uploads/output.csv"

    # Initialize output file with header if it doesn't exist
    if not os.path.exists(output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
            writer.writeheader()

    with SB(uc=True, ad_block_on=True) as sb:
        login_to_linkedin(sb)

        for company_name in company_names:
            linkedin_url = search_for_company(sb, company_name)
            result = {"linkedincompanypageurl": linkedin_url if linkedin_url else "Not found"}
            
            # Append result to the CSV file
            with open(output_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
                writer.writerow(result)
                
            print(f"Processed {company_name} - LinkedIn URL: {linkedin_url}")
            time.sleep(random.uniform(1.5, 3))  # Rate limit

    print(f"LinkedIn URLs saved to {output_file}")


import csv
import time
import random
import os
from dotenv import load_dotenv
from seleniumbase import SB

# Load LinkedIn credentials
load_dotenv()
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin(sb):
    sb.open("https://www.linkedin.com/login")
    sb.type('input[name="session_key"]', linkedin_username)
    sb.type('input[name="session_password"]', linkedin_password)
    sb.click('button[type="submit"]')
    time.sleep(random.uniform(3, 6))  # Wait for login to complete

def search_for_company(sb, company_name):
    search_url = f"https://www.linkedin.com/search/results/companies/?keywords={company_name}"
    sb.open(search_url)
    time.sleep(2)  # Wait for results to load

    try:
        # Select the first result's URL
        company_link = sb.get_attribute(
            'ul.reusable-search__entity-result-list li.reusable-search__result-container a.app-aware-link', 'href'
        )
        return company_link
    except Exception as e:
        print(f"Error finding company link for {company_name}: {e}")
        return None

async def search_linkedin_urls(whitelist_companies, blacklist_companies=None):
    output_whitelist = "uploads/whitelist_linkedin.csv"
    output_blacklist = "uploads/blacklist_linkedin.csv" if blacklist_companies else None

    # Initialize whitelist output file with header if it doesn't exist
    with open(output_whitelist, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
        writer.writeheader()

    # Initialize blacklist output file if it exists
    if output_blacklist:
        with open(output_blacklist, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
            writer.writeheader()

    with SB(uc=True, ad_block_on=True) as sb:
        login_to_linkedin(sb)

        # Process whitelist companies
        for company_name in whitelist_companies:
            linkedin_url = search_for_company(sb, company_name)
            result = {"linkedincompanypageurl": linkedin_url if linkedin_url else "Not found"}
            
            # Append result to the whitelist CSV file
            with open(output_whitelist, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
                writer.writerow(result)
                
            print(f"Processed {company_name} - LinkedIn URL: {linkedin_url}")
            time.sleep(random.uniform(1.5, 3))  # Rate limit

        # Process blacklist companies if provided
        if blacklist_companies:
            for company_name in blacklist_companies:
                linkedin_url = search_for_company(sb, company_name)
                result = {"linkedincompanypageurl": linkedin_url if linkedin_url else "Not found"}
                
                # Append result to the blacklist CSV file
                with open(output_blacklist, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
                    writer.writerow(result)
                    
                print(f"Processed {company_name} - LinkedIn URL: {linkedin_url}")
                time.sleep(random.uniform(1.5, 3))  # Rate limit

    print(f"LinkedIn URLs saved to {output_whitelist}" + (f" and {output_blacklist}" if output_blacklist else ""))


import csv
import time
import random
import os
from dotenv import load_dotenv
from seleniumbase import SB

# Load LinkedIn credentials
load_dotenv()
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin(sb):
    sb.open("https://www.linkedin.com/login")
    sb.type('input[name="session_key"]', linkedin_username)
    sb.type('input[name="session_password"]', linkedin_password)
    sb.click('button[type="submit"]')
    time.sleep(random.uniform(3, 6))  # Wait for login to complete

def search_for_company(sb, company_name):
    search_url = f"https://www.linkedin.com/search/results/companies/?keywords={company_name}"
    sb.open(search_url)
    time.sleep(2)  # Wait for results to load

    try:
        # Select the first result's URL
        company_link = sb.get_attribute(
            'ul.reusable-search__entity-result-list li.reusable-search__result-container a.app-aware-link', 'href'
        )
        return company_link
    except Exception as e:
        print(f"Error finding company link for {company_name}: {e}")
        return None

async def search_linkedin_urls(whitelist_companies, blacklist_companies=None):
    output_whitelist = "uploads/whitelist_linkedin.csv"
    output_blacklist = "uploads/blacklist_linkedin.csv" if blacklist_companies else None

    # Initialize whitelist output file with header if it doesn't exist
    with open(output_whitelist, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
        writer.writeheader()

    # Initialize blacklist output file if it exists
    if output_blacklist:
        with open(output_blacklist, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
            writer.writeheader()

    with SB(uc=True, ad_block_on=True) as sb:
        login_to_linkedin(sb)

        # Process whitelist companies
        for company_name in whitelist_companies:
            linkedin_url = search_for_company(sb, company_name)
            result = {"linkedincompanypageurl": linkedin_url if linkedin_url else "Not found"}
            
            # Append result to the whitelist CSV file
            with open(output_whitelist, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
                writer.writerow(result)
                
            print(f"Processed {company_name} - LinkedIn URL: {linkedin_url}")
            time.sleep(random.uniform(1.5, 3))  # Rate limit

        # Process blacklist companies if provided
        if blacklist_companies:
            for company_name in blacklist_companies:
                linkedin_url = search_for_company(sb, company_name)
                result = {"linkedincompanypageurl": linkedin_url if linkedin_url else "Not found"}
                
                # Append result to the blacklist CSV file
                with open(output_blacklist, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
                    writer.writerow(result)
                    
                print(f"Processed {company_name} - LinkedIn URL: {linkedin_url}")
                time.sleep(random.uniform(1.5, 3))  # Rate limit

    print(f"LinkedIn URLs saved to {output_whitelist}" + (f" and {output_blacklist}" if output_blacklist else ""))

# backend/company_url_bot_optimized_search.py
import csv
import time
import random
import sys
import os
from dotenv import load_dotenv
from seleniumbase import SB

# Load LinkedIn credentials
load_dotenv()
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin(sb):
    sb.open("https://www.linkedin.com/login")
    sb.type('input[name="session_key"]', linkedin_username)
    sb.type('input[name="session_password"]', linkedin_password)
    sb.click('button[type="submit"]')
    time.sleep(random.uniform(3, 6))  # Wait for login to complete

def search_for_company(sb, company_name):
    search_url = f"https://www.linkedin.com/search/results/companies/?keywords={company_name}"
    sb.open(search_url)
    time.sleep(2)  # Wait for results to load

    try:
        company_link = sb.get_attribute(
            'ul.reusable-search__entity-result-list li.reusable-search__result-container a.app-aware-link', 'href'
        )
        return company_link
    except Exception:
        return None

def search_linkedin_urls(input_file, output_file, sb):
    # Initialize output file with header if it doesn't exist
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["linkedincompanypageurl"])
        writer.writeheader()

        with open(input_file, 'r', encoding='utf-8') as infile:
            for company in infile:
                linkedin_url = search_for_company(sb, company.strip())
                writer.writerow({"linkedincompanypageurl": linkedin_url if linkedin_url else "Not found"})
                print(f"Processed {company.strip()} - LinkedIn URL: {linkedin_url}")
                time.sleep(random.uniform(1.5, 3))  # Rate limiting

if __name__ == "__main__":
    whitelist_file = sys.argv[1]
    whitelist_output = sys.argv[2]

    # Optional blacklist files
    blacklist_file = sys.argv[3] if len(sys.argv) > 3 else None
    blacklist_output = sys.argv[4] if len(sys.argv) > 4 else None

    with SB(uc=True, ad_block_on=True) as sb:
        login_to_linkedin(sb)

        # Process whitelist
        search_linkedin_urls(whitelist_file, whitelist_output, sb)

        # Process blacklist if provided
        if blacklist_file and blacklist_output:
            search_linkedin_urls(blacklist_file, blacklist_output, sb)

    print(f"LinkedIn URLs saved to {whitelist_output}" + (f" and {blacklist_output}" if blacklist_file else ""))


# backend/company_url_bot_optimized_search.py
import csv
import time
import random
from dotenv import load_dotenv
from seleniumbase import SB
import os

load_dotenv()
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin(sb):
    sb.open("https://www.linkedin.com/login")
    sb.type('input[name="session_key"]', linkedin_username)
    sb.type('input[name="session_password"]', linkedin_password)
    sb.click('button[type="submit"]')
    time.sleep(random.uniform(3, 6))

def search_for_company(sb, company_name):
    sb.open(f"https://www.linkedin.com/search/results/companies/?keywords={company_name}")
    time.sleep(2)
    try:
        return sb.get_attribute('ul.reusable-search__entity-result-list li.reusable-search__result-container a.app-aware-link', 'href')
    except Exception:
        return None

async def search_linkedin_urls(company_names, whitelist_data, blacklist_data):
    output_whitelist = "uploads/whitelist_linkedin.csv"
    output_blacklist = "uploads/blacklist_linkedin.csv"

    with open(output_whitelist, 'w', newline='', encoding='utf-8') as wl_file, \
         open(output_blacklist, 'w', newline='', encoding='utf-8') as bl_file:
        
        wl_writer = csv.DictWriter(wl_file, fieldnames=["Company Name", "linkedincompanypageurl"])
        bl_writer = csv.DictWriter(bl_file, fieldnames=["Company Name", "linkedincompanypageurl"])
        wl_writer.writeheader()
        bl_writer.writeheader()

        with SB(uc=True, ad_block_on=True) as sb:
            login_to_linkedin(sb)
            for company_name in company_names:
                linkedin_url = search_for_company(sb, company_name)
                row = {"Company Name": company_name, "linkedincompanypageurl": linkedin_url or "Not found"}
                
                if whitelist_data.get(company_name):
                    wl_writer.writerow(row)
                else:
                    bl_writer.writerow(row)
                time.sleep(random.uniform(1.5, 3))
    print(f"LinkedIn URLs saved to {output_whitelist} and {output_blacklist}")
'''

# backend/company_url_bot_optimized_search.py
import csv
import time
import random
from dotenv import load_dotenv
from seleniumbase import SB
import os

load_dotenv()
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin(sb):
    sb.open("https://www.linkedin.com/login")
    sb.type('input[name="session_key"]', linkedin_username)
    sb.type('input[name="session_password"]', linkedin_password)
    sb.click('button[type="submit"]')
    time.sleep(random.uniform(3, 6))

def search_for_company(sb, company_name):
    sb.open(f"https://www.linkedin.com/search/results/companies/?keywords={company_name}")
    time.sleep(2)
    try:
        return sb.get_attribute('ul.reusable-search__entity-result-list li.reusable-search__result-container a.app-aware-link', 'href')
    except Exception:
        return None

async def search_linkedin_urls(company_names, whitelist_data, blacklist_data):
    output_whitelist = "uploads/whitelist_linkedin.csv"
    output_blacklist = "uploads/blacklist_linkedin.csv"

    with open(output_whitelist, 'w', newline='', encoding='utf-8') as wl_file, \
         open(output_blacklist, 'w', newline='', encoding='utf-8') as bl_file:
        
        wl_writer = csv.writer(wl_file)
        bl_writer = csv.writer(bl_file)
        wl_writer.writerow(["linkedincompanypageurl"])
        bl_writer.writerow(["linkedincompanypageurl"])

        with SB(uc=True, ad_block_on=True) as sb:
            login_to_linkedin(sb)
            for company_name in company_names:
                linkedin_url = search_for_company(sb, company_name)
                row = [linkedin_url if linkedin_url else "Not found"]
                
                if whitelist_data.get(company_name):
                    wl_writer.writerow(row)
                else:
                    bl_writer.writerow(row)
                time.sleep(random.uniform(1.5, 3))
    print(f"LinkedIn URLs saved to {output_whitelist} and {output_blacklist}")
