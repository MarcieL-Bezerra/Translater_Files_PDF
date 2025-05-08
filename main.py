import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from time import sleep
import threading
import asyncio

import translate 

main_color = '#3498db' # Azul
secondary_color = '#f1c40f' # Amarelo

def select_file():
    file = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    if file:
        print(file)
        txt_file.delete(0, tk.END)
        txt_file.insert(0, file)

def translate_file_progress():
    file = txt_file.get()
    language = variable.get()
    languages_translator = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt'
    }
    if file:
        progressbar.pack(pady=10)
        progressbar.start()
        language_translator = languages_translator.get(language)
        print(file)
        print(language_translator)
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(translate.translate_file(file, language_translator))
            if result == "Finished":
                messagebox.showinfo("Info", "Translation completed successfully!")
                progressbar.stop()
                progressbar.pack_forget()
                txt_file.delete(0, tk.END)
                return "Finished"
            else:
                messagebox.showerror("Error", "Error during translation")
                progressbar.stop()
                progressbar.pack_forget()
                return "Error"
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            progressbar.stop()
            progressbar.pack_forget()
            return "Error"
    else:
        messagebox.showerror("Error", "Please select a file")
        return "Error"

def translate_file():
    thread = threading.Thread(target=translate_file_progress)
    thread.start()

root = tk.Tk()
root.title("Translate Files PDF")
root.config(bg=main_color)

main_frame = tk.Frame(root, bg=main_color)
main_frame.pack(padx=10, pady=10)

lbl_title = tk.Label(main_frame, text="Translate Files PDF", font=("Arial", 18), bg=main_color, fg="#fff")
lbl_title.pack(pady=10)

btn_select_file = tk.Button(main_frame, text="Select PDF file", command=select_file, bg=secondary_color, fg="#fff")
btn_select_file.pack(pady=10)

txt_file = tk.Entry(main_frame, width=50)
txt_file.pack(pady=10)

languages = ['English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese']
variable = tk.StringVar(main_frame)
variable.set(languages[5]) # default value

option_language = tk.OptionMenu(main_frame, variable, *languages)
option_language.pack(pady=10)

progressbar = ttk.Progressbar(main_frame, orient='horizontal', length=200, mode='indeterminate')

btn_translate_file = tk.Button(main_frame, text="Translate PDF file", command=translate_file, bg=secondary_color, fg="#fff")
btn_translate_file.pack(pady=11)

root.mainloop()


# python -m PyInstaller --onefile --windowed --icon=img/Picture1.ico main.py