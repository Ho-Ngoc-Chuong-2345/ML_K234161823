import tkinter as tk
from tkinter import ttk
import requests

class TextTranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Text Translator (OpenRouter)")

        self.create_widgets()

    def create_widgets(self):
        label1 = tk.Label(self.root, text="Enter text to translate:")
        label1.grid(row=0, column=0, padx=10, pady=10)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.grid(row=0, column=1, padx=10, pady=10)

        label2 = tk.Label(self.root, text="Choose source language:")
        label2.grid(row=1, column=0, padx=10, pady=10)

        self.source_lang = ttk.Combobox(self.root, values=["en", "es", "fr", "vi", "ja", "zh-cn"])
        self.source_lang.set("en")
        self.source_lang.grid(row=1, column=1, padx=10, pady=10)

        label3 = tk.Label(self.root, text="Choose target language:")
        label3.grid(row=2, column=0, padx=10, pady=10)

        self.target_lang = ttk.Combobox(self.root, values=["en", "es", "fr", "vi", "ja", "zh-cn"])
        self.target_lang.set("vi")
        self.target_lang.grid(row=2, column=1, padx=10, pady=10)

        translate_button = tk.Button(self.root, text="Translate", command=self.translate_text)
        translate_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self.root, text="Translated text will appear here.", wraplength=400, justify="left")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def translate_text(self):
        api_key = "YOUR_OPENROUTER_API_KEY"   # 🔹 ĐIỀN API KEY Ở ĐÂY
        text_to_translate = self.entry.get()
        src = self.source_lang.get()
        dest = self.target_lang.get()

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer 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",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-3.5-turbo",  # bạn có thể đổi sang "gpt-4", "mistral", v.v.
            "messages": [
                {"role": "system", "content": f"You are a translator. Translate the following text from {src} to {dest}."},
                {"role": "user", "content": text_to_translate},
            ],
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            translated = result["choices"][0]["message"]["content"]
            self.result_label.config(text=translated)
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextTranslatorApp(root)
    root.mainloop()
