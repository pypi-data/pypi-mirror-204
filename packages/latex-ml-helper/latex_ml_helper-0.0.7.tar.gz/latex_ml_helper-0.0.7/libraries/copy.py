import pyperclip

def copy_text(text, copy = False):
    if copy:
        pyperclip.copy(text)
        return "Copyed to clipboard"
    else:
        return text