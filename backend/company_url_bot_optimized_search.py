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
