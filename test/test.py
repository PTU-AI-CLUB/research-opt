import re
import PyPDF2
import fitz

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
  doc = fitz.open("test1.pdf")
  text = ""
  for i in range(len(doc)):
      text += doc[i].get_text()

  print(count_numbers_in_square_brackets(text=text))   