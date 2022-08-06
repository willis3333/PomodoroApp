# TODO: reduce use of global variables
# TODO: Add Round times info (long break, short break etc)
# TODO: Add customization of timer in round times info (create interactive slider for minutes)
# Todo: Add task list (swim lanes?)

import tkinter
from playsound import playsound

# ---------------------------- CONSTANTS ------------------------------- #
RED = "#8b0000"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 10
timer_countdown = None
# ---------------------------- UI SETUP ------------------------------- #
gui = tkinter.Tk()
gui.title("Pomodoro App")
gui.config(padx=100, pady=100)

heading = tkinter.Label(text='Pomodoro Timer', font=(FONT_NAME, 40, 'bold'))
heading.grid(column=2, row=1)

image_canvas = tkinter.Canvas(width=260, height=224, bg=YELLOW)
tomato_image = tkinter.PhotoImage(file='tomato.png')
image_canvas.create_image(130, 112, image=tomato_image,)
image_canvas.grid(column=2, row=2)
# ---------------------------- TIMER MECHANISM ------------------------------- #
pomodoro_minutes = WORK_MIN
timer_round = 1
timer_text = f'{pomodoro_minutes}:00'
timer = image_canvas.create_text(100, 130, text=timer_text, fill='white', font=(FONT_NAME, 35, "bold"))


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(seconds):
    global timer_round
    global timer_text
    global timer
    global timer_countdown
    if seconds >= 0:
        timer_countdown = gui.after(1000, count_down, seconds-1)
        minutes = int(seconds / 60)
        seconds = seconds % 60
        if seconds < 10:
            seconds = f'0{seconds}'
        timer_text = f'{minutes}:{seconds}'
        image_canvas.itemconfig(timer, text=timer_text, fill='white')
    else:
        buzzer_play()
        if timer_round % 2 == 1:
            image_canvas.itemconfig(timer, fill=RED)
            if timer_round % 7 == 0:
                timer_text = 'LONG BREAK'
            else:
                timer_text = 'BREAK'
        else:
            timer_text = 'WORK'
            image_canvas.itemconfig(timer, fill=GREEN)
        image_canvas.itemconfig(timer, text=timer_text)
        global pomodoro_count
        timer_round += 1
        if timer_round % 2 == 0:
            pomodoro_count += 1
        pomodoro_counter.config(text=f'Pomodoros Completed: {pomodoro_count}')
        start_button['state'] = 'normal'

def buzzer_play():
    playsound('mixkit-alarm-clock-beep-988.wav')

def start_timer():
    global timer_round
    global timer
    global pomodoro_minutes
    global start_button
    start_button['state'] = 'disabled'
    if timer_round % 2 == 1:
        pomodoro_minutes = WORK_MIN
    elif timer_round % 2 == 0:
        if timer_round % 8 == 0:
            pomodoro_minutes = LONG_BREAK_MIN
        else:
            pomodoro_minutes = SHORT_BREAK_MIN
    pomodoro_seconds = pomodoro_minutes*60
    count_down(pomodoro_seconds)


start_button = tkinter.Button(text='Start', command=start_timer)
start_button.grid(column=1, row=3)


# ---------------------------- TIMER RESET ------------------------------- #
def count_down_reset():
    global timer_countdown
    global timer
    global pomodoro_minutes
    global timer_text
    global timer_round
    global start_button
    gui.after_cancel(timer_countdown)
    start_button['state'] = 'normal'
    if timer_round % 2 == 0:
        timer_round += 1
    pomodoro_minutes = WORK_MIN
    timer_text = f'{pomodoro_minutes}:00'
    image_canvas.itemconfig(timer, text=timer_text)


reset_button = tkinter.Button(text='Reset', command=count_down_reset)
reset_button.grid(column=3, row=3)
# ---------------------------- POMODORO COUNTER------------------------------- #
pomodoro_count = 0
pomodoro_counter = tkinter.Label(text=f'Pomodoros Completed: {pomodoro_count}', font=(FONT_NAME, 14, 'bold'))
pomodoro_counter.grid(column=2, row=4)

gui.mainloop()
