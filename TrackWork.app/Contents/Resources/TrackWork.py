# features test for TrackWork
# version 18. New:
# - project comments stored in database
# - Added summary
# - fixed bugs with End/Reset and Summary
# - new functionalities with project comments
# - new popup window layout
# - session summary export to text file
# - bugs with add project and summary list fixed
# - End/Reset button disabled when project running
# - Export option disabled when window is 'X'd

import PySimpleGUI as sg
import time
import datetime
import dbm
import shelve

def time_int():
    return int(round(time.time() * 100))

sg.theme('DarkGrey')
# DarkGrey - grey25
# DarkGrey5 - grey20
# DarkGray2 - grey17
ip_bgcolor = 'orange3' #blanched almond, orange3

# Define the window's contents
play_image = 'a.png'
pause_image ='p.png'
icon_image = 'tw_icon.icns'
font = 'Andale Mono'

guiA = 0
guiB = 0

if dbm.whichdb('tw_db') == None:
    username = 'username'
else:
    # create database for pure strings only
    db = dbm.open('tw_db', 'c')
    username_b = db['username']
    username = str(username_b, "utf-8")
    db.close()

if dbm.whichdb('shelve_tw_db') == None:
    listKT = ['Select...']
    # Comment list for storing project comments
else:
    # create shelf database for string lists and other objects
    sh = shelve.open('shelve_tw_db', 'c')
    listKT = sh['list']
    sh.close()

if dbm.whichdb('comm_tw_db') == None:
    # Comment list for storing project comments
    n = len(listKT)
    commentlist = [[None]] * n
    for j in range(0, n):
        commentlist[j] = ['']  # replace j element of empty mainlist with new value
else:
    # create shelf database for string lists and other objects
    co = shelve.open('comm_tw_db', 'c')
    commentlist = co['comments']
    co.close()


QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'

layout1 = [ [sg.Text("Setup", text_color='orange3', size=(40, 1), font=[font, 20])],
            [sg.Button(username, key='unametext', use_ttk_buttons=False, border_width=1, size=(16, 1), font=[font, 9],
                       visible=True, disabled=False, button_color=('blanched almond', 'grey17'),
                       tooltip='  Tip: Click, Edit and Hit Enter to update username  '),
            sg.InputText(key='editusername', tooltip=' e.g. - Star trooper ', background_color=ip_bgcolor, border_width=0,
                          font=[font, 11], visible=False, enable_events=True, focus=True),
            sg.Button('OK', key='OKuname', use_ttk_buttons=True, border_width=0, size=(4, 1), font=[font, 9],
                       visible=False, disabled=True, button_color=('black', 'orange3'), bind_return_key=True,
                       tooltip='  Tip: Hit Enter to update username  ')],
            [sg.Text('')],
            [sg.Text("Current project list:", text_color='orange', font=[font, 11]),
             sg.InputOptionMenu(listKT, size=(20, 1), text_color='black',
                                default_value='Select...', key='currentKT')],
            [sg.Text("Add new projects:", metadata=True, text_color='orange', font=[font, 11]),
             sg.InputText(key='ip1', tooltip=' e.g.- Project X ', do_not_clear=True, background_color=ip_bgcolor, border_width=0,
                      font=[font, 11], enable_events=True, focus=False),
             sg.Button('Add', key='add1', use_ttk_buttons=True, border_width=1, size=(12, 1), font=[font, 9],
                       disabled=False, button_color=('orange3', 'grey25'), bind_return_key=True,
                       tooltip='  Note: New projects can be added later too  ')],
            [sg.Text('...', size=(18,1), text_color='blanched almond', font=[font, 10], k='news'),
             sg.Text('', size=(40,1), text_color='blanched almond', font=[font, 10], key='addedKT')],
            [sg.Text('')],
            [sg.Button('Get Started!', use_ttk_buttons=True, border_width=0, size=(14, 1), font=[font, 11],
                       button_color=('black', 'orange3'), key='getstarted', disabled=False)]]

