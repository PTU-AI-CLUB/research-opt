import requests
import os
from scholarly import scholarly
from typing import Dict, List, Any
import fitz
from unidecode import unidecode
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class DocumentSummarizer:

    API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

    # API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def __init__(self, path: str) -> None:
        self.doc = fitz.open(path)
        self.toc = self.doc.get_toc(simple=True)
    
    def _summarize(self, payload: str):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()[0]["summary_text"]
    
    def summarize(self) -> str:
        summarized_doc = {}
        for i, content in enumerate(self.toc):
            title = content[1]
            page_no = content[2]

            if i+1==len(self.toc):
                text = unidecode(self.doc[page_no-1].get_text())
                start_idx = text.find(title)
                content_text = text[len(title)+start_idx:]
                
            
            else:
                start_idx = unidecode(self.doc[page_no-1].get_text()).find(title)
                end_idx = unidecode(self.doc[self.toc[i+1][2]-1].get_text()).find(self.toc[i+1][1])
                if page_no == self.toc[i+1][2]:
                    content_text = unidecode(self.doc[page_no-1].get_text())[len(title)+start_idx:end_idx]
                else:
                    content_text = unidecode(self.doc[page_no-1].get_text())[len(title)+start_idx:] + \
                                   unidecode(self.doc[self.toc[i+1][2]-1].get_text())[:end_idx]
            
            content_text = content_text.replace("\n", " ")
            summzarized_content_text = ""
            while len(content_text)>512:
                summzarized_content_text += self._summarize(content_text[:512])
                content_text = content_text[512:]
            summarized_doc[title] = summzarized_content_text
        
        summarized_paper = ""
        for title, content in summarized_doc.items():
            summarized_paper += title + "\n" + content
        return summarized_paper
    



def get_author_details(auth_name: str) -> Dict[str, Any]:
	auth_details = scholarly.search_author(auth_name)
	auth_details = next(auth_details)
	return {
		"name" : auth_details["name"],
		"affiliation" : auth_details["affiliation"],
		"interests" : auth_details["interests"],
		"citations" : auth_details["citedby"]
    }


if __name__ == "__main__":
    # print(summarize("""The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct."""))
    # paper_title = 'Attention is all you need'
    # get_reference_pdfs(paper_title)
    print(get_author_details("K Sathiyamurthy"))