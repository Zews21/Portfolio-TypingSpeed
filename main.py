import tkinter as tk
import UI


class TypingSpeedApp(tk.Tk):
    """
    A class representing the main application window for the Typing Speed App.
    Inherits from tk.Tk.
    """
    def __init__(self):
        """
        Initializes the main application window and sets up the UI components.
        """
        super().__init__()

        # Configure the main window
        self.title("Typing Speed App")  # Set the window title
        self.geometry("800x600")  # Set the window size
        self.config(padx=100, pady=100)  # Add padding around the content

        # Create and display the SentenceDisplay and TypingArea components
        self.sentence_display = UI.SentenceDisplay(self)  # Display a random sentence
        self.input_area = UI.TypingArea(self, self.sentence_display)  # Typing area with timer and accuracy checking

        # Arrange the components in a grid layout
        self.sentence_display.grid(column=1, row=1)
        self.input_area.grid(column=1, row=2)

        # Start the Tkinter event loop
        self.mainloop()


if __name__ == "__main__":
    # Entry point for the application. Create an instance of TypingSpeedApp and start the main loop.
    app = TypingSpeedApp()
    app.mainloop()



