'''
WICHTIG: URL ENCODING WEGEN SONDERZEICHEN ETC. & DIE SPALTE IN DER FINALEN EXPORT-CSV FÜR DEN LINKEDIN
ADS CAMPAIGN MANAGER MIT DER SPALTE "linkedincompanypageurl" BENENNEN
'''
import csv
from urllib.parse import quote

# Input and output file paths
input_file = 'olmero_finale_urls.csv'
output_file = 'olmero_final_encoded.csv'

# Read the CSV file
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    
    # Get the column names from the original file
    fieldnames = reader.fieldnames
    
    # Prepare to write to the output file
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Write the header to the output file
        writer.writeheader()
        
        # Process each row
        for row in reader:
            original_url = row['linkedincompanypageurl']
            
            # Encode the URL
            encoded_url = quote(original_url, safe=":/")
            
            # Replace the original URL with the encoded one
            row['linkedincompanypageurl'] = encoded_url
            
            # Write the updated row to the output file
            writer.writerow(row)

print(f"Encoded URLs have been written to {output_file}")
