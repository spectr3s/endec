# endec - Encryption/Decryption Tool

A feature-rich encryption/decryption desktop application supporting Caesar Cipher and Vigenere Cipher with an intuitive GUI.

## Overview

**endec** is a Python-based encryption tool that provides a user-friendly interface for encrypting and decrypting text using classical cipher methods. It features a modern, responsive GUI built with Tkinter and supports both Caesar Cipher and Vigenere Cipher algorithms.

## Features

- **Multiple Cipher Methods**
  - **Caesar Cipher**: Shift-based character encryption (adjustable shift values)
  - **Vigenere Cipher**: Keyword-based polyalphabetic encryption (stronger security)

- **User-Friendly GUI**
  - Clean, intuitive interface built with Tkinter
  - Real-time cipher selection with dynamic field switching
  - Input/Output text areas with scrolling support
  - Status bar for operation feedback

- **Practical Utilities**
  - Encrypt/Decrypt toggle mode
  - Copy output to clipboard
  - Save encrypted/decrypted text to file
  - Clear all fields with one click
  - Input validation and error handling
  - Built-in usage examples

- **Quality Code**
  - Modular `CipherHandler` class for cipher logic
  - Type hints for better code clarity
  - Comprehensive error handling
  - Professional GUI layout with responsive grid system

## Quick Start

1. **Run the application:**
   ```bash
   python encryption_tool-1.py
   ```

2. **Select a cipher method** (Caesar or Vigenere)
3. **Choose your mode** (Encrypt or Decrypt)
4. **Enter your text** and cipher parameters (shift number or keyword)
5. **Click "Process"** to transform your text
6. **Copy or Save** the output as needed

## Usage Examples

- **Caesar Cipher**: Text "HELLO" with shift 3 → "KHOOR"
- **Vigenere Cipher**: Text "ATTACKATDAWN" with keyword "LEMON" → "LXFOPVEFRNHR"

## Build as Executable

Convert to standalone EXE file:
```bash
pyinstaller --onefile --windowed encryption_tool-1.py
```