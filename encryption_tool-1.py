"""
Encryption / Decryption Tool
Supports:
- Caesar Cipher
- Vigenere Cipher

Features:
- GUI (Tkinter)
- Encrypt / Decrypt
- Copy result
- Save result to a text file
- Input validation and status messages

Run:
    python encryption_tool.py
"""

from __future__ import annotations

import string
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def caesar_encrypt(text: str, shift: int) -> str:
    shift %= 26
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


def clean_vigenere_key(key: str) -> str:
    return "".join(ch for ch in key if ch.isalpha()).upper()


def vigenere_encrypt(text: str, key: str) -> str:
    key = clean_vigenere_key(key)
    if not key:
        raise ValueError("Vigenere keyword must contain at least one letter.")

    out = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord("A")
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


def vigenere_decrypt(text: str, key: str) -> str:
    key = clean_vigenere_key(key)
    if not key:
        raise ValueError("Vigenere keyword must contain at least one letter.")

    out = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord("A")
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


class EncryptionToolApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Encryption / Decryption Tool")
        self.geometry("860x700")
        self.minsize(780, 620)

        self.cipher_var = tk.StringVar(value="Caesar Cipher")
        self.mode_var = tk.StringVar(value="Encrypt")
        self.shift_var = tk.StringVar(value="3")
        self.key_var = tk.StringVar(value="KEY")
        self.status_var = tk.StringVar(value="Ready.")

        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self, padding=(18, 18, 18, 8))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text="Encryption / Decryption Tool",
            font=("Segoe UI", 20, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            header,
            text="Choose Caesar or Vigenere, then encrypt or decrypt your text.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        body = ttk.Frame(self, padding=18)
        body.grid(row=1, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(3, weight=1)

        settings = ttk.LabelFrame(body, text="Controls", padding=14)
        settings.grid(row=0, column=0, columnspan=2, sticky="ew")
        settings.columnconfigure(1, weight=1)

        ttk.Label(settings, text="Cipher:").grid(row=0, column=0, sticky="w", pady=5)
        cipher_combo = ttk.Combobox(
            settings,
            textvariable=self.cipher_var,
            values=["Caesar Cipher", "Vigenere Cipher"],
            state="readonly",
            width=24,
        )
        cipher_combo.grid(row=0, column=1, sticky="w", pady=5)
        cipher_combo.bind("<<ComboboxSelected>>", lambda _e: self._refresh_fields())

        ttk.Label(settings, text="Mode:").grid(row=1, column=0, sticky="w", pady=5)
        mode_frame = ttk.Frame(settings)
        mode_frame.grid(row=1, column=1, sticky="w", pady=5)
        ttk.Radiobutton(mode_frame, text="Encrypt", variable=self.mode_var, value="Encrypt").pack(side="left", padx=(0, 14))
        ttk.Radiobutton(mode_frame, text="Decrypt", variable=self.mode_var, value="Decrypt").pack(side="left")

        self.shift_label = ttk.Label(settings, text="Shift:")
        self.shift_entry = ttk.Entry(settings, textvariable=self.shift_var, width=30)

        self.key_label = ttk.Label(settings, text="Keyword:")
        self.key_entry = ttk.Entry(settings, textvariable=self.key_var, width=30)

        ttk.Label(settings, text="Tip: Caesar uses a number. Vigenere uses a word.").grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(6, 0)
        )

        input_frame = ttk.LabelFrame(body, text="Input Text", padding=14)
        input_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(14, 0))
        input_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)

        self.input_text = tk.Text(input_frame, wrap="word", height=14)
        self.input_text.grid(row=0, column=0, sticky="nsew")
        input_scroll = ttk.Scrollbar(input_frame, orient="vertical", command=self.input_text.yview)
        input_scroll.grid(row=0, column=1, sticky="ns")
        self.input_text.configure(yscrollcommand=input_scroll.set)

        output_frame = ttk.LabelFrame(body, text="Output Text", padding=14)
        output_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(14, 0))
        output_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, wrap="word", height=14)
        self.output_text.grid(row=0, column=0, sticky="nsew")
        output_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        output_scroll.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=output_scroll.set)

        buttons = ttk.Frame(body)
        buttons.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        buttons.columnconfigure((0, 1, 2, 3), weight=1)

        ttk.Button(buttons, text="Process", command=self.process_text).grid(row=0, column=0, sticky="ew", padx=4)
        ttk.Button(buttons, text="Clear", command=self.clear_all).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(buttons, text="Copy Output", command=self.copy_output).grid(row=0, column=2, sticky="ew", padx=4)
        ttk.Button(buttons, text="Save Output", command=self.save_output).grid(row=0, column=3, sticky="ew", padx=4)

        examples = ttk.LabelFrame(body, text="Examples", padding=14)
        examples.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        ttk.Label(
            examples,
            text=(
                "Caesar example: HELLO with shift 3 -> KHOOR\n"
                "Vigenere example: ATTACKATDAWN with keyword LEMON -> LXFOPVEFRNHR"
            ),
            justify="left",
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding=(10, 4)).grid(
            row=2, column=0, sticky="ew"
        )

        self._refresh_fields()

    def _refresh_fields(self) -> None:
        cipher = self.cipher_var.get()
        self.shift_label.grid_remove()
        self.shift_entry.grid_remove()
        self.key_label.grid_remove()
        self.key_entry.grid_remove()

        if cipher == "Caesar Cipher":
            self.shift_label.grid(row=2, column=0, sticky="w", pady=5)
            self.shift_entry.grid(row=2, column=1, sticky="w", pady=5)
            self.status_var.set("Caesar Cipher selected.")
        else:
            self.key_label.grid(row=2, column=0, sticky="w", pady=5)
            self.key_entry.grid(row=2, column=1, sticky="w", pady=5)
            self.status_var.set("Vigenere Cipher selected.")

    def _get_input(self) -> str:
        return self.input_text.get("1.0", "end-1c")

    def _set_output(self, text: str) -> None:
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)

    def process_text(self) -> None:
        text = self._get_input()
        if not text.strip():
            messagebox.showwarning("Missing input", "Please enter some text first.")
            return

        cipher = self.cipher_var.get()
        mode = self.mode_var.get()

        try:
            if cipher == "Caesar Cipher":
                try:
                    shift = int(self.shift_var.get().strip())
                except ValueError:
                    raise ValueError("Caesar shift must be a whole number.")

                result = caesar_encrypt(text, shift) if mode == "Encrypt" else caesar_decrypt(text, shift)
            else:
                key = self.key_var.get().strip()
                result = vigenere_encrypt(text, key) if mode == "Encrypt" else vigenere_decrypt(text, key)

            self._set_output(result)
            self.status_var.set(f"{mode}ed successfully using {cipher}.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.status_var.set("Error occurred.")

    def clear_all(self) -> None:
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.shift_var.set("3")
        self.key_var.set("KEY")
        self.mode_var.set("Encrypt")
        self.cipher_var.set("Caesar Cipher")
        self._refresh_fields()
        self.status_var.set("Cleared.")

    def copy_output(self) -> None:
        output = self.output_text.get("1.0", "end-1c")
        if not output.strip():
            messagebox.showinfo("Nothing to copy", "There is no output text yet.")
            return
        self.clipboard_clear()
        self.clipboard_append(output)
        self.status_var.set("Output copied to clipboard.")

    def save_output(self) -> None:
        output = self.output_text.get("1.0", "end-1c")
        if not output.strip():
            messagebox.showinfo("Nothing to save", "There is no output text yet.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Output",
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(output)

        self.status_var.set(f"Output saved to {path}.")


def main() -> None:
    app = EncryptionToolApp()
    app.mainloop()


if __name__ == "__main__":
    main()
