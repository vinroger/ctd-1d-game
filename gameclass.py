# import modules needed
import random
import reader as reader
import game_over as game_over
import storymenu as storymenu
import tkinter as tk
import tkinter.ttk as ttk

font_used = "Consolas"
win_value = 10

list_answer = []
list_description = []
list_category = []


def update_database():
    f = open('difficulty.txt', 'r')
    difficulty = f.read()
    f.close()
    dictUsed = {}
    # code below chooses the word list based on the difficulty
    if difficulty == "easy":
        dictUsed = reader.easyWords
    elif difficulty == "medium":
        dictUsed = reader.mediumWords
    elif difficulty == "hard":
        dictUsed = reader.hardWords
    elif difficulty == "asian":
        dictUsed = reader.asianWords
    else:
        dictUsed = reader.easyWords
    # then adds the different components to the correct arrays
    for i in list(dictUsed.keys()):
        list_answer.append(i)
    for i in list(dictUsed.values()):
        list_description.append(i[0])
        list_category.append(i[1])


class Game(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        update_database()
        self.title("Frank's Scrabble Game")
        self.geometry('800x800')
        self.iconbitmap('img/favicon.ico')
        # Full Screen
        self.fullScreenState = True
        try:
            # The code for the fullscreen function was taken from the code found at 
            # https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/ 
            self.attributes('-fullscreen', self.fullScreenState)
            self.bind("<F11>", lambda event: self.attributes(
                "-fullscreen", not self.attributes("-fullscreen")))
            self.bind("<Escape>", lambda event: self.attributes(
                "-fullscreen", False))
        except:
            pass

        self.bg_image = tk.PhotoImage(file="img/frame/boat_0_0.png")
        self.framelabel = tk.Label(
            self,
            image=self.bg_image,
        )
        self.framelabel.pack()
        self.framelabel.place(relx=0.5, y=130, anchor="c", height=400)
        self.main_frame = tk.Frame(self, height=600, width=1500)

        self.progress = 0
        self.answer = ""
        self.reset_all_globals()
        self.start_game()
        self.main_frame.pack(side="bottom")
        self.main_frame.pack_propagate(0)

        self.mainloop()

    def clear_window(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def start_game(self):
        self.clear_window()
        self.button_list = []
        self.answer_list = []
        self.last_button_pressed = []
        self.last_index_pressed = []
        self.answer = ""
        self.guess = ""
        # generate new answer
        randomInteger = random.randint(0, len(list_answer)-1)
        self.answer = list_answer[randomInteger]
        self.answer_description = list_description[randomInteger]
        self.category = list_category[randomInteger]

        # Pop the list element to avoid duplicate answers and then save it to database
        self.removed_q = list_answer.pop(randomInteger)
        self.removed_d = list_description.pop(randomInteger)
        self.removed_c = list_category.pop(randomInteger)

        self.generate_elements()
        self.main_frame.pack(side="bottom")
        self.main_frame.pack_propagate(0)

    def start_game_skip(self):
        self.clear_window()
        self.button_list = []
        self.answer_list = []
        self.last_button_pressed = []
        self.last_index_pressed = []
        self.answer = ""
        self.guess = ""
        # generate new answer

        list_answer.append(self.removed_q)
        list_description.append(self.removed_d)
        list_category.append(self.removed_c)

        randomInteger = random.randint(0, len(list_answer)-1)
        self.answer = list_answer[randomInteger]
        self.answer_description = list_description[randomInteger]
        self.category = list_category[randomInteger]

        self.removed_q = list_answer.pop(randomInteger)
        self.removed_d = list_description.pop(randomInteger)
        self.removed_c = list_category.pop(randomInteger)

        self.generate_elements()
        self.main_frame.pack(side="bottom")
        self.main_frame.pack_propagate(0)

    def reset_all_globals(self):
        self.last_button_pressed = []
        self.last_index_pressed = []
        self.progress = 0
        self.lifeline = ["❤", "❤", "❤", "❤", "❤"]
        self.hints = ["💡", "💡", "💡", "💡", "💡"]
        self.answer = ""
        self.button_list = []
        self.answer_list = []
        self.guess = ""

    def undo(self):
        try:
            self.last_button_pressed[-1].grid(
                row=1, column=self.last_index_pressed[-1], padx=5, pady=5
            )
            self.last_button_pressed.pop()
            self.last_index_pressed.pop()
            self.guess = self.guess[:-1]
            self.guess_label.config(text=self.guess)
            return
        except:
            return

    def assign_letter(self, content, button, index):
        self.last_button_pressed.append(button)
        self.last_index_pressed.append(index)
        self.guess = self.guess + str(content)
        self.guess_label.config(text=self.guess)
        button.grid_forget()

        return

    def generate_buttons(self):
        s = self.answer.upper()
        while s == self.answer.upper():
            lst = list(s)
            random.shuffle(lst)
            self.answer_list = lst
            s = ''.join(lst)
        answer = s

        for i in range(len(answer)):
            self.button_list.append(tk.Button(self.guess_buttons_frame, text=answer[i].upper(
            ), font=("Consolas", 20), command=lambda idx=i: self.assign_letter(answer[idx].upper(), self.button_list[idx], idx)))
            self.button_list[i].grid(row=1, column=i, padx=5, pady=5)

    def update_lifeline(self):
        self.check_progress()
        lifeline_text = ""
        for i in self.lifeline:
            lifeline_text += i + " "
        self.lifeline_label.config(text="Lifeline\n"+lifeline_text)

        if len(self.lifeline) <= 0:
            self.game_over_lost()

    def update_hint(self):

        hint_text = ""
        for i in self.hints:
            hint_text += i + " "
        self.hint_label.config(text="Hint\n"+hint_text)

    def hint(self):
        if len(self.hints) > 0:
            self.hints.pop()
            self.hint_text.config(text=self.answer_description)
            self.update_hint()

    def check_progress(self):
        # Read what level is This
        f = open('level.txt', 'r')
        self.level = f.read()
        f.close()
        self.level = int(self.level)
        if self.level == 0:
            drawing = "boat"
        elif self.level == 1:
            drawing = "truck"
        else:
            drawing = "plane"
        framestring = "img/frame/" + drawing + "_" + \
            str(int(self.progress/10)) + "_" + \
            str(5-len(self.lifeline)) + ".png"
        self.bg_image.config(file=framestring)
        self.framelabel.config(image=self.bg_image)

        if self.progress >= win_value:
            self.game_over_win()
        return

    def game_over_win(self):
        self.clear_window()
        win_text_properties = tk.Label(
            self.main_frame, text="I made it across safely!\nThanks for your help!\nMeoww <3", font=("Consolas", 20))
        win_text_properties.pack(pady=100)
        self.generate_restart_button()
        return

    def generate_restart_button(self):
        # restart_button
        self.restart_button = tk.Button(self.main_frame, text="Continue", font=(
            "Consolas", 20), command=self.go_to_next_level)
        self.restart_button.pack(pady=10)
        return

    def go_to_next_level(self):

        f = open('level.txt', 'r')
        a = f.read()
        level_now = int(a) + 1
        f.close()

        f = open('level.txt', 'w')
        f.write(str(level_now))
        f.close()

        self.destroy()
        storymenu.StoryMenu()

    def generate_return_menu_button(self,win=True):
        # restart_button
        if win:
            cmd_used = self.credit_window
        else:
            cmd_used = self.lose_window
        self.return_menu_button = tk.Button(self.main_frame, text="Continue", font=(
                "Consolas", 20), command=cmd_used)

        self.return_menu_button.pack(pady=10)
        return

    def credit_window(self):
        self.destroy()
        game_over.GameOver()
    
    def lose_window(self):
        self.destroy()
        game_over.GameOver(False)

    def game_over_lost(self):
        self.clear_window()
        if self.level == 0:
            drawing = "boat"
        elif self.level == 1:
            drawing = "truck"
        else:
            drawing = "plane"
        string = "Nooo my " + drawing + " is destroyed..."
        lose_text_properties = tk.Label(
            self.main_frame, text=string, font=("Consolas", 40))
        lose_text_properties.pack(pady=100)
        self.generate_return_menu_button(False)
        return

    def check_guess(self):
        if self.guess == self.answer.upper():
            self.grade.config(text="You are Right!")
            # progress update
            self.progress += 10
            self.progress_bar["value"] = abs(self.progress)
            self.progress_text.config(
                text="Progress: " + str(self.progress)+" %")
            self.check_progress()
            self.update_lifeline()
            if self.progress < win_value:
                self.start_game()
        else:
            for i in range(len(self.guess)):
                self.undo()
            self.grade.config(text="oops! You are wrong")
            try:
                self.lifeline.pop()
            except:
                pass

            self.update_lifeline()

        return

    def generate_elements(self):
        self.gridframe = tk.Frame(self.main_frame, width=400)
        self.gridframe.pack(expand=True)
        self.hint_label = tk.Label(
            self.gridframe, text="Hint\n", font=("default", 15, "bold"), fg="orange")
        self.hint_label.grid(row=0, column=0)
        self.update_hint()

        self.empty_spaces = tk.Label(
            self.gridframe, text="                 Category: " + self.category + "                ", font=("Consolas", 15, "bold"), fg="blue", anchor="center")
        self.empty_spaces.grid(row=0, column=1)

        self.lifeline_label = tk.Label(
            self.gridframe, text="Lifeline\n", font=("default", 15, "bold"), fg="red")
        self.lifeline_label.grid(row=0, column=2, padx=10)
        self.update_lifeline()

        # theme for progress bar
        ttk_style = ttk.Style()
        ttk_style.theme_use('classic')
        ttk_style.configure("red.Horizontal.TProgressbar",
                            foreground='red', background='red')

        # Progress Bar
        self.progress_bar = ttk.Progressbar(
            self.main_frame, style="", orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_bar["value"] = abs(self.progress)
        self.progress_bar.pack()

        # Progress text and percentage
        self.progress_text = tk.Label(self.main_frame, text="Progress: " +
                                      str(self.progress) + " %", font=("Consolas", 15))
        self.progress_text.pack(pady=(0, 20))

        self.guess_buttons_frame = tk.Frame(self.main_frame)
        self.guess_buttons_frame.pack(pady=5)
        # loop through the answer and generate buttons
        # scramble the answer

        self.generate_buttons()

        self.guess_label = tk.Label(self.main_frame, text=self.guess, font=(
            font_used, 20), width=20)
        self.guess_label.pack(pady=5)

        # undo button for
        self.ans_button = tk.Button(
            self.main_frame, text="Submit", font=(
                font_used, 15), width=20, command=self.check_guess)
        self.ans_button.pack(pady=5)

        # button frame for submit hint next
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=5)

        self.next_button = tk.Button(
            self.button_frame, text="Skip", command=self.start_game_skip)
        self.next_button.grid(row=0, column=0, padx=10)

        self.hint_button = tk.Button(
            self.button_frame, text="Hint", command=self.hint)
        self.hint_button.grid(row=0, column=1, padx=10)

        self.undo_button = tk.Button(
            self.button_frame, text="Undo", command=self.undo)
        self.undo_button.grid(row=0, column=2, padx=10)
        self.bind('<Return>', lambda event: self.check_guess())

        # hint for the answer
        self.hint_text = tk.Label(
            self.main_frame, text="", font=("Consolas", 18))
        self.hint_text.pack(pady=5, padx=00)

        self.grade = tk.Label(
            self.main_frame, text="", font=("Consolas", 18))
        self.grade.pack(pady=(10, 20), padx=00)
