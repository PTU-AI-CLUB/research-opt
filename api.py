from flask import Flask, request, jsonify
from utils import DocumentSummarizer, PdfDoc
import os

app = Flask(__name__)

@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    data = request.get_json()
    print("Here")
    if 'filePath' in data:
        pdf_url = data['filePath']
        ds = DocumentSummarizer(path=pdf_url)
        doc = ds.summarize()
        pdf = PdfDoc(orientation="P", unit="mm", format="letter")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.write(doc=doc)
        
        os_name = os.name

        if os_name == 'posix':  # For Unix-based systems like Linux or macOS
            downloads_path = os.path.expanduser('~/Downloads')
        elif os_name == 'nt':  # For Windows
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        
        pdf.output(downloads_path)


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