layout2 = [ [sg.Text("TrackWork", size=(40,1), text_color='orange3', font=[font, 20])],
            [sg.Text('...', size=(40,2), font=[font, 11] ,text_color='blanched almond', key='unamemain')],
            #[sg.Text('_' * 90, size=(0, 2), text_color='blanched almond')],
            [sg.Text("Start time:", text_color='orange', font=[font, 11]),
             sg.Text('00:00:00', size=(8,1), text_color='blanched almond', font=[font, 11], key='start_time')],
            [sg.Text("Start date:", text_color='orange', font=[font, 11]),
             sg.Text('00.00.0000', size=(10,1), text_color='blanched almond', font=['Consolas', 11], key='start_date'),
             sg.Text('...', size=(12,1), text_color='blanched almond', font=[font, 11], key='start_day')],
            [sg.Text("Clnd. week:", text_color='orange', font=[font, 11]),
             sg.Text('...', size=(12,1), text_color='blanched almond', font=[font, 11], key='cald_week')],
            [sg.Text("Select project:", text_color='orange', font=[font, 11]),
             sg.InputOptionMenu(listKT, size=(20, 1), text_color='black',
                                default_value='Select...',key='KT'), # background_color=ip_bgcolor, text_color='blanched almond',
             sg.Button('Switch project', k='switch_proj', use_ttk_buttons=True, disabled=True,
                       border_width=1, size=(16, 1), font=[font, 9], button_color=('orange3', 'grey25'),
                       tooltip= ' Tip: Resets timer, enables selection of a new project, enables <Add project>'),
             sg.Button(k='active', border_width=0, auto_size_button=False, use_ttk_buttons=False, visible=True,
                       button_color=('grey20', 'grey25'), disabled=False, image_filename=play_image,
                       bind_return_key=False, enable_events=True),
             sg.Button(k='pause', border_width=0, auto_size_button=False, use_ttk_buttons=False, visible=False,
                       button_color=('grey20', 'grey25'), disabled=True, image_filename=pause_image,
                       enable_events=True)],
            #[sg.Text('')],
            [sg.Text("Add new project:", text_color='orange', font=[font, 11]),
             sg.InputText('', key='ip2', background_color=ip_bgcolor, border_width=0, font=[font, 11],
                          enable_events=True, do_not_clear=False,  tooltip=' e.g.- Project X '),
             sg.Button('Add project', k='add2', use_ttk_buttons=True, border_width=1, size=(12, 1),
                       font=[font, 9], disabled=False, button_color=('orange3', 'grey25'),
                       tooltip=' Tip: Requires <Switch project> to be enabled, once a project starts ',)],
            [sg.Text("Project comment:",  text_color='orange', font=[font, 11]),
             sg.InputText('', key='projcomment', background_color=ip_bgcolor, border_width=0, font=[font, 11],
                          enable_events=True, do_not_clear=False,  tooltip=' e.g.- Project extended by two weeks ',),
             sg.Button('Add comment', k='add3', use_ttk_buttons=True, border_width=1, size=(12, 1),
                       font=[font, 9], button_color=('orange3', 'grey25'), key='comment')],
            [sg.Text('')],
            [sg.Text('...', size=(24,1), font=[font, 11], text_color='blanched almond', key='currentKT'), sg.Text(''),
             sg.Text(size=(24,1), font=[font, 11], text_color='blanched almond', key='KTupdate'),
             sg.Text(size=(24,1), font=[font, 11], text_color='blanched almond', key='currentKT2')],
            [sg.Text('...', size=(18,1), font=[font, 24], text_color='blanched almond', key='status')],
            [sg.Text('00:00:00', size=(8,1), font=[font, 32], text_color='blanched almond', key='time')],
            [sg.Text('')],
            [sg.Button('Summary', border_width=0, use_ttk_buttons=True, size=(12, 1), font=[font, 11],
                       button_color=('black', 'orange3'), k='summary', tooltip=' View current session summary '),
             sg.Button('End/Reset session', border_width=0, use_ttk_buttons=True, size=(22, 1), font=[font, 11],
                       button_color=('black', 'orange3'), k='end', tooltip=' View session summary and end/reset current session '),
             sg.Button('Close', border_width=0, use_ttk_buttons=True, size=(10, 1), font=[font, 11],
                       button_color=('black', 'orange3'), k='close', tooltip=' View session summary and close the App ')
             ]]

