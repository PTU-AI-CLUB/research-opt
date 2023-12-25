from flask import Blueprint, render_template, request, send_file, send_from_directory
from flask import redirect, url_for, session, jsonify
from utils import *
import io
import os


views = Blueprint("views", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')  # Define the uploads folder
ALLOWED_EXTENSIONS = {"pdf"}


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(file_name: str):
    for ext in ALLOWED_EXTENSIONS:
        if file_name.endswith(ext):
            return True
    return False

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
    return render_template("index.html")

@views.route("/summarize_page", methods=["GET", "POST"])
def summarize_page():
    return render_template("summarize.html")
@views.route("/search_page")
def search_page():
    return render_template("search.html")

@views.route("/summarize", methods=["GET", "POST"])
def summarize():
    if "pdf_file" not in request.files:
        return redirect(request.url)
    
    pdf = request.files["pdf_file"]

    if pdf.filename == '':
        return redirect(request.url)

    if pdf and allowed_file(pdf.filename):

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        pdf.save(pdf_path)
        summarized_pdf = summarize_utility(pdf_path)
        summarized_pdf_path = os.path.join(UPLOAD_FOLDER, f"summarized_{pdf.filename.split('.')[0]}.pdf")
        summarized_pdf.output(summarized_pdf_path)
        summarized_pdf_path = url_for("views.uploaded_file", filename=f"summarized_{pdf.filename.split('.')[0]}.pdf")
        return render_template("summarize.html", summarized_pdf=summarized_pdf_path)

    return redirect(request.url)

@views.route("/view-pdf/<filename>")
def view_pdf(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, mimetype="application/pdf")

@views.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@views.route("/search_papers_related_to_field", methods=["GET", "POST"])
def search_papers_related_to_field():
    field_of_science = request.args.get("field_of_science", "")
    print(field_of_science)
    search_results = None
    if field_of_science:
        search_results = search_papers_with_field(field=field_of_science)
    return render_template("search.html", search_results=search_results)



@views.route("/download_ref_paper", methods=["POST"])
def download_ref_paper():
    data = request.get_json()
    paper_title = data.get("paper")
    is_downloaded = download_ref_papers(paper_title)
    if is_downloaded:
        return jsonify({"message" : "Downloaded successfully"})
    return jsonify({"message" : "could not be downloaded"})