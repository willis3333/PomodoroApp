# TODO: Debug Start and Reset button interaction anomalies(i.e.- pressing start when timer is running,
# TODO: Add Break/ Work Indicator
# TODO: Add Round times info (long break, short break etc)
# TODO: Add customization of timer in round times info (allow user input for minutes)
import tkinter
from playsound import playsound

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = .25
LONG_BREAK_MIN = .5
timer_countdown = None
# ---------------------------- UI SETUP ------------------------------- #
gui = tkinter.Tk()
gui.title("Pomodoro App")
gui.config(padx=100, pady=100)

heading = tkinter.Label(text='Pomodoro App', font=(FONT_NAME, 40, 'bold'))
heading.grid(column=2, row=1)

image_canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW)
tomato_image = tkinter.PhotoImage(file='tomato.png')
image_canvas.create_image(100, 112, image=tomato_image,)
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
        if minutes < 10:
            minutes = f'0{minutes}'
        seconds = seconds % 60
        if seconds < 10:
            seconds = f'0{seconds}'
        timer_text = f'{minutes}:{seconds}'
        image_canvas.itemconfig(timer, text=timer_text)
    else:
        buzzer_play()
        timer_text = 'Time up!'
        image_canvas.itemconfig(timer, text=timer_text)
        global pomodoro_count
        timer_round += 1
        if timer_round % 2 == 0:
            pomodoro_count += 1
        pomodoro_counter.config(text=f'Pomodoros Completed: {pomodoro_count}')


def buzzer_play():
    playsound('mixkit-alarm-clock-beep-988.wav')

def start_timer():
    global timer_round
    global timer_text
    global timer
    global pomodoro_minutes
    if timer_round % 2 == 1:
        pomodoro_minutes = WORK_MIN
    elif timer_round % 2 ==0:
        if timer_round % 7 == 0:
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
    gui.after_cancel(timer_countdown)
    timer_round = 1
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
