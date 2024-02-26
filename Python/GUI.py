from tkinter import *
from tkinter import messagebox
import project
import flask

voice_rec = Tk()
voice_rec.geometry("700x200")
voice_rec.title("Recorder")

title_lbl = Label(voice_rec, text="Start Recording Now")
title_lbl.grid(row=0, column=0, columnspan=3)

record_btn = Button(voice_rec, text="Record Audio", command=lambda: project.threading_rec(1))
stop_btn = Button(voice_rec, text="Stop Recording", command=lambda: project.threading_rec(2))
play_btn = Button(voice_rec, text="Play Recording", command=lambda: project.threading_rec(3))
halfSpeed_btn = Button(voice_rec, text="Speed x0.5", command=lambda : project.threading_rec(4))
doubleSpeed_btn = Button(voice_rec, text="Speed x2", command=lambda : project.threading_rec(5))

record_btn.grid(row=1, column=1)
stop_btn.grid(row=1, column=0)
play_btn.grid(row=1, column=2)
halfSpeed_btn.grid(row=1, column=3)
doubleSpeed_btn.grid(row=1, column=4)

voice_rec.mainloop()