import requests
from dotenv import load_dotenv, find_dotenv
import os
from scholarly import scholarly
from typing import Dict, List, Any


load_dotenv(find_dotenv())

API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def summarize(payload: str) -> str:
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()[0]["summary_text"]

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