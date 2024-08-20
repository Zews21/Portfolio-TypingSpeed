import data
import random
import tkinter as tk


class SentenceDisplay(tk.Frame):
    """
    A class to display a random sentence for the user to type.
    Inherits from tk.Frame.
    """

    def __init__(self, parent):
        """
        Initializes the SentenceDisplay frame with a sentence label.

        Args:
            parent: The parent widget that contains this frame.
        """
        super().__init__(parent)
        self.parent = parent
        self.sentence_list = data.sentences  # List of sentences from the data module
        self.sentence_label = tk.Label(parent, font=("Arial", 20))  # Label to display the sentence
        self.sentence_label.grid(column=1, row=0, pady=30)
        self.display_sentence()  # Display a random sentence when initialized

    def get_random_sentence(self):
        """
        Returns a random sentence from the sentence list.

        Returns:
            str: A randomly selected sentence from the list.
        """
        return random.choice(self.sentence_list)

    def display_sentence(self):
        """
        Displays a random sentence in the sentence label.
        """
        sentence = self.get_random_sentence()
        self.sentence_label.config(text=sentence)

    def get_sentence(self):
        """
        Retrieves the current sentence displayed in the sentence label.

        Returns:
            str: The text of the sentence currently displayed.
        """
        return self.sentence_label.cget("text")


class TypingArea(tk.Frame):
    """
    A class representing the typing area where the user types the sentence.
    Also includes functionality for timer, accuracy calculation, and WPM calculation.
    Inherits from tk.Frame.
    """

    def __init__(self, parent, sentence_display):
        """
        Initializes the TypingArea frame with an input area, labels, and a restart button.

        Args:
            parent: The parent widget that contains this frame.
            sentence_display: The SentenceDisplay object to retrieve sentences from.
        """
        super().__init__(parent)
        self.parent = parent
        self.sentence_display = sentence_display  # Reference to the SentenceDisplay instance

        # Timer-related attributes
        self.timer_running = False  # Flag to indicate if the timer is running
        self.time_elapsed = 0  # Total time elapsed in seconds
        self.timer_id = None  # ID of the scheduled timer event

        # Typing input area
        self.input_area = tk.Entry(self, width=30, font=("Arial", 20))  # Text entry for user input
        self.input_area.grid(column=1, row=1, pady=20)
        self.input_area.bind("<KeyRelease>", self.check_accuracy)  # Bind key release event to check accuracy
        self.input_area.bind("<FocusIn>", self.start_timer)  # Bind focus event to start timer

        # Labels for accuracy, timer, and WPM
        self.accuracy_label = tk.Label(self, text="Accuracy: 100%", font=("Arial", 16))
        self.accuracy_label.grid(column=2, row=1, padx=20)

        self.timer_label = tk.Label(self, text="Time: 0s", font=("Arial", 16))
        self.timer_label.grid(column=2, row=0, padx=20)

        self.wpm_label = tk.Label(self, text="WPM: 0.00", font=("Arial", 16))
        self.wpm_label.grid(column=2, row=2, padx=20)

        # Restart button to reset the program
        self.restart_button = tk.Button(self, text="Restart", command=self.restart_program)
        self.restart_button.grid(column=1, row=3, pady=20)

    def check_accuracy(self, event=None):
        """
        Checks the user's input for accuracy compared to the displayed sentence.
        Also calculates and updates the WPM and stops the timer if accuracy reaches 100%.

        Args:
            event: The event that triggers this method (usually a key release event).
        """
        input_text = self.input_area.get()  # Get the text the user has typed
        sentence = self.sentence_display.get_sentence()  # Get the displayed sentence

        correct_chars = 0
        for i, char in enumerate(input_text):
            if i < len(sentence) and char == sentence[i]:  # Compare each character
                correct_chars += 1

            # Calculate and display the accuracy
            accuracy_score = (correct_chars / len(sentence)) * 100 if sentence else 0
            self.accuracy_label.config(text=f"Accuracy: {accuracy_score:.2f}%")

            if accuracy_score == 100:  # Stop the timer and calculate WPM when accuracy reaches 100%
                self.stop_timer()
                self.calculate_wpm(input_text)

        # Continuously calculate WPM as user types
        self.calculate_wpm(input_text)

    def start_timer(self, event=None):
        """
        Starts the timer if it is not already running. The timer updates every second.

        Args:
            event: The event that triggers this method (usually a focus event).
        """
        if not self.timer_running:  # Only start the timer if it is not running
            self.timer_running = True
            self.update_timer()  # Start updating the timer

    def update_timer(self):
        """
        Updates the timer every second and recalculates the WPM.
        Schedules the next update using `after`.
        """
        if self.timer_running:
            self.time_elapsed += 1  # Increment elapsed time by 1 second
            self.timer_label.config(text=f"Time Elapsed: {self.time_elapsed}s")  # Update timer label

            # Recalculate WPM based on current input
            input_text = self.input_area.get()
            self.calculate_wpm(input_text)

            # Schedule the next timer update after 1 second
            self.timer_id = self.after(1000, self.update_timer)

    def stop_timer(self):
        """
        Stops the timer and cancels any scheduled timer updates.
        """
        if self.timer_running:  # Only stop the timer if it is running
            self.timer_running = False
        if self.timer_id:  # Cancel any scheduled timer events
            self.after_cancel(self.timer_id)

    def reset_timer(self):
        """
        Resets the timer to 0 and updates the timer label accordingly.
        """
        self.timer_running = False
        self.time_elapsed = 0
        self.timer_label.config(text="Time: 0s")  # Reset the timer label

    def calculate_wpm(self, input_text):
        """
        Calculates and updates the words per minute (WPM) based on the user's input and elapsed time.

        Args:
            input_text: The text that the user has typed so far.
        """
        if self.time_elapsed > 0:  # Avoid division by zero
            time_minutes = self.time_elapsed / 60  # Convert elapsed time to minutes
            words = len(input_text.split())  # Count the number of words typed
            wpm = (words / time_minutes)  # Calculate words per minute
            self.wpm_label.config(text=f"WPM: {wpm:.2f}")  # Update the WPM label
        else:
            self.wpm_label.config(text="WPM: 0.00")  # If no time has elapsed, WPM is 0

    def restart_program(self):
        """
        Resets the program to its initial state, including the timer, input area, and displayed sentence.
        """
        self.reset_timer()  # Reset the timer to 0
        self.input_area.delete(0, tk.END)  # Clear the input area
        self.sentence_display.display_sentence()  # Display a new random sentence
        self.accuracy_label.config(text="Accuracy: 100%")  # Reset accuracy label
        self.wpm_label.config(text="WPM: 0.00")  # Reset WPM label
        self.start_timer()  # Restart the timer when the user starts typing again
        self.input_area.bind("<KeyRelease>", self.check_accuracy)  # Rebind the key release event
        self.input_area.focus_set()  # Focus on the input field to allow typing immediately
