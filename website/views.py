from flask import Blueprint, render_template, request, send_file
from flask import redirect, url_for
from utils import DocumentSummarizer, PdfDoc
import io
import os

views = Blueprint("views", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')  # Define the uploads folder

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    pdf.save(pdf_path)
    summarized_pdf = summarize_utility(pdf_path)
    summarized_pdf_path = os.path.join(UPLOAD_FOLDER, f"summarized_{pdf.filename.split('.')[0]}.pdf")
    summarized_pdf.output(summarized_pdf_path)
    print(pdf.filename, pdf_path)
    # return redirect(url_for("views.view_pdf", filename=f"summarized_{pdf.filename.split('.')[0]}.pdf"))

    view_link = url_for('views.view_pdf', filename=f"summarized_{pdf.filename.split('.')[0]}.pdf")
    link_html = f'<a href="{view_link}" target="_blank">View Summarized PDF</a>'
    
    return f"Summarization completed! {link_html}"


@views.route("/view-pdf/<filename>")
def view_pdf(filename):
    print(filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, mimetype="application/pdf")