import keyboard
from app_engine import AppEngine
import tkinter


# ___________________________________________Create Constants________________________________________________#
HEADING_FONT = ("Bebas Neu", 20, "bold")
SUBHEADING_FONT = ("Bebas Neu", 16, "bold")
INSTRUCTION_FONT = ("Bebas Neu", 16, "normal")
TEST_TEXT_FONT = ("Bebas Neu", 10, "normal")

INSTRUCTION_TEXT = ("Train yourself to type smoothly and consistently.. "
                    "If you stop for too long, you have to start again!")
START_BTN_FONT = ("Bebas Neu", 16, "normal")

engine = AppEngine()



# __________________________________________Set up Window________________________________________________#
window = tkinter.Tk(screenName="PerfecType", className="disappearing text app")
window.title("PerfecType")
window.geometry("600x1500")
window.maxsize(height=600, width=600)

keyboard.hook(engine.reset_count)

# ______________________________________Definition of Functions__________________________________________#






def open_result_popup(percentage_complete, similarity_score):
    """Creates a pop up window to display the test results"""
    top = tkinter.Toplevel(window)
    top.maxsize(width=300, height=300)
    top.geometry("300x300")
    top.title("Test Results")
    tkinter.Label(top, text="Test Over!\nYour Results", font=INSTRUCTION_FONT, anchor="n", justify="center").place(x=90, y=20)
    tkinter.Label(top, text=f"You managed to type {percentage_complete:.2f}% of the text\n\nYou got a similarity score of "
                            f"{similarity_score * 100:.2f}%", font=INSTRUCTION_FONT, wraplength=260, anchor="center").\
                            place(x=20, y=100)


def run_test():
    """Run typing test"""
    engine.count()
    engine.check_test_over()
    if not engine.test_over:
        window.after(1000, run_test)
    else:
        heading.config(text="Test Over")
        text.config(state="disabled")
        start_btn.config(state="normal")
        percentage_complete = engine.calculate_score(typed_text=text.get(1.0, "end"))[0]
        similarity_score = engine.calculate_score(typed_text=text.get(1.0, "end"))[1]
        open_result_popup(percentage_complete, similarity_score)




def start_test():
    """Start typing test"""
    reset()
    engine.test_over = False
    text.config(state='normal')
    start_btn.config(state='disabled')
    text.delete(1.0, "end")
    engine.difficulty = difficulty.get()
    random_text = engine.random_text()["story"]
    instructions.config(text=random_text, font=TEST_TEXT_FONT)
    run_test()



def reset():
    """Reset the typing test"""
    text.config(state="normal")  # Set the state to "normal" before deleting
    text.delete(1.0, "end-1c")
    text.config(state="disabled")
    heading.config(text="Typing Trainer")
    start_btn.config(state='normal')
    engine.count_var = 0
    engine.test_over = True
    instructions.config(text=INSTRUCTION_TEXT, font=INSTRUCTION_FONT)



def save():
    """Save the typed text to a file"""
    try:
        text_to_save = text.get(1.0, "end-1c")
        with open("C:/Users/profe/Desktop/saved_text.txt", "w", encoding="utf-8") as text_file:
            text_file.write(text_to_save)
    except Exception as e:
        print(f"Error while saving: {e}")











# ____________________________________________Main Canvas________________________________________________#
#Heading label
heading = tkinter.Label(text="PerfecType", font=HEADING_FONT, fg="black")
heading.config(anchor='n', pady=10)
heading.grid(row=0, column=0, columnspan=3, sticky='n')


#Instructions label
instructions = tkinter.Label(text=INSTRUCTION_TEXT, font=INSTRUCTION_FONT, fg="gray", wraplength=500, width=100, justify='center')
instructions.config(anchor='n')
instructions.grid(row=1, column=0, columnspan=3, sticky='n')

#Text widget
text = tkinter.Text(bd=3, width=60, height=15)
text.config(padx=20, pady=20, state="disabled")
text.grid(row=2, column=0, columnspan=3)

#Start button
start_btn = tkinter.Button(window, text="Start", activebackground="lightblue", bd=2, bg="lightgray", relief="ridge", height=1, width=4, font=START_BTN_FONT, command=start_test)
start_btn.grid(row=3, column=1, sticky="nsew", pady=20)


#__________________________________________Difficulty___________________________________________________#
#Difficulty canvas
difficulty_canvas = tkinter.Canvas(width=500, height=70, bg="lightgray")
difficulty_canvas.grid(row=4, column=0, columnspan=3)

difficulty = tkinter.IntVar()

#Difficulty label
radio_label = tkinter.Label(text="Difficulty", font=SUBHEADING_FONT, fg="black", bg="lightgray")
difficulty_canvas.create_window(250, 5, window=radio_label, anchor="n")

#Difficulty radio buttons
radio_1 = tkinter.Radiobutton(text="Easy", bg="lightgray", variable=difficulty, value=4)
radio_2 = tkinter.Radiobutton(text="Normal", bg="lightgray", variable=difficulty, value=3)
radio_3 = tkinter.Radiobutton(text="Hard", bg="lightgray", variable=difficulty, value=2)

difficulty_canvas.create_window(150, 50, window=radio_1, anchor="w")
difficulty_canvas.create_window(250, 50, window=radio_2, anchor="center")
difficulty_canvas.create_window(350, 50, window=radio_3, anchor="e")

difficulty.set(4)

#_____________________________________________Save / Reset_____________________________________________________#
#Save /Reset canvas
save_reset_canvas = tkinter.Canvas(width=500, height=60, bg="#333333")
save_reset_canvas.grid(row=5, column=0, columnspan=3)

#Save button
save_btn = tkinter.Button(window, text="Save", activebackground="lightblue", bd=2, bg="lightgray", relief="ridge", height=1, width=10, font=START_BTN_FONT, command=save)
save_btn.config(anchor="center")
save_btn_window = save_reset_canvas.create_window(150, 35, window=save_btn, anchor="center")

#Reset button
reset_btn = tkinter.Button(window, text="Reset", activebackground="lightblue", bd=2, bg="lightgray", relief="ridge", height=1, width=10, font=START_BTN_FONT, command=reset)
reset_btn.config(anchor="center")
reset_btn_window = save_reset_canvas.create_window(350, 35, window=reset_btn, anchor="center")

#Column/Row configurations
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(2, weight=1)

window.mainloop()