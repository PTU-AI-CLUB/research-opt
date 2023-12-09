from flask import Blueprint, render_template, request, send_file
from utils import DocumentSummarizer, PdfDoc
import io

views = Blueprint("views", __name__)

def summarize_utility(pdf_path):
    ds = DocumentSummarizer(pdf_path)
    doc = ds.summarize()
    pdf = PdfDoc(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.write(doc=doc)
    return pdf


@views.route("/")
def home():
    return render_template("base.html")

@views.route("/summarize", methods=["POST"])
def summarize():
    if "pdf_file" not in request.files:
        return "<h1>No file part</h1>"
    
    pdf = request.files["pdf_file"]

    if pdf.filename == '':
        return "No selected file"
    
    pdf_path = f"./uploads/{pdf.filename}"
    pdf.save(pdf_path)

    summarized_pdf = summarize_utility(pdf_path)
    output_pdf = io.BytesIO()
    summarized_pdf.output(output_pdf)
    output_pdf.seek(0)
    print(pdf.filename, pdf_path)
    return send_file(output_pdf, as_attachment=True, download_name="summarized.pdf")