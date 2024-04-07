import PySimpleGUI as sg
from datetime import datetime, date, timedelta
import csv, os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

today_date = datetime.today().strftime('%d-%m-%Y')
today_date = datetime.strptime(today_date,"%d-%m-%Y")
time_date = today_date.strftime('%a %d %b %Y')



secondary_foreground="#5C636A"
foreground="#393E46"
background="#F0EDEE" 
secondary_background="#DAD2C3"
accent_colour1 = "#A88B79"
accent_colour2 = "#7B8D8E" 
accent_colour3 = "#A3BFA8"
highlight_colour = "#D7896F"

primary_font = ("Segoe UI", 25)
secondary_font = ("Georgia", 20)
tertiary_font = ("Arial", 10)
accent_font = ("Consolas", 20)
time_font = ("Courier", 15)



new_theme = {"BACKGROUND": background, "TEXT": sg.COLOR_SYSTEM_DEFAULT, "INPUT": sg.COLOR_SYSTEM_DEFAULT,
             "TEXT_INPUT": sg.COLOR_SYSTEM_DEFAULT, "SCROLL": sg.COLOR_SYSTEM_DEFAULT,
             "BUTTON": sg.OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR, "PROGRESS": sg.COLOR_SYSTEM_DEFAULT, "BORDER": 1,
             "SLIDER_DEPTH": 1, "PROGRESS_DEPTH": 0
             }
sg.theme_add_new('Custom theme', new_theme)
sg.theme('Custom theme')

class Setup:
    def __init__(self):
        self.all_dates = []

    def load_dates(self):
        folderpath = os.path.dirname(os.path.abspath(__file__))
        self.file = folderpath + '/term_dates.csv'
    
        with open(self.file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.all_dates.append(row)

    def current_term_checker(self):
        for i in (0,1,2,3,4,5,6,7):
            self.term_start_date=datetime.strptime(self.all_dates[i]["Start_date"], "%d-%m-%Y")
            self.term_end_date=datetime.strptime(self.all_dates[i]["End_date"], "%d-%m-%Y")
            self.term=self.all_dates[i]["Term"]
            print(self.term_start_date)
            print(self.term_end_date)
            if self.term_start_date <= today_date <= self.term_end_date:
                break
        else: 
            window['-COL1-'].update(visible=False)
            window['-COL2-'].update(visible=True)
                
week_setup = Setup()
week_setup.load_dates()


main_layout = [
    [sg.Column(
        [[sg.Text("School Week checker!", text_color='Black', background_color=secondary_background, font=primary_font, size=(435, 1), expand_x=True, justification="center")]], pad=(0,0)
    )],
    [sg.Text("Number of weeks: ",key="-TXT1-", text_color=foreground, font=secondary_font, background_color=secondary_background)],
    [sg.Text("Completed school days: ",key="-TXT2-", text_color=foreground, font=secondary_font, background_color=secondary_background)],
    [sg.Text("Current week: ",key="-TXT3-", text_color=foreground, font=secondary_font, background_color=secondary_background)],
    [sg.VPush()],
    [sg.Text("", font=tertiary_font), sg.Push(), sg.Text("",key="-TXT-", font=tertiary_font)]
]
school_holiday_layout = [
    [sg.Text("It's the school holidays, go have some fun!")]
]
layout = [
    [sg.Column(main_layout,key='-COL1-', expand_x=True, expand_y=True), sg.Column(school_holiday_layout, visible=False,key='-COL2-', expand_x=True, expand_y=True)]
]

window = sg.Window('Week checker', layout, resizable=True, size=(435,520), finalize=True)
week_setup.current_term_checker()

dtime_here = datetime.now()
dtime_here = dtime_here.strftime('%a %d %b %Y')
window["-TXT-"].update(f'{week_setup.term} {time_date}')


#getting all dates
dates = (week_setup.term_start_date + timedelta(idx + 1)
for idx in range((week_setup.term_end_date - week_setup.term_start_date).days))

# summing all weekdays
school_days = sum(1 for day in dates if day.weekday() < 5)
school_days+=1
total_weeks = int(school_days/5)
window["-TXT1-"].update(f'Number of weeks: {total_weeks}')

elapsed_dates = (week_setup.term_start_date + timedelta(idx + 1)
for idx in range((today_date-week_setup.term_start_date).days))
current_days = sum(1 for day in elapsed_dates if day.weekday() < 5)
window["-TXT2-"].update(f'Completed school days: {current_days+1}/{school_days}')

num_to_add=5
current_week=0
for i in range(total_weeks):
    current_week+=1
    if current_days-num_to_add<0:
        break
    else:
        num_to_add+=5
window["-TXT3-"].update(f'Current school week: {current_week}')

while True:
    event, values = window.read()

    if event in (None, 'Exit') or event =="-QUIT-":
        break

window.close()