# Create the windows

window1 = sg.Window('TrackWork (vintage) v1.2 - welcome!', layout1, grab_anywhere=False, return_keyboard_events=True,
                    icon=icon_image)
ip1_active = False

while True:
    event, values = window1.read()

    if event == 'ip1':
        ip1_active = True

    if event == 'add1':
        newKT = values['ip1']
        if len(newKT) == 0:
            window1['news'].update('New project added:')
            window1['addedKT'].update(' Field empty! :( ')
        else:
            listKT.append(newKT)
            window1['news'].update('New project added:')
            window1['addedKT'].update(newKT)
            window1['ip1'].update('')
            window1.Element('currentKT').update(values=listKT)
            print('newKT:', newKT)
            print('new listKT:', listKT)

    if event == 'unametext':
        ip1_active = False
        window1['editusername'].update(visible=True)
        window1['editusername'].update(disabled=False)
        window1['unametext'].update(visible=False)
    if event == 'editusername':
        window1['OKuname'].update(disabled=False)
        window1['unametext'].update(values['editusername'])
        username = values['editusername']
    if event == 'OKuname':
        window1['unametext'].update(visible=True)
        window1['editusername'].update(visible=False)
        window1['editusername'].update(disabled=True)
        window1['OKuname'].update(disabled=True)
    if event == 'getstarted':
        guiB = 1
        window1.close()
        window2 = sg.Window('TrackWork (vintage) v1.2', layout2, grab_anywhere=False, return_keyboard_events=True, icon=icon_image)

    # Add capability to allow enter as button click
    if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):  # Check for ENTER key
            if ip1_active:  # if it's a button element, click it
                elem = window1['add1']  # target element
                elem.Click()  # check for buttons that have been clicked

    if event == sg.WIN_CLOSED:
        window1.close()
        break

# Event loop to process events and get the 'values' of inputs
current_time, paused_time, active, paused = 0, 0, False, False
App_start_time = time_int()
proj_start_time = 0
switch_proj = False
add2 = False

# start time
localtime = time.localtime()
day_hr = localtime[3]
day_min = localtime[4]
day_sec = localtime[5]
start_time = '{:02d}:{:02d}:{:02d}'.format(day_hr, day_min, day_sec)
end_time_text = '0.0.0'

# date
day = localtime[2]
mon = localtime[1]
year = localtime[0]
start_date = '{:02d}.{:02d}.{:02d}'.format(day, mon, year)

# day and Weeknumber
week_number = datetime.date(year, mon, day).isocalendar()[1] # 0: year, 1: weeknumber, 2:weekday
day_number = datetime.date(year, mon, day).weekday() # weekday starting 0-Monday 1-Tuesday ...

weekdays = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
week_day = weekdays[day_number]

# Project List for time calc
tfac = 1 #time factor FOR TESTING ONLY
n = len(listKT)
mainlist = [[None]]*n
summarylist = [[None]]*n
required_list = [[None]]*n
for j in range(0,n):
    mainlist[j] = [0] # replace j element of empty mainlist with new value
    summarylist[j] = [0]
    required_list[j] = [0]

# Comment list for storing project comments
n = len(listKT)
commentlist = [[None]] * n
for j in range(0, n):
    commentlist[j] = ['']  # replace j element of empty mainlist with new value

ip2_active = False
projcomment_active = False
enter_active = False
enter_pause = True

