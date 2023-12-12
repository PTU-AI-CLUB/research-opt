from typing import Dict, List, Any

from paperswithcode import PapersWithCodeClient
from fpdf import FPDF
import fitz
from unidecode import unidecode
import os
from PIL import Image
import requests
import PIL.Image
import io
import shutil
from pathlib import Path
import arxiv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class DocumentSummarizer:

    API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    # API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def __init__(self, path: str) -> None:
        self.doc = fitz.open(path)
        self.doc_name = self.doc.name.split("/")[-1]
        self.toc = self.doc.get_toc(simple=True)
    
    def _summarize(self, payload: str):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()[0]["summary_text"]

    def _get_images(self) -> None:
        counter = 0
        if not os.path.exists("./images/"):
            os.mkdir("./images/")
        
        
        for page in self.doc:
            images = page.get_images()
        
            for image in images:
                base_image = self.doc.extract_image(image[0])
                image_data = base_image["image"]
                ext = base_image["ext"]
                image = PIL.Image.open(io.BytesIO(image_data))
                image.save(open(f"./images/{self.doc_name}_image_{counter}.{ext}", "wb"))
                counter += 1    

    def _get_abstract(self):
        page_1_text = unidecode(self.doc[0].get_text())
        start_idx = page_1_text.lower().find("abstract") + len("abstract")
        end_idx = page_1_text.lower().find(self.toc[0][1].lower())
        return page_1_text[start_idx:end_idx].replace("\n", " ")

    def summarize(self) -> None:

        summarized_doc = {}
        summarized_doc["Abstract"] = self._get_abstract()
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
        
        self._get_images()
        return summarized_doc
     
class PdfDoc(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
    
    def write(self, doc: Dict[str, str]):
        self._write_doc(doc)
        self._write_images()
    
    def _write_doc(self, doc: Dict[str, str]):
        for title in doc:
            text = doc[title]
            self.set_font("times", "B", size=16)
            self.cell(0, 15, text=title)
            self.ln()
            if len(text)>0:
                self.set_font("times", "", 12)
                self.multi_cell(0, 5, text=text)
                self.ln()
    
    def _write_images(self):
        self.add_page()
        self.set_font(family="helvetica", style="B", size=16)
        self.cell(0, 10, text="Figures", align="C")
        self.ln()
        counter = 1
        for _, _, files in os.walk("./images/"):
            for file in files:
                self.image(name=Image.open(f"./images/{file}"),
                        w=75,
                        h=75,
                        x=self.w/2 - 37.5)
                self.ln()
                self.set_font(family="times", style="I", size=10)
                self.cell(0, 5, text=f"Figure {counter}", align="C")
                self.ln(20)
                counter += 1
            
        shutil.rmtree("./images/")


def search_papers_with_field(field: str,
                             count: int=10) -> List[Dict[str, Any]]:
    search = arxiv.Search(
        query=field,
        max_results=count,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = arxiv.Client().results(search=search)
    results_dict = []
    for result in results:
        result_dict = {}
        result_dict["title"] = result.title
        result_dict["authors"] = result.authors
        result_dict["summary"] = result.summary
        results_dict.append(result_dict)
    
    return results_dict


def download_ref_papers(title: str):
    client = PapersWithCodeClient()
    papers = client.search(q=title)
    pdf_url = papers.results[0].paper.url_pdf
    response = requests.get(pdf_url)
    
    try:
        if response.status_code == 200:
            downloads_folder = str(Path.home() / "Downloads")        
            filename = pdf_url.split("/")[-1]        
            file_path = os.path.join(downloads_folder, filename)        
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            return False        

    except:
        return False


def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""
    for page_idx in range(len(doc)):
        text += unidecode(doc[page_idx].get_text())
    return text

if __name__ == "__main__":
    ds = DocumentSummarizer("test_file.pdf")
    doc = ds.summarize()
    pdf = PdfDoc(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.write(doc=doc)
    pdf.output("summarized_doc.pdf")