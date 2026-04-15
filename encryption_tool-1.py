"""
Encryption / Decryption Tool - Improved Version
Supports: Caesar Cipher and Vigenere Cipher
Features: GUI (Tkinter), Encrypt/Decrypt, Copy, Save, Input Validation

Run: python encryption_tool_improved.py
Build EXE: pyinstaller --onefile --windowed encryption_tool_improved.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable


# ============================================================================
# CIPHER LOGIC - Modular and Optimized
# ============================================================================

class CipherHandler:
    """Handles encryption and decryption for Caesar and Vigenere ciphers."""
    
    ALPHABET_SIZE = 26
    
    @staticmethod
    def _shift_char(char: str, shift: int, base: int) -> str:
        """Shift a single character by the given amount."""
        return chr((ord(char) - base + shift) % CipherHandler.ALPHABET_SIZE + base)
    
    @staticmethod
    def caesar(text: str, shift: int, encrypt: bool = True) -> str:
        """
        Caesar cipher encryption/decryption.
        
        Args:
            text: Input text
            shift: Number of positions to shift
            encrypt: True for encrypt, False for decrypt
            
        Returns:
            Encrypted/decrypted text
        """
        shift = shift % CipherHandler.ALPHABET_SIZE
        if not encrypt:
            shift = -shift
        
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(CipherHandler._shift_char(char, shift, base))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def _clean_key(key: str) -> str:
        """Extract only alphabetic characters from key and convert to uppercase."""
        return ''.join(char for char in key if char.isalpha()).upper()
    
    @staticmethod
    def vigenere(text: str, key: str, encrypt: bool = True) -> str:
        """
        Vigenere cipher encryption/decryption.
        
        Args:
            text: Input text
            key: Keyword for encryption
            encrypt: True for encrypt, False for decrypt
            
        Returns:
            Encrypted/decrypted text
            
        Raises:
            ValueError: If key contains no alphabetic characters
        """
        key = CipherHandler._clean_key(key)
        if not key:
            raise ValueError("Keyword must contain at least one letter.")
        
        result = []
        key_index = 0
        
        for char in text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                if not encrypt:
                    shift = -shift
                
                base = ord('A') if char.isupper() else ord('a')
                result.append(CipherHandler._shift_char(char, shift, base))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)


# ============================================================================
# GUI APPLICATION
# ============================================================================

class EncryptionApp(tk.Tk):
    """Main application window for encryption/decryption tool."""
    
    # Default values
    DEFAULT_SHIFT = 3
    DEFAULT_KEY = "KEY"
    WINDOW_SIZE = "860x700"
    WINDOW_MIN_SIZE = (780, 620)
    
    def __init__(self):
        super().__init__()
        self.title("Encryption / Decryption Tool")
        self.geometry(self.WINDOW_SIZE)
        self.minsize(*self.WINDOW_MIN_SIZE)
        
        # Initialize variables
        self._init_variables()
        self._build_ui()
    
    def _init_variables(self) -> None:
        """Initialize StringVar variables for GUI bindings."""
        self.cipher_var = tk.StringVar(value="Caesar Cipher")
        self.mode_var = tk.StringVar(value="Encrypt")
        self.shift_var = tk.StringVar(value=str(self.DEFAULT_SHIFT))
        self.key_var = tk.StringVar(value=self.DEFAULT_KEY)
        self.status_var = tk.StringVar(value="Ready.")
    
    def _build_ui(self) -> None:
        """Construct the user interface."""
        self._configure_grid()
        self._build_header()
        self._build_body()
        self._build_status_bar()
    
    def _configure_grid(self) -> None:
        """Configure grid weights for responsive layout."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
    
    def _build_header(self) -> None:
        """Build the application header section."""
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
            text="Select a cipher method and encrypt or decrypt your text.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))
    
    def _build_body(self) -> None:
        """Build the main body with controls, text areas, and buttons."""
        body = ttk.Frame(self, padding=18)
        body.grid(row=1, column=0, sticky="nsew")
        body.columnconfigure((0, 1), weight=1)
        body.rowconfigure(3, weight=1)
        
        self._build_controls(body)
        self._build_text_areas(body)
        self._build_buttons(body)
        self._build_examples(body)
    
    def _build_controls(self, parent: ttk.Frame) -> None:
        """Build cipher and mode selection controls."""
        controls = ttk.LabelFrame(parent, text="Controls", padding=14)
        controls.grid(row=0, column=0, columnspan=2, sticky="ew")
        controls.columnconfigure(1, weight=1)
        
        # Cipher selection
        ttk.Label(controls, text="Cipher:").grid(row=0, column=0, sticky="w", pady=5)
        cipher_combo = ttk.Combobox(
            controls,
            textvariable=self.cipher_var,
            values=["Caesar Cipher", "Vigenere Cipher"],
            state="readonly",
            width=24,
        )
        cipher_combo.grid(row=0, column=1, sticky="w", pady=5)
        cipher_combo.bind("<<ComboboxSelected>>", lambda _: self._refresh_fields())
        
        # Mode selection
        ttk.Label(controls, text="Mode:").grid(row=1, column=0, sticky="w", pady=5)
        mode_frame = ttk.Frame(controls)
        mode_frame.grid(row=1, column=1, sticky="w", pady=5)
        ttk.Radiobutton(mode_frame, text="Encrypt", variable=self.mode_var, value="Encrypt").pack(side="left", padx=(0, 14))
        ttk.Radiobutton(mode_frame, text="Decrypt", variable=self.mode_var, value="Decrypt").pack(side="left")
        
        # Dynamic fields (shown/hidden based on cipher selection)
        self.shift_label = ttk.Label(controls, text="Shift:")
        self.shift_entry = ttk.Entry(controls, textvariable=self.shift_var, width=30)
        
        self.key_label = ttk.Label(controls, text="Keyword:")
        self.key_entry = ttk.Entry(controls, textvariable=self.key_var, width=30)
        
        ttk.Label(controls, text="💡 Tip: Caesar uses a number. Vigenere uses a word.").grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(6, 0)
        )
        
        self._refresh_fields()
    
    def _build_text_areas(self, parent: ttk.Frame) -> None:
        """Build input and output text areas with scrollbars."""
        # Input text area
        input_frame = ttk.LabelFrame(parent, text="Input Text", padding=14)
        input_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(14, 0))
        input_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)
        
        self.input_text = tk.Text(input_frame, wrap="word", height=14, font=("Courier", 10))
        self.input_text.grid(row=0, column=0, sticky="nsew")
        input_scroll = ttk.Scrollbar(input_frame, orient="vertical", command=self.input_text.yview)
        input_scroll.grid(row=0, column=1, sticky="ns")
        self.input_text.configure(yscrollcommand=input_scroll.set)
        
        # Output text area
        output_frame = ttk.LabelFrame(parent, text="Output Text", padding=14)
        output_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(14, 0))
        output_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_text = tk.Text(output_frame, wrap="word", height=14, font=("Courier", 10))
        self.output_text.grid(row=0, column=0, sticky="nsew")
        output_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        output_scroll.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=output_scroll.set)
    
    def _build_buttons(self, parent: ttk.Frame) -> None:
        """Build action buttons."""
        buttons = ttk.Frame(parent)
        buttons.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        buttons.columnconfigure((0, 1, 2, 3), weight=1)
        
        button_specs = [
            ("Process", self.process_text),
            ("Clear", self.clear_all),
            ("Copy Output", self.copy_output),
            ("Save Output", self.save_output),
        ]
        
        for idx, (text, command) in enumerate(button_specs):
            ttk.Button(buttons, text=text, command=command).grid(
                row=0, column=idx, sticky="ew", padx=4
            )
    
    def _build_examples(self, parent: ttk.Frame) -> None:
        """Build examples section."""
        examples = ttk.LabelFrame(parent, text="Examples", padding=14)
        examples.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        
        example_text = (
            "Caesar: 'HELLO' with shift 3 → 'KHOOR'\n"
            "Vigenere: 'ATTACKATDAWN' with keyword 'LEMON' → 'LXFOPVEFRNHR'"
        )
        ttk.Label(examples, text=example_text, justify="left").grid(row=0, column=0, sticky="w")
    
    def _build_status_bar(self) -> None:
        """Build status bar at the bottom."""
        ttk.Label(
            self,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=(10, 4)
        ).grid(row=2, column=0, sticky="ew")
    
    def _refresh_fields(self) -> None:
        """Show/hide fields based on selected cipher."""
        cipher = self.cipher_var.get()
        
        # Hide all dynamic fields
        self.shift_label.grid_remove()
        self.shift_entry.grid_remove()
        self.key_label.grid_remove()
        self.key_entry.grid_remove()
        
        # Show relevant field
        if cipher == "Caesar Cipher":
            self.shift_label.grid(row=2, column=0, sticky="w", pady=5)
            self.shift_entry.grid(row=2, column=1, sticky="w", pady=5)
            self.status_var.set("Caesar Cipher selected.")
        else:
            self.key_label.grid(row=2, column=0, sticky="w", pady=5)
            self.key_entry.grid(row=2, column=1, sticky="w", pady=5)
            self.status_var.set("Vigenere Cipher selected.")
    
    def _get_input(self) -> str:
        """Get text from input area."""
        return self.input_text.get("1.0", "end-1c")
    
    def _set_output(self, text: str) -> None:
        """Set text in output area."""
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
    
    def process_text(self) -> None:
        """Process text based on selected cipher and mode."""
        text = self._get_input()
        
        if not text.strip():
            messagebox.showwarning("Missing Input", "Please enter some text first.")
            return
        
        cipher = self.cipher_var.get()
        mode = self.mode_var.get()
        encrypt = mode == "Encrypt"
        
        try:
            if cipher == "Caesar Cipher":
                try:
                    shift = int(self.shift_var.get().strip())
                except ValueError:
                    raise ValueError("Shift value must be a whole number.")
                
                result = CipherHandler.caesar(text, shift, encrypt)
            else:
                key = self.key_var.get().strip()
                result = CipherHandler.vigenere(text, key, encrypt)
            
            self._set_output(result)
            self.status_var.set(f"✓ {mode}ed successfully using {cipher}.")
        
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self.status_var.set("✗ Error occurred.")
    
    def clear_all(self) -> None:
        """Clear all input/output and reset to defaults."""
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.shift_var.set(str(self.DEFAULT_SHIFT))
        self.key_var.set(self.DEFAULT_KEY)
        self.mode_var.set("Encrypt")
        self.cipher_var.set("Caesar Cipher")
        self._refresh_fields()
        self.status_var.set("Cleared.")
    
    def copy_output(self) -> None:
        """Copy output text to clipboard."""
        output = self.output_text.get("1.0", "end-1c")
        
        if not output.strip():
            messagebox.showinfo("No Output", "Generate output first before copying.")
            return
        
        self.clipboard_clear()
        self.clipboard_append(output)
        self.status_var.set("✓ Copied to clipboard.")
    
    def save_output(self) -> None:
        """Save output text to a file."""
        output = self.output_text.get("1.0", "end-1c")
        
        if not output.strip():
            messagebox.showinfo("No Output", "Generate output first before saving.")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Output",
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(output)
            self.status_var.set(f"✓ Saved to {filepath}")
        except Exception as error:
            messagebox.showerror("Save Error", f"Could not save file: {error}")
            self.status_var.set("✗ Save failed.")


# ============================================================================
# ENTRY POINT
# ============================================================================

def main() -> None:
    """Launch the application."""
    app = EncryptionApp()
    app.mainloop()


if __name__ == "__main__":
    main()