while True & guiB == 1:

    if active:
        event, values = window2.read(timeout=10)
        current_time = time_int() - proj_start_time
        window2['unamemain'].update(username)
    else:
        event, values = window2.read()
        window2['unamemain'].update(username)

    if event == 'pause':
        window2['currentKT'].update(values['KT'])
        window2['status'].update('PAUSED...')
        window2['status'].update(text_color='orange red')
        window2['KT'].update(disabled=True)
        window2['pause'].update(disabled=True)
        window2['active'].update(disabled=False)
        window2['pause'].update(visible=False)
        window2['active'].update(visible=True)
        window2['pause'].update(image_filename=pause_image)
        window2['active'].update(image_filename=play_image)
        window2['currentKT2'].update('')
        window2['switch_proj'].update(disabled=False)
        window2['add2'].update(disabled=True)
        window2['end'].update(disabled=False)
        ip2_active = False
        projcomment_active = False
        enter_active = False
        enter_pause = True

        # time related
        paused = True
        active = not active
        paused_time = time_int()
        selected_proj = values['KT']

    if event == 'active':
        if values['KT'] == 'Select...':
            window2['currentKT'].update('Select Project!')
            window2['currentKT'].update(text_color='orange red')
        else:
            window2['currentKT'].update(values['KT'])
            window2['status'].update('ACTIVE!')
            window2['status'].update(text_color='lawn green')  # lawn green
            window2['KT'].update(disabled=True)
            window2['active'].update(disabled=True)
            window2['pause'].update(disabled=False)
            window2['active'].update(visible=False)
            window2['pause'].update(visible=True)
            window2['active'].update(image_filename=play_image)
            window2['pause'].update(image_filename=pause_image)
            window2['currentKT2'].update('')
            window2['KTupdate'].update('')
            window2['switch_proj'].update(disabled=True)
            window2['add2'].update(disabled=True)
            window2['currentKT'].update(text_color='blanched almond')
            window2['end'].update(disabled=True)
            ip2_active = False
            projcomment_active = False
            enter_active = True
            enter_pause = False

            # time related
            active = True
            active_proj = values['KT']
            print('active project:', active_proj)
            if not paused:
                proj_start_time = time_int()
            elif switch_proj & paused:
                paused_time = proj_start_time = time_int()
                current_time = 0
            else:
                proj_start_time = proj_start_time + time_int() - paused_time

    if event == 'switch_proj':
        switch_proj = True
        window2['KT'].update(disabled=False)
        window2['add2'].update(disabled=False)
        active_proj = values['KT']
        time1 = (current_time * tfac // 100) // 60
        print('active proj 0 time (mins):', time1)
        for i in [i for i, x in enumerate(listKT) if x == active_proj]: # locate active project list in mainlist
            pos = i
            listi = mainlist[pos]
            listi.append(time1)
            mainlist[pos] = listi  # This reassigns updated list in the mainlist
            print('mainlist after project switch:', mainlist)
        paused_time = proj_start_time = time_int()
        current_time = 0
        window2['currentKT'].update('...')
        window2['projcomment'].update('')
        window2['KTupdate'].update('')
        window2['currentKT2'].update('')
    else:
        switch_proj = False

    if event == 'ip2':
        ip2_active = True
        projcomment_active = False
        enter_active = False
        enter_pause = False

    if event == 'projcomment':
        ip2_active = False
        projcomment_active = True
        enter_active = False
        enter_pause = False


    if event == 'add2':
        add2 = True
        newKT = values['ip2']
        if len(newKT) == 0:
            window2['KTupdate'].update('New project added:')
            window2['currentKT2'].update(' Field empty! :( ')
        else:
            listKT.append(newKT)
            window2['KTupdate'].update('New project added:')
            window2['currentKT2'].update(newKT)
            window2['ip2'].update('')
            window2.Element('KT').update(values=listKT)
            window2['KT'].update(disabled=False)
            mainlist.append([0])
            summarylist.append([0])
            required_list.append([0])
            commentlist.append([''])

    if event == 'comment':
        comment_active = True
        comment = values['projcomment']
        if values['KT'] == 'Select...':
            window2['currentKT'].update('Select Project!')
            window2['currentKT'].update(text_color='orange red')
        elif len(comment) == 0:
            window2['KTupdate'].update('Comment not recorded.')
            window2['currentKT2'].update(' Field empty! :( ')
            window2['currentKT'].update(values['KT'])
            window2['currentKT'].update(text_color='blanched almond')
        else:
            window2['currentKT'].update(values['KT'])
            window2['currentKT'].update(text_color='blanched almond')
            window2['KTupdate'].update('Comment recorded.')
            window2['currentKT2'].update('')
            comment = values['projcomment']
            # storing comments
            proj = values['KT']
            for i in [i for i, x in enumerate(listKT) if x == proj]:  # locate active project list in mainlist
                pos = i
                commlisti = commentlist[pos]
                commlisti.append(comment)
                commentlist[pos] = commlisti  # This reassigns updated list in the mainlist
                print('commentlist after project comment:', commentlist)

    # Add capability to allow enter as button click
    if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):  # Check for ENTER key
            if ip2_active:  # if it's a button element, click it
                elem = window2['add2']  # target element
                elem.Click()  # check for buttons that have been clicked
            if projcomment_active:
                elem = window2['comment']  # target element
                elem.Click()  # check for buttons that have been clicked
            if enter_active:
                elem = window2['pause']
                elem.Click()
            if enter_pause:
                elem = window2['active']
                elem.Click()

    if event == 'summary':
        active_proj = values['KT']
        n = len(listKT)
        time1 = (current_time * tfac // 100) // 60
        for i in [i for i, x in enumerate(listKT) if x == active_proj]:
            pos = i
            list_i = summarylist[pos]
            list_i[0] = time1
            required_list = mainlist
            required_list[pos] = list_i
            print('summarylist on summary click:', summarylist)
        # Now you have recorded all the individual project times as elements of corresponding list inside the mainlist
        # generate popup with all time calculation
        stime_list = [0]
        sproj_list = [0]
        for j in range(1, n):
            sunit_list = required_list[j]
            sunit_time = sum(sunit_list) # later add comments to shelf too. check if you can change popup window size
            stime_list.append(sunit_time)
            sunit_proj = listKT[j]
            sproj_list.append(sunit_proj)

        required_list = mainlist
        required_list[pos] = summarylist[pos]
        # for comments
        finalcomm_list = ['']
        for j in range(1, n):
            unit_commlist = commentlist[j]
            unit_comment = '.'.join(unit_commlist)
            finalcomm_list.append(unit_comment)

        sg.popup('Hi {}!'.format(username), '_________________________________________________________',
                 '<Session summary>', 'Start time: {}'.format(start_time), '',
                 'All projects:', (sproj_list[1:n + 1]), '', 'Total time (mins):', stime_list[1:n + 1], '',
                 'All comments:', finalcomm_list[1:n + 1], '',
                 '_________________________________________________________', 'Session in progress...', '',
                 text_color='blanched almond', font=['Consolas', 12], grab_anywhere=False,
                 button_color=('black', 'orange'), any_key_closes=True, title='TrackWork summary')

        # reset first value of summarylist back to zero
        for i in [i for i, x in enumerate(listKT) if x == active_proj]:
            pos = i
            list_i = summarylist[pos]
            list_i[0] = 0
            summarylist[pos] = list_i

    if event == 'end':
        active_proj = values['KT']
        time1 = (current_time * tfac // 100) // 60
        for i in [i for i, x in enumerate(listKT) if x == active_proj]:
            pos = i
            listi = mainlist[pos]
            listi.append(time1)
            mainlist[pos] = listi
            print('mainlist after project end:', mainlist)
        # Now you have recorded all the individual project times as elements of corresponding list inside the mainlist
        # generate popup with all time calculation
        n = len(listKT)
        time_list = [0]
        proj_list = [0]
        for j in range(1, n):
            unit_list = mainlist[j]
            unit_time = sum(unit_list)
            time_list.append(unit_time)
            unit_proj = listKT[j]
            proj_list.append(unit_proj)
            print('Total time for project:', unit_proj, 'is:', unit_time, 'mins')
        paused_time = proj_start_time = time_int()
        current_time = 0
        window2['currentKT'].update('...')
        window2['KT'].update(disabled=False)
        window2['switch_proj'].update(disabled=True)
        window2['status'].update('...')
        window2['status'].update(text_color='blanched almond')
        window2['projcomment'].update('')
        window2['KTupdate'].update('')
        window2['currentKT2'].update('')
        window2['add2'].update(disabled=True)

        # for comments
        finalcomm_list = ['']
        for j in range(1, n):
            unit_commlist = commentlist[j]
            unit_comment = '.'.join(unit_commlist)
            finalcomm_list.append(unit_comment)

        # end time
        localtime = time.localtime()
        end_day_hr = localtime[3]
        end_day_min = localtime[4]
        end_day_sec = localtime[5]
        end_time = '{:02d}:{:02d}:{:02d}'.format(end_day_hr, end_day_min, end_day_sec)

        sg.popup('Hi {}!'.format(username), '_________________________________________________________',
                 '<Session summary>', 'Start time: {}'.format(start_time), 'End time: {}'.format(end_time), '',
                 'All projects:', proj_list[1:n + 1], '', 'Total time (mins):', time_list[1:n + 1], '',
                 'All comments:', finalcomm_list[1:n + 1], '',
                 '_________________________________________________________',
                 'Session ended and reset. Session summary exported to text file.', '',
                 text_color='blanched almond', font=['Consolas', 12], grab_anywhere=False,
                 button_color=('black', 'orange'), any_key_closes=True, title='TrackWork summary')

        # export summary to text file
        end_time_text = '{:02d}.{:02d}.{:02d}'.format(end_day_hr, end_day_min, end_day_sec)
        date_time = start_date + '_' + end_time_text
        filename = 'TrackWork_summary_{}.txt'.format(date_time)
        heading = 'TrackWork session summary'
        text2 = 'Start date: {}'.format(start_date)
        text3 = 'End time: {}'.format(end_time)

        all_projects = 'All projects:'
        s1 = proj_list[1:n + 1]
        text4 = ' | '.join([str(elem) for elem in s1])

        t_time = 'Total time (mins):'
        s2 = time_list[1:n + 1]
        text5 = ' | '.join([str(elem) for elem in s2])

        all_comms = 'All comments: {}'
        s3 = finalcomm_list[1:n + 1]
        text6 = ' | '.join([str(elem) for elem in s3])

        file = open(filename, 'x')
        text = "\n".join([heading, text2, text3, '', all_projects, text4, '', t_time, text5, '', all_comms, text6])
        file.write(text)
        file.close()

        # to reset all values to zero, repeat all calc here and set to zero
        for j in range(0, n):
            mainlist[j] = summarylist[j] = required_list[j] = [0]  # replace j element of empty mainlist with new value

    if event == 'close':
        active_proj = values['KT']
        time1 = (current_time * tfac // 100) // 60
        for i in [i for i, x in enumerate(listKT) if x == active_proj]:
            pos = i
            listi = mainlist[pos]
            listi.append(time1)
            mainlist[pos] = listi
            print('mainlist after project end:', mainlist)
        # generate popup with all time calculation
        n = len(listKT)
        time_list = [0]
        proj_list = [0]
        for j in range(1, n):
            unit_list = mainlist[j]
            unit_time = sum(unit_list)
            time_list.append(unit_time)
            unit_proj = listKT[j]
            proj_list.append(unit_proj)
            print('Total time for project:', unit_proj, 'is:', unit_time,'mins')

        # for comments
        finalcomm_list = ['']
        for j in range(1, n):
            unit_commlist = commentlist[j]
            unit_comment = '.'.join(unit_commlist)
            finalcomm_list.append(unit_comment)

        # end time
        localtime = time.localtime()
        end_day_hr = localtime[3]
        end_day_min = localtime[4]
        end_day_sec = localtime[5]
        end_time = '{:02d}:{:02d}:{:02d}'.format(end_day_hr, end_day_min, end_day_sec)

        sg.popup('Hi {}!'.format(username), '_________________________________________________________',
                 '<Session summary>', 'Start time: {}'.format(start_time), 'End time: {}'.format(end_time), '',
                 'All projects:', proj_list[1:n + 1], '', 'Total time (mins):', time_list[1:n + 1], '',
                 'All comments:', finalcomm_list[1:n + 1], '',
                 '_________________________________________________________',
                 'Session ended. Session summary exported to text file.', 'App will now close.', '',
                 text_color='blanched almond', font=['Consolas', 12], grab_anywhere=False,
                 button_color=('black', 'orange'), any_key_closes=True, title='TrackWork summary')

        # export summary to text file
        end_time_text = '{:02d}.{:02d}.{:02d}'.format(end_day_hr, end_day_min, end_day_sec)
        date_time = start_date + '_' + end_time_text
        filename = 'TrackWork_summary_{}.txt'.format(date_time)
        heading = 'TrackWork session summary'
        text2 = 'Start date: {}'.format(start_date)
        text3 = 'End time: {}'.format(end_time)

        all_projects = 'All projects:'
        s1 = proj_list[1:n + 1]
        text4 = ' | '.join([str(elem) for elem in s1])

        t_time = 'Total time (mins):'
        s2 = time_list[1:n + 1]
        text5 = ' | '.join([str(elem) for elem in s2])

        all_comms = 'All comments: {}'
        s3 = finalcomm_list[1:n + 1]
        text6 = ' | '.join([str(elem) for elem in s3])

        file = open(filename, 'x')
        text = "\n".join([heading, text2, text3, '', all_projects, text4, '', t_time, text5, '', all_comms, text6])
        file.write(text)
        file.close()

        # Update databases
        db = dbm.open('tw_db', 'c')
        db['username'] = username
        print('db username:', username)
        # shelve lists
        sh = shelve.open('shelve_tw_db', 'c')
        sh['list'] = listKT
        listKT = sh['list']
        co = shelve.open('comm_tw_db', 'c')
        co['comments'] = commentlist
        commentlist = co['comments']
        print('Final shelved listKT:', sh['list'])
        print('Final shelved commlist:', co['comments'])
        sh.close()
        co.close()
        db.close()

        window2.close()
        break

    if event == sg.WIN_CLOSED:
        # Update databases
        db = dbm.open('tw_db', 'c')
        db['username'] = username
        print('db username:', username)
        # shelve lists
        sh = shelve.open('shelve_tw_db', 'c')
        sh['list'] = listKT
        listKT = sh['list']
        co = shelve.open('comm_tw_db', 'c')
        co['comments'] = commentlist
        commentlist = co['comments']
        print('Final shelved listKT:', sh['list'])
        print('Final shelved commlist:', co['comments'])
        sh.close()
        co.close()
        db.close()

        window2.close()
        break

    window2['time'].update('{:02d}:{:02d}:{:02d}'.format(((current_time*tfac // 100) // 60) // 60,
                                                         ((current_time*tfac // 100) // 60) % 60,
                                                        (current_time*tfac // 100) % 60))
    window2['start_time'].update(start_time)
    window2['start_date'].update(start_date)
    window2['start_day'].update(week_day)
    window2['cald_week'].update('{:02d}'.format(week_number))

#end