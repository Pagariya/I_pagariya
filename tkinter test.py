import tkinter as tk

window = tk.Tk()

for i in range(3):
    for j in range(3):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack()
        button = tk.Button(master=frame,text="Click me!",width=25,height=5,bg="blue",fg="yellow")
        button.pack()


for i in range(3):
    for j in range(3,6):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)
        frame_2 = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame_2.grid(row=i, column=j, padx=5, pady=5)
        if i == 0 and j == 3:
          label_2 = tk.Label(master=frame_2, text=f"Row {i}\nColumn {j}")
          label_2.pack()
          button_2 = tk.Button(master=frame_2, text="Click me!", width=25, height=5, bg="blue", fg="yellow")
          button_2.pack()


for i in range(3,6):
    for j in range(3):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)
        frame_3 = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame_3.grid(row=i, column=j, padx=5, pady=5)
        label_3 = tk.Label(master=frame_3, text=f"Row {i}\nColumn {j}")
        label_3.pack()

        label_3_1 = tk.Label(master=frame_3, text=f"Row {i}\nColumn {j}")
        label_3_1.pack()



for i in range(3,6):
    for j in range(3,6):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)
        frame_4 = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame_4.grid(row=i, column=j, padx=5, pady=5)
        label_4 = tk.Label(master=frame_4, text=f"Row {i}\nColumn {j}")
        label_4.pack()

        label_4_1 = tk.Label(master=frame_4, text=f"Row {i}\nColumn {j}")
        label_4_1.pack()



window.mainloop()

