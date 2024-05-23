import os
import requests
import zipfile

def download_zip(url, save_path):
    """
    Downloads a ZIP file from the given URL and saves it to the specified path.

    Parameters:
    url (str): URL of the ZIP file to download.
    save_path (str): Path where the ZIP file will be saved.

    Returns:
    None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded ZIP file from {url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def extract_pdfs(zip_path, extract_to):
    """
    Extracts PDFs from a ZIP file and saves them to the specified directory.

    Parameters:
    zip_path (str): Path to the ZIP file.
    extract_to (str): Directory where the extracted PDFs will be saved.

    Returns:
    None
    """
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.lower().endswith('.pdf'):
                zip_ref.extract(file_name, extract_to)
                print(f"Extracted: {file_name}")

if __name__ == "__main__":
    """
    Main entry point of the script.
    """
    # URL of the ZIP file to download
    zip_url = 'https://www.uspto.gov/web/offices/pac/mpep/e9r-07-2022.zip'
    
    # Directory to save the downloaded ZIP file
    zip_save_dir = '../data/scratch/'
    
    # Path to save the downloaded ZIP file
    zip_save_path = os.path.join(zip_save_dir, 'e9r-07-2022.zip')
    
    # Directory to save the extracted PDFs
    pdf_extract_dir = '../data/scratch/pdfs/'
    
    # Download the ZIP file
    download_zip(zip_url, zip_save_path)
    
    # Extract PDFs from the ZIP file
    extract_pdfs(zip_save_path, pdf_extract_dir)
