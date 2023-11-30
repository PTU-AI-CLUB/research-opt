import re
import PyPDF2
import fitz

def extract_blocks(pdf_file):
  """Extracts blocks from a PDF file.

  Args:
    pdf_file: The path to the PDF file.

  Returns:
    A list of blocks.
  """

  doc = fitz.open(pdf_file)
  blocks = []
  for page in doc:
    for block in page.get_text("blocks"):
      blocks.append(block[4])
  return blocks


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        all_text = ''
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            all_text += page.extractText()
    return all_text

def count_numbers_in_square_brackets(text):
    pattern = r'\[(.*?)\]'  
    matches = re.findall(pattern, text)
    numbers = []
    for match in matches:
        if ',' in match:
            numbers.extend(match.split(','))
        else:
            numbers.append(match)  
    numbers = [int(num.strip()) for num in numbers if num.strip().isdigit()]  
    frequency = {}
    for number in numbers:
        if number in frequency:
            frequency[number] += 1
        else:
            frequency[number] = 1
    return sorted(frequency.items(), key=lambda k:-k[1])

if __name__ == "__main__":
    pdf_file = "test_pdf.pdf"
    blocks = extract_blocks(pdf_file)
    print(blocks)
    