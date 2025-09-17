import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class AfrikaansSpellingGame:
    """
    A simple GUI-based spelling game for Afrikaans words.
    It displays an image and prompts the user to spell the object's name.
    """
    def __init__(self, master):
        self.master = master
        master.title("Afrikaanse Spel Speletjie 🇿🇦")
        master.geometry("500x550")
        master.configure(bg='#f0f8ff') # Light alice blue background

        # --- Data Loading ---
        # The dictionary will be populated from the 'images' folder.
        # Key: word (e.g., 'appel'), Value: file path (e.g., 'images/appel.png')
        self.words = {}
        self.load_words_from_folder('images')

        # Check if any images were loaded. If not, show an error and close.
        if not self.words:
            messagebox.showerror("Fout (Error)", 
                                 "Geen prente gevind in die 'images' gids nie.\n\n"
                                 "Please create an 'images' folder and add image files (.png, .jpg).")
            master.destroy()
            return

        self.current_word = None
        self.current_image_path = None

        # --- GUI Widgets ---
        self.title_label = tk.Label(master, text="Wat is hierdie?", font=("Helvetica", 24, "bold"), bg='#f0f8ff')
        self.title_label.pack(pady=10)

        # Label to display the image
        self.image_label = tk.Label(master, bg='#ffffff', relief="solid", borderwidth=1)
        self.image_label.pack(pady=10)

        # Label and Entry for user input
        self.entry_label = tk.Label(master, text="Tik jou antwoord hier:", font=("Helvetica", 14), bg='#f0f8ff')
        self.entry_label.pack(pady=(10, 5))

        self.entry = tk.Entry(master, font=("Helvetica", 16), width=20, justify='center')
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.check_spelling_event) # Bind Enter key

        # Button to check the answer
        self.check_button = tk.Button(master, text="Raai", font=("Helvetica", 14), command=self.check_spelling)
        self.check_button.pack(pady=10)

        # Label to show feedback (Correct/Incorrect)
        self.feedback_label = tk.Label(master, text="", font=("Helvetica", 14, "italic"), bg='#f0f8ff')
        self.feedback_label.pack(pady=10)

        # --- Start the Game ---
        self.next_word()

    def load_words_from_folder(self, folder_path):
        """Dynamically loads words and image paths from the specified folder."""
        if not os.path.exists(folder_path):
            return
        
        supported_extensions = ('.png', '.jpg', '.jpeg', '.gif')
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(supported_extensions):
                # The word is the filename without its extension (e.g., 'appel.png' -> 'appel')
                word = os.path.splitext(filename)[0]
                self.words[word] = os.path.join(folder_path, filename)

    def next_word(self):
        """Selects a new random word and displays its corresponding image."""
        # Randomly choose a word from the dictionary
        self.current_word, self.current_image_path = random.choice(list(self.words.items()))
        
        # Load, resize, and display the image
        try:
            img = Image.open(self.current_image_path)
            img = img.resize((300, 300), Image.LANCZOS)
            self.photo_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo_img)
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load image: {self.current_image_path}\n{e}")
            self.image_label.config(image=None, text=f"Kon nie beeld laai nie:\n{os.path.basename(self.current_image_path)}")

        # Clear the previous input and feedback message
        self.entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.entry.focus_set() # Put the cursor back in the text box

    def check_spelling_event(self, event):
        """Allows the Enter key to trigger the check."""
        self.check_spelling()

    def check_spelling(self):
        """Checks if the user's guess is correct."""
        user_guess = self.entry.get().strip().lower()

        if not user_guess:
            self.feedback_label.config(text="Tik asseblief 'n woord in.", fg="orange")
            return

        # Compare the guess with the correct answer (case-insensitive)
        if user_guess == self.current_word.lower():
            self.feedback_label.config(text="Reg! Mooi so! 🥳", fg="green")
            # Wait 1.5 seconds before showing the next word
            self.master.after(1500, self.next_word)
        else:
            feedback_text = f"Verkeerd. Die regte antwoord is '{self.current_word}'."
            self.feedback_label.config(text=feedback_text, fg="red")
            # Wait 2.5 seconds before showing the next word
            self.master.after(2500, self.next_word)


# --- Main execution block ---
if __name__ == "__main__":
    # This block runs when the script is executed directly
    root = tk.Tk()
    game_gui = AfrikaansSpellingGame(root)
    root.mainloop()