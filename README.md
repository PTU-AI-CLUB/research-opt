# research-opt

research-opt is being developed as a browser extension that is used to optimize the researching paper reading experience of a researcher. In it's current stage research-opt is can 
summarize whole research papers and also download for you any research paper by passing just the title of the research paper.

## How to use
To summarize a document:
```python
ds = DocumentSummarizer("test_file.pdf")
doc = ds.summarize()
pdf = PdfDoc(orientation="P", unit="mm", format="letter")
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.write(doc=doc)
pdf.output("summarized_doc.pdf")
```

To download a research paper
```python
download_ref_papers(title="Attention is all you need")
```

To know about a researcher
```python
print(get_author_details(auth_name="Ilya Sutskever"))
```

## Future updates
In future iterations the backend code will be more user friendly. <br>
The next stage in the pipeline is to integrate these features with a browser extension
