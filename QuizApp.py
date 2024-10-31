import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Create a MySQL connection
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="quizapp"
)

# Create a cursor object
cursor = cnx.cursor()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("400x300")

        # Create frames for different sections of the app
        self.topic_frame = tk.Frame(self.root)
        self.topic_frame.pack(fill="x")

        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(fill="x")

        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill="x")

        # Create topic selection dropdown
        self.topic_label = tk.Label(self.topic_frame, text="Select a topic:")
        self.topic_label.pack(side="left")

        self.topic_var = tk.StringVar()
        self.topic_var.set("Select a topic")

        self.topic_menu = tk.OptionMenu(self.topic_frame, self.topic_var, "History", "Science", "Literature")
        self.topic_menu.pack(side="left")

        # Create start quiz button
        self.start_quiz_button = tk.Button(self.topic_frame, text="Start Quiz", command=self.start_quiz)
        self.start_quiz_button.pack(side="left")

        # Create question label and answer options
        self.question_label = tk.Label(self.question_frame, text="", wraplength=300)
        self.question_label.pack(fill="x")

        self.answer_var = tk.IntVar()

        self.option1_button = tk.Radiobutton(self.question_frame, text="", variable=self.answer_var, value=1)
        self.option1_button.pack(fill="x")

        self.option2_button = tk.Radiobutton(self.question_frame, text="", variable=self.answer_var, value=2)
        self.option2_button.pack(fill="x")

        self.option3_button = tk.Radiobutton(self.question_frame, text="", variable=self.answer_var, value=3)
        self.option3_button.pack(fill="x")

        self.option4_button = tk.Radiobutton(self.question_frame, text="", variable=self.answer_var, value=4)
        self.option4_button.pack(fill="x")

        # Create submit answer button
        self.submit_button = tk.Button(self.question_frame, text="Submit", command=self.submit_answer)
        self.submit_button.pack(fill="x")

        # Create score label
        self.score_label = tk.Label(self.score_frame, text="Score: 0")
        self.score_label.pack(fill="x")

    def start_quiz(self):
        # Get the selected topic
        topic = self.topic_var.get()

        # Retrieve questions from the database
        cursor.execute("SELECT * FROM questions WHERE topic = %s", (topic,))
        questions = cursor.fetchall()

        # Set the first question
        self.set_question(questions[0])

    def set_question(self, question):
        # Set the question label and answer options
        self.question_label.config(text=question[1])
        self.option1_button.config(text=question[2], value=1)
        self.option2_button.config(text=question[3], value=2)
        self.option3_button.config(text=question[4], value=3)
        self.option4_button.config(text=question[5], value=4)

    def submit_answer(self):
        # Get the user's answer
        answer = self.answer_var.get()

        # Check if the answer is correct
        cursor.execute("SELECT correct_answer FROM questions WHERE id = %s", (self.current_question_id,))
        correct_answer = cursor.fetchone()[0]

        if answer == correct_answer:
            # Increment the score
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

        # Move to the next question
        self.current_question_id += 1
        if self.current_question_id < len(self.questions):
            self.set_question(self.questions[self.current_question_id])
        else:
            # Quiz is complete, store the score in the database
            cursor.execute("INSERT INTO scores (user_id, topic, score) VALUES (%s, %s, %s)", (1, self.topic_var.get(), self.score))
            cnx.commit()
            messagebox.showinfo("Quiz Complete", f"Your score is {self.score}!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
