import PyPDF2
from googletrans import Translator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import asyncio

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
                new_pdf.setFont('Helvetica', 12)
                new_pdf.drawString(100, y, line)
                y -= 20
                if y < 100:
                    new_pdf.showPage()
                    y = 700
        new_pdf.save()
    return "Finished"

if __name__ == "__main__":
    asyncio.run(translate_file('my-file.pdf', 'pt'))
    print("Finished")