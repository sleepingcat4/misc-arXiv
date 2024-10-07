import requests
import os

output_folder = input("Enter the name of the output folder: ")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

error_log = input("Enter the name for the error log file (e.g., 'psy_error.txt'): ")

input_filename = input("Enter the .txt file containing URLs: ")

with open(input_filename, 'r') as file:
    urls = file.readlines()

for url in urls:
    url = url.strip().rstrip('/')
    
    if url and 'osf.io/' in url:
        # Check if the URL contains a wrong schema like "htp://", and replace it with "http://"
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url.lstrip('htp:/')
        
        filename_part = url.split('osf.io/')[-1]
        if filename_part:
            download_url = url + '/download'
            try:
                response = requests.get(download_url)

                pdf_filename = os.path.join(output_folder, f"{filename_part}.pdf")
                with open(pdf_filename, 'wb') as f:
                    f.write(response.content)

                print(f"PDF downloaded successfully as {pdf_filename}")
            except Exception as e:
                with open(error_log, 'a') as error_file:
                    error_file.write(f"Failed to download {download_url}: {e}\n")
                print(f"Error occurred with {download_url}, logged in {error_log}")
