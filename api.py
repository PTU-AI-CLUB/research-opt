from flask import Flask, request, jsonify
from utils import DocumentSummarizer, PdfDoc

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize_document():
    data = request.get_json()
    document_content = data.get('documentContent')
    summary = "This is a summary of the document."
    return jsonify({'summary': summary})

@app.route('/download-references', methods=['POST'])
def download_references():
    # Implement download reference logic here
    # Retrieve data from the request, process it, and return the result
    data = request.get_json()
    highlighted_references = data.get('highlightedReferences')
    # Perform download logic...
    # Return a link or the actual content of the downloaded references
    return jsonify({'downloadedReferences': "Download link or content"})

if __name__ == '__main__':
    app.run()
