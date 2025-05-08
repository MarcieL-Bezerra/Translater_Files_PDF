import PyPDF2
from googletrans import Translator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import asyncio
from reportlab.lib.units import inch

async def translate_file(file_name, language):
    file_name = os.path.normpath(file_name)
    translator = Translator()
    with open(file_name, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        file_path, file_extension = os.path.splitext(file_name)
        new_file_name = f"{file_path}_trad{file_extension}"
        new_pdf = canvas.Canvas(new_file_name, pagesize=letter)
        y = 700

        for page in range(len(pdf.pages)):
            text = pdf.pages[page].extract_text()
            translated_text = await translator.translate(text, dest=language)
            lines = translated_text.text.split('\n')
            for line in lines:
                words = line.split()
                current_line = ''
                textobject = new_pdf.beginText(100, y)
                textobject.setFont('Helvetica', 12)
                for word in words:
                    if new_pdf.stringWidth(current_line + ' ' + word, 'Helvetica', 12) < 6 * inch:
                        current_line += ' ' + word if current_line else word
                    else:
                        textobject.textLine(current_line)
                        new_pdf.drawText(textobject)
                        y -= 20
                        if y < 100:
                            new_pdf.showPage()
                            y = 700
                        textobject = new_pdf.beginText(100, y)
                        textobject.setFont('Helvetica', 12)
                        current_line = word
                if current_line:
                    textobject.textLine(current_line)
                new_pdf.drawText(textobject)
                y -= 20
                if y < 100:
                    new_pdf.showPage()
                    y = 700
        new_pdf.save()
        return "Finished"

if __name__ == "__main__":
    asyncio.run(translate_file('my-file.pdf', 'pt'))
    print("Finished")