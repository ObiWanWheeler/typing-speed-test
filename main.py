from tkinter import *
import math
import sqlite3
import random


conn = sqlite3.connect('sample_texts.db')
c = conn.cursor()
sentences = [row[0] for row in c.execute("SELECT text FROM samples").fetchall()]

timer = None


def set_target():
    target_text["text"] = random.choice(sentences)
    timer_txt["text"] = "00:00"
    timer_txt["fg"] = "#000000"


def stop_timer():
    global timer
    window.after_cancel(timer)
    timer_txt["fg"] = "#9bdeac"
    response.delete(0, END)
    timer = None
    window.after(3000, set_target)


def stopwatch(count):
    global timer
    if response.get().lower() == target_text["text"].lower():
        stop_timer()
    else:
        ms, seconds = math.modf(count)
        timer_txt["text"] = f"{int(seconds)}:{f'{ms:.2f}'.replace('0.','')}"
        timer = window.after(10, stopwatch, count + 0.01)


def start_timer():
    if not timer:
        response.delete(0, END)
        response.focus()
        stopwatch(0)


window = Tk()
window.title("Typing Speed Tester")
window.minsize(width=400, height=100)
window.config(padx=100, pady=40)

target_text = Label(text=random.choice(sentences))
target_text.grid(column=1, row=1)
response = Entry(width=50)
response.grid(column=1, row=2)
start_btn = Button(text="Start", width=10, command=start_timer)
start_btn.grid(column=1, row=3)
timer_txt = Label(text="00:00")
timer_txt.grid(column=1, row=4)

window.mainloop()
