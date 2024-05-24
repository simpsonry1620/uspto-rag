import os
import requests
from bs4 import BeautifulSoup
import re

# Base URL of the MPEP content
base_url = "https://www.uspto.gov/web/offices/pac/mpep/"

# List of MPEP chapter URLs
chapters = [
    "mpep-0100.html",
    "mpep-0200.html",
    "mpep-0300.html",
    "mpep-0400.html",
    "mpep-0500.html",
    "mpep-0600.html",
    "mpep-0700.html",
    "mpep-0800.html",
    "mpep-0900.html",
    "mpep-1000.html",
    "mpep-1100.html",
    "mpep-1200.html",
    "mpep-1300.html",
    "mpep-1400.html",
    "mpep-1500.html",
    "mpep-1600.html",
    "mpep-1700.html",
    "mpep-1800.html",
    "mpep-1900.html",
    "mpep-2000.html",
    "mpep-2100.html",
    "mpep-2200.html",
    "mpep-2300.html",
    "mpep-2400.html",
    "mpep-2500.html",
    "mpep-2600.html",
    "mpep-2700.html",
    "mpep-2800.html",
    "mpep-2900.html",
]

# Directory to save the processed text files
txt_directory = '../data/scratch/txt/'

# Create directory if it doesn't exist
if not os.path.exists(txt_directory):
    os.makedirs(txt_directory)

def scrape_and_save(url, save_path):
    """
    Scrapes the text content from the given URL and saves it to the specified path.
    
    Args:
    url (str): URL of the webpage to scrape.
    save_path (str): File path to save the scraped content.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='yui-main')
        if (main_div):
            content = main_div.get_text(separator='\n')
            cleaned_content = clean_text(content)
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            print(f"Saved content from {url} to {save_path}")
        else:
            print(f"'yui-main' section not found in {url}")
    else:
        print(f"Failed to retrieve content from {url}")

def get_section_urls(chapter_url):
    """
    Retrieves a list of section URLs from the given chapter URL.
    
    Args:
    chapter_url (str): URL of the chapter page to scrape for section links.
    
    Returns:
    list: A list of section URLs found in the chapter page.
    """
    response = requests.get(chapter_url)
    section_urls = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='yui-main')
        if main_div:
            links = main_div.find_all('a', href=True)
            for link in links:
                href = link['href']
                if 'mpep-' in href and href.endswith('.html'):
                    section_urls.append(base_url + href)
                elif href.startswith('s') and href.endswith('.html'):
                    section_urls.append(base_url + href)
    else:
        print(f"Failed to retrieve the chapter page: {chapter_url}")
    return section_urls

def clean_text(text):
    """
    Cleans the extracted text content by removing unwanted characters and fixing formatting issues.
    
    Args:
    text (str): Raw text content to be cleaned.
    
    Returns:
    str: Cleaned text content.
    """
    text = re.sub(r'(?<!\.)\n(?!\n)', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    text = re.sub(r'\s+([.,;:])', r'\1', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    text = re.sub(r'\.([A-Za-z])', r'. \1', text)
    text = re.sub(r'(\b[A-Z])\s+(\.)\s+([A-Z])\s+(\.)\s+([A-Z])\s+(\.)', r'\1\2\3\4\5\6', text)
    text = re.sub(r'(\b[A-Z]{2,})\s+(\.)', r'\1\2', text)
    text = re.sub(r'(\d+)\s+U\.?\s*S\.?\s*C\.?', r'\1 U.S.C.', text)
    text = re.sub(r'(\d+)\s+C\.?\s*F\.?\s*R\.?', r'\1 CFR', text)
    text = re.sub(r'U\.?\s*S\.?\s*P\.?\s*T\.?\s*O\.?', 'USPTO', text)
    
    return text

if __name__ == "__main__":
    # Iterate over each chapter to scrape and save its sections
    for chapter_site in chapters:
        chapter_url = base_url + chapter_site
        section_urls = get_section_urls(chapter_url)
        
        for url in section_urls:
            section_name = url.split('/')[-1].replace('.html', '.txt')
            save_path = os.path.join(txt_directory, section_name)
            scrape_and_save(url, save_path)