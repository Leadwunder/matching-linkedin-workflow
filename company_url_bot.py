'''
LOOP UM UNTERNEHMENSURL VON LINKEDIN ZU EXTRAHIEREN. olemero_4.csv als beispieldatei mit hochgeladen.
'''
import time
import random
import os
import pandas as pd
from seleniumbase import SB

def login_to_linkedin(sb, username, password):
    # Open LinkedIn login page
    sb.open("https://www.linkedin.com/login")
    
    # Enter username
    sb.type('input[name="session_key"]', username)
    
    # Enter password
    sb.type('input[name="session_password"]', password)
    
    # Click on the 'Sign in' button
    sb.click('button[type="submit"]')
    
    time.sleep(random.uniform(5, 10))  # Wait for a random time between 5 and 10 seconds
    
    # Save cookies after login
    sb.save_cookies(name="linkedin_cookies.txt")

def search_for_company(sb, company_name):
    search_url = "https://www.linkedin.com/search/results/companies/?keywords=" + company_name
    sb.open(search_url)
    time.sleep(0.5)  # Wait for the search results to load

    try:
        # Find the first company link and click it using a selector
        sb.uc_click('ul.reusable-search__entity-result-list li.reusable-search__result-container a.app-aware-link')
        company_link = sb.get_current_url()  # Get the current URL after clicking
        return company_link
    except Exception as e:
        print(f"Error finding or clicking company link: {e}")
        return None

def extract_linkedin_company_url(sb, company_name):
    company_url = search_for_company(sb, company_name)
    if not company_url:
        return {
            'Firma': company_name,
            'LinkedIn URL': 'N/A',
        }

    # Clean the URL to ensure it's the main LinkedIn company page URL
    base_url = company_url.split('/about')[0]
    return {
        'Firma': company_name,
        'LinkedIn URL': base_url,
    }

def main():
    username = 'marc.oris.mueller@gmail.com'
    password = 'JackDaniels#43!'

    # Read the Customer column from the CSV file
    input_file = 'olmero_4.csv'
    df = pd.read_csv(input_file)
    
    if 'Firma' not in df.columns:
        print("The 'Customer' column was not found in the input file.")
        return

    customer_names = df['Firma'].dropna().unique()  # Drop any missing values and get unique customers
    
    output_file = 'olmero_upload_3.csv'

    # Initialize the CSV file with headers
    if not os.path.exists(output_file):
        pd.DataFrame(columns=['Firma', 'LinkedIn URL']).to_csv(output_file, index=False)

    with SB(uc=True, ad_block_on=True) as sb:
        if os.path.exists("linkedin_cookies.txt"):
            sb.load_cookies(name="linkedin_cookies.txt")
            sb.open("https://www.linkedin.com/feed")
        else:
            login_to_linkedin(sb, username, password)
        
        for company_name in customer_names:
            print(f"Processing {company_name}")
            company_info = extract_linkedin_company_url(sb, company_name)

            # Append the result to the CSV file immediately
            df_output = pd.DataFrame([company_info])
            df_output.to_csv(output_file, mode='a', header=False, index=False)

            print(f"Extracted LinkedIn URL for {company_info['Firma']}")
            time.sleep(random.uniform(0.5, 1.0))

    print(f"LinkedIn company URLs have been saved to {output_file}")

if __name__ == '__main__':
    main()
