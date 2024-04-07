import PySimpleGUI as sg
from datetime import datetime, date, timedelta
#import dictreader

today_date = datetime.today().strftime('%d-%m-%Y')
today_date = datetime.strptime(today_date,"%d-%m-%Y")

day_of_week = date.weekday(today_date)

main_layout = [
    [sg.Column(
        [[sg.Text("School Week checker!", text_color="Black", background_color="White", font = ("Comic Sans MS", 20), justification="Center")]],background_color="White", expand_x=True, justification="center")],
        [sg.Input(key='-START_DATE-', size=(20,1), enable_events=True), sg.CalendarButton('Term start date',  target='-START_DATE-', format="%d-%m-%Y")],
        [sg.Input(key='-END_DATE-', size=(20,1), enable_events=True), sg.CalendarButton('Term end date',  target='-END_DATE-', format="%d-%m-%Y")],
        [sg.Button("Submit?", key='-SUBMIT-')],
        [sg.Text("Number of weeks: ",key="-TXT1-")],
        [sg.Text("Completed school days: ",key="-TXT2-")],
        [sg.Text("Current week: ",key="-TXT3-")],
]




window = sg.Window('Week checker', main_layout, resizable=True, size=(435,520), finalize=True)
while True:
    event, values = window.read()
    if event in (None, 'Exit') or event =="-QUIT-":
        break

    elif event == '-START_DATE-':
        if values[event]:
            term_start_date = datetime.strptime(values[event], "%d-%m-%Y")
        else:
            pass

    elif event == '-END_DATE-':
        if values[event]:
            term_end_date = datetime.strptime(values[event], "%d-%m-%Y")
        else:
            pass
    elif event == '-SUBMIT-':
        # generating dates
        dates = (term_start_date + timedelta(idx + 1)
                for idx in range((term_end_date - term_start_date).days))
        
        # summing all weekdays
        school_days = sum(1 for day in dates if day.weekday() < 5)
        school_days+=1
        total_weeks = int(school_days/5)
        window["-TXT1-"].update(f'Number of weeks: {total_weeks}')

        elapsed_dates = (term_start_date + timedelta(idx + 1)
                for idx in range((today_date-term_start_date).days))
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
window.close()
