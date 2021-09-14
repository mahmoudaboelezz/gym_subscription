import random
from datetime import date, datetime
from PySimpleGUI.PySimpleGUI import Image
from dateutil.relativedelta import *
import sqlite3
import PySimpleGUI as sg

conn = sqlite3.connect('sub.db')
curs = conn.cursor()


layout = [[sg.Image(source='F:\work\Python\learning\sub_app.py\logo.png',background_color='black')],[sg.Text("PowerGym",background_color='black') ],
 [ sg.InputText(key='new_name',size=(20,50),do_not_clear=True , metadata='alo' , ),sg.Text("ألأسم",background_color='black')] 
 ,[sg.InputOptionMenu(['جيم','تخسيس','حديد'],key='new_type', size=(10,50) ),sg.Text("نوع الأشتراك",background_color='black')]
 ,[sg.Input(key='new_done', size=(10,50),do_not_clear=True),sg.Text("المدفوع",background_color='black')]
 ,[sg.Input(key='new_still',size=(10,50),do_not_clear=True),sg.Text("الباقي",background_color='black')], [sg.Button("New", size=(30,2)),
 sg.Text(" " , size=(30,1),background_color='black',key='out')] ,
 [sg.Button('done'),sg.Button('all')],[],[sg.Text("مسح الأعضاء الذين تمت فترة الأشتراك الخاصة بهم" ,size=(40,2),background_color='black')]
 , [ sg.Input(key='delet_name', size=(20,50),do_not_clear=True),sg.Text("أسم العضو",background_color='black')]
 ,[ sg.Input(key='delet_id', size=(10,50),do_not_clear=False),sg.Text("الكود الخاص به",background_color='black')],[sg.Button('مسح العضو') ,sg.Text(" " , size=(30,1),key='deleted',background_color='black')]  ]

# Create the window
window = sg.Window("أشتراك الجيم", layout ,margins=(30, 60),element_padding=5,icon='F:\work\Python\learning\sub_app.py\gym.ico',button_color='orange',background_color='black',titlebar_background_color="yellow",resizable=True)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "New" and values['new_name'] !="" and values['new_type'] != '' :
        name = values['new_name']
        type = ""
        for val in values['new_type']:
            type += val
        new_still = values['new_still']
        new_done = values['new_done']
        NOW = datetime.now()
        date_sub = date.today().strftime("%d/%m/%Y")
        month1 = NOW+relativedelta(months=+1)
        date1 = month1.strftime("%d/%m/%Y")
        ids = random.randint(1,1000)
        if values['new_still'] =='':
            if type == "حديد"  or type =="تخسيس":
                new_still = 100 - int(new_done)
            else:
                new_still = 150 - int(new_done)
        valuess = [(name, date_sub,date1,ids,type,new_done,new_still)]
        curs.executemany("insert into Member values (?,?,?,?,?,?,?);",valuess)
        conn.commit()
        window['out'].update(f"تم أضافة {name} \n بتاريخ {date_sub}")
        print(f"تم أضافة {name} \n بتاريخ {date_sub}")
        print("-----------------------------------------------------")
    elif event == 'close' or event== sg.WIN_CLOSED:

        window.close()
        exit()
    elif event == "done":
        NOW = datetime.now()
        date2 = NOW.strftime("%d/%m/%Y")
        dates = curs.execute("SELECT ids,name,still FROM Member WHERE date_end == ?",(date2,))
        rows = dates.fetchall()
        complete = []
        for row in rows:
            result = '   :   '.join(str(i) for i in row)
            result = result.replace(",","")
            complete.append(result)
        print('\n'.join(complete))
        print("-----------------------------------------------------")
        sg.popup_scrolled('\n'.join(complete))
     
    elif event == "all":
        dates = curs.execute("SELECT name,date_sub,ids,still FROM Member")
        rows = dates.fetchall()
        all =[] 
        for row in rows:
            result = '   :   '.join(str(i) for i in row)
            result = result.replace("'","")
            all.append(result)
        print('\n'.join(all))
        print("-----------------------------------------------------")
        sg.popup_scrolled('\n'.join(all))
    elif event == "مسح العضو":
        if values['delet_id'] == '' and values['delet_name'] != '':
            delets = curs.execute("DELETE FROM Member WHERE name=?",(values['delet_name'],))
            window['out'].update(f"تم مسح العضو  {values['delet_name']}")
            print(f"تم مسح العضو  {values['delet_name']}")
            print("-----------------------------------------------------")
        elif values['delet_id'] != '':
            delets = curs.execute("DELETE FROM Member WHERE ids=?",(values['delet_id'],))
            window['out'].update(f"تم مسح العضو صاحب الكود {values['delet_id']}")
            print(f"تم مسح العضو صاحب الكود {values['delet_id']}")
            print("-----------------------------------------------------")
        conn.commit()
        




conn.commit()
        

    
conn.close()


