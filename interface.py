from tkinter import *
from tkinter import filedialog, messagebox
import fitz
import voicerss_tts
import os

TITLE_FONT = ("Times New Roman", 18, "bold")
BUTTON_FONT = ("Times New Roman", 14, "bold")


class Screen(Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF to MP3 Converter")
        self.config(padx=10, pady=10)
        self.app_label = Label(master=self, text="PDF to MP3 Converter", font=TITLE_FONT)
        self.description = Label(master=self, text="File must be less than 25KB.")
        self.upload_button = Button(master=self, text="Upload PDF", font=BUTTON_FONT, command=self.upload_pdf)
        self.convert_button = Button(master=self, text="Convert", font=BUTTON_FONT, state=DISABLED)
        self.save_button = Button(master=self, text="Save", font=BUTTON_FONT, state=DISABLED)
        self.file_path = None
        self.file = None
        self.binary_data = None
        self.text = ""
        self.file_size = None
        self.setup_screen()
        self.mainloop()

    def setup_screen(self):
        self.app_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        self.upload_button.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
        self.description.grid(row=2, column=0, columnspan=2)
        self.convert_button.grid(row=5, column=0, padx=20, pady=20)
        self.save_button.grid(row=5, column=1, padx=20, pady=20)

    def upload_pdf(self):
        self.file_path = filedialog.askopenfilename(initialdir="/", title="Select File",
                                                    filetypes=[("PDF files", "*.pdf")])
        self.convert_button.config(state=NORMAL, command=self.convert_to_mp3)
        self.file = fitz.open(self.file_path)
        for page in self.file:
            self.text += page.get_text()
        self.file_size = os.path.getsize(self.file_path) / 1000
        size_label = Label(master=self, text=f"Size: {self.file_size} KB")
        size_label.grid(row=3, column=0, columnspan=2)
        file_name = Label(master=self, text=f"{self.file_path}")
        file_name.grid(row=4, column=0, columnspan=2)

    def convert_to_mp3(self):
        if self.file_size < 25:
            voice = voicerss_tts.speech({
                'key': '1db9298eb4f24853aaac7c36b7dc33bf',
                'hl': 'en-gb',
                'src': self.text,
                'r': '0',
                'c': 'mp3',
                "v": "Nancy",
                "f": "48khz_16bit_stereo"
            })
            self.binary_data = voice["response"]
            if len(self.binary_data) < 5:
                messagebox.showerror(title="Error",
                                     message="The file you chose is too large, please upload a smaller file.")
            else:
                file_converted_label = Label(master=self, text="File successfully converted.")
                file_converted_label.grid(row=6, column=0, columnspan=2)
                self.save_button.config(state=NORMAL, command=self.save_mp3)
        else:
            messagebox.showerror(title="Error",
                                 message="The file you chose is too large, please upload a smaller file.")

    def save_mp3(self):
        short_name = self.file_path.split("/")
        short_name = short_name[len(short_name) - 1].split(".")[0]
        output_file = f"mp3/{short_name}.mp3"
        with open(output_file, "wb") as file:
            file.write(self.binary_data)
        save_label = Label(master=self, text=f"File has been saved as {short_name}.mp3 in mp3 folder.")
        save_label.grid(row=7, column=0, columnspan=2)
