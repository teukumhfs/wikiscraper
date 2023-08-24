import requests
from bs4 import BeautifulSoup
import re

url = input("Enter the URL: ")

response = requests.get(url)

if response.status_code == 200:
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3"])  # Find h1, h2, and h3 elements
    paragraphs = soup.find_all("p")
    definition_list = soup.find_all("dl")
    unordered_list = soup.find_all("ul")

    cleaned_text = ""

    for heading in headings:
        heading_text = re.sub(r'\[.*?\]', '', heading.get_text().strip())
        cleaned_text += f"{heading_text}\n\n"

        # Find corresponding paragraphs for each heading
        for sibling in heading.find_next_siblings():
            if sibling.name and sibling.name.startswith("h"):
                break  # Stop if another heading is found
            elif sibling.name == "p":
                p_text = re.sub(r'\[.*?\]', '', sibling.get_text().strip())
                cleaned_text += f"{p_text}\n\n"
            elif sibling.name == "dl":
                dl_text = re.sub(r'\[.*?\]', '', sibling.get_text().strip())
                cleaned_text += f"{dl_text}\n"
            elif sibling.name == "ul":
                ul_text = re.sub(r'\[.*?\]', '', sibling.get_text().strip())
                cleaned_text += f"{ul_text}\n"

    with open("exported_text.txt", "w", encoding="utf-8") as file:
        file.write(cleaned_text)

    print("Text export saved to exported_text.txt")
else:
    print("Parsing Failed.")
