import tkinter as tk              # Import Tkinter for GUI
from tkinter import messagebox   # Import messagebox for popups
import random                    # Import random for shuffling questions
from mcqs import questions       # Import questions list from mcqs.py


class QuizGame:

    def __init__(self, root):
        # Initialize main window
        self.root = root                        #Stores main window reference
        self.root.title("Python Quiz Game")     # Set window title
        self.root.geometry("800x600")           # Set window size
        self.root.configure(bg='#2c3e50')     # Set background color

        # Load and shuffle questions
        self.questions = questions              #Stores imported questions in class variable
        random.shuffle(self.questions)          #Randomizes question order each time

        # Initialize variables
        self.q_no = 0                            # Current question index starts from 0
        self.score = 0                           # Score initially 0
        self.selected = tk.IntVar()              # Stores selected option index(radio button value)

        # Bind ESC key to quit game
        self.root.bind("<Escape>", lambda e: self.quit_game())

        # Create UI and show first question
        self.create_ui()
        self.show_question()

    def create_ui(self):                    #Function to design GUI
        # Title label
        tk.Label(                           #Creates heading label 
            self.root,
            text="🐍 Python Quiz Game 🐍",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=20)                     #.pack() places it on screen

        # Progress label (shows Question number + percentage)
        self.progress = tk.Label(
            self.root,
            font=("Arial", 14, "bold"),
            bg='#2c3e50',
            fg='#f39c12'
        )
        self.progress.pack()

        # Score label(Displays score)
        self.score_label = tk.Label(
            self.root,
            font=("Arial", 14, "bold"),
            bg='#2c3e50',
            fg='#27ae60'
        )
        self.score_label.pack()

        # Question label
        self.question = tk.Label(       #Displays question text
            self.root,
            font=("Arial", 16, "bold"),
            wraplength=700,   # Wrap text for long questions
            bg='#34495e',
            fg='white',
            pady=30
        )
        self.question.pack(padx=40, pady=20, fill='x')      #Places question box

        # List to store option buttons
        self.options = []

        # Create 4 radio buttons (options)
        for i in range(4):
            btn = tk.Radiobutton(
                self.root,
                text="",                 # Option text (updated later)
                variable=self.selected,  # Variable to store selected option
                value=i,                 # Option index
                font=("Arial", 12),
                indicatoron=0,           # Makes it look like a button
                width=50,
                height=2,
                bg='#34495e',
                fg='white',
                selectcolor='#3498db',
                command=self.enable_next  # Enable next button when selected
            )

            btn.pack(pady=6)            #Displays button
            self.options.append(btn)   # Store button in list

        # Frame for buttons
        btn_frame = tk.Frame(self.root, bg='#2c3e50')
        btn_frame.pack(pady=30)         

        # Next Question button
        self.next_btn = tk.Button(
            btn_frame,
            text="Next Question",
            font=("Arial", 14, "bold"),
            bg='#3498db',
            fg='white',
            width=15,
            height=2,
            command=self.next_question,
            state='disabled'  # Disabled until option selected
        )
        self.next_btn.pack(side='left', padx=10)

        # Restart button
        tk.Button(
            btn_frame,
            text="Restart Quiz",
            font=("Arial", 14, "bold"),
            bg='#e74c3c',
            fg='white',
            width=15,
            height=2,
            command=self.restart
        ).pack(side='left', padx=10)

        # Quit button
        tk.Button(
            btn_frame,
            text="Quit Game ❌",
            font=("Arial", 14, "bold"),
            bg='#95a5a6',
            fg='white',
            width=15,
            height=2,
            command=self.quit_game
        ).pack(side='left', padx=10)

    def show_question(self):
        # Get current question
        q = self.questions[self.q_no]

        # Calculate progress percentage
        progress_percent = (self.q_no + 1) / len(self.questions) * 100

        # Update progress label
        self.progress.config(
            text=f"Question {self.q_no+1} of {len(self.questions)} ({progress_percent:.0f}%)"
        )

        # Update score label
        self.score_label.config(
            text=f"Score: {self.score}/{self.q_no}"
        )

        # Display question text
        self.question.config(text=q["question"])

        # Display options
        for i in range(4):
            self.options[i].config(text=q["options"][i])

        # Reset selected option
        self.selected.set(-1)

        # Enable next button
        self.next_btn.config(state="normal")

    def enable_next(self):
        # Enable Next button when option is selected
        self.next_btn.config(state="normal")

    def next_question(self):
        # Check if user selected any option
        if self.selected.get() == -1:
            messagebox.showwarning("Warning", "Please select an option before continuing.")
            return

        # Get correct answer index
        correct = self.questions[self.q_no]["answer"]

        # Check answer
        if self.selected.get() == correct:
            self.score += 1  # Increase score if correct
        else:
            # Show correct answer if wrong
            messagebox.showinfo(
                "Wrong Answer",
                f"Correct Answer: {self.questions[self.q_no]['options'][correct]}"
            )

        # Move to next question
        self.q_no += 1

        # Check if quiz completed
        if self.q_no == len(self.questions):
            self.show_result()
        else:
            self.show_question()

    def show_result(self):
        # Calculate percentage
        percent = (self.score / len(self.questions)) * 100

        # Show result
        messagebox.showinfo(
            "Quiz Completed",
            f"Score: {self.score}/{len(self.questions)}\nPercentage: {percent:.1f}%"
        )

        # Restart quiz
        self.restart()

    def restart(self):
        # Reset quiz
        self.q_no = 0
        self.score = 0
        random.shuffle(self.questions)

        # Show first question again
        self.show_question()

    def quit_game(self):
        # Confirm before quitting
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):

            total = len(self.questions)
            percent = (self.score / total) * 100

            # Show final score
            messagebox.showinfo(
                "Final Score",
                f"Your Score: {self.score}/{total}\nPercentage: {percent:.1f}%"
            )

            # Close window
            self.root.destroy()


# Create main window
root = tk.Tk()

# Create Quiz Game object
QuizGame(root)

# Run the application
root.mainloop()