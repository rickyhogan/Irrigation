from Tkinter import *
import Tkinter as tk
import RPi.GPIO as GPIO
import megaio
import time,sys

GPIO.setmode(GPIO.BOARD)
global inpt
inpt = 37
GPIO.setup(inpt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
global pump
pump = 35
GPIO.setup(pump,GPIO.OUT)

stack = [0,1,2]
relay = [1,2,3,4,5,6,7,8]

rate_count= 0
total_count = 0.0
purge_count = 0.0
drain_amount = 0.0
constant = 315 # 630 = half gallon
purged = 630
purging = True

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
    
class start(tk.Tk):
    
    def __init__(self, *args, **kwargs):
       
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        tk.Tk.title(self, "Plants")
        self.labels()
        self.check_buttons()
        self.drop_box()
        self.buttons()
        self.listboxs()
        
    def labels(self):
        feed_left = Label(self, text='Feed :')
        feed_right = Label(self, text='Feed :')
        amount_left = Label(self, text='Amount :')
        amount_right = Label(self, text='Amount :')
        plant_label1 = Label(self, text='Plant 1')
        plant_label2 = Label(self, text='Plant 2')
        plant_label3 = Label(self, text='Plant 3')
        plant_label4 = Label(self, text='Plant 4')
        plant_label5 = Label(self, text='Plant 5')
        plant_label6 = Label(self, text='Plant 6')
        plant_label7 = Label(self, text='Plant 7')
        plant_label8 = Label(self, text='Plant 8')
        plant_label9 = Label(self, text='Plant 9')
        plant_label10 = Label(self, text='Plant 10')
        plant_label11 = Label(self, text='Plant 11')
        plant_label12 = Label(self, text='Plant 12')
        plant_label13 = Label(self, text='Plant 13')
        plant_label14 = Label(self, text='Plant 14')
        plant_label15 = Label(self, text='Plant 15')
        plant_label16 = Label(self, text='Plant 16')
        plant_label17 = Label(self, text='Plant 17')
        plant_label18 = Label(self, text='Plant 18')
        plant_label19 = Label(self, text='Plant 19')
        plant_label20 = Label(self, text='Plant 20')
        plant_label21 = Label(self, text='Plant 21')
        plant_label22 = Label(self, text='Plant 22')
        plant_label23 = Label(self, text='Plant 23')
        plant_label24 = Label(self, text='Plant 24')
        rate_count_label = Label(self, text='Meter Count :')
        total_count_label = Label(self, text='Total Gallons :')
        global rate_count_var
        rate_count_var = StringVar()
        rate_count_var_label = Label(self, textvariable=rate_count_var)
        global total_count_var
        total_count_var = StringVar()
        total_count_var_label = Label(self, textvariable=total_count_var)
        feed_left.grid(row=0 ,column=1 ,pady=2 ,padx=2)
        feed_right.grid(row=0 ,column=4 ,pady=2 ,padx=2)
        amount_left.grid(row=0 ,column=2 ,pady=2 ,padx=2)
        amount_right.grid(row=0 ,column=5 ,pady=2 ,padx=2)
        plant_label1.grid(row=1 ,column=0 ,pady=2 ,padx=2)
        plant_label2.grid(row=2 ,column=0 ,pady=2 ,padx=2)
        plant_label3.grid(row=3 ,column=0 ,pady=2 ,padx=2)
        plant_label4.grid(row=4 ,column=0 ,pady=2 ,padx=2)
        plant_label5.grid(row=5 ,column=0 ,pady=2 ,padx=2)
        plant_label6.grid(row=6 ,column=0 ,pady=2 ,padx=2)
        plant_label7.grid(row=7 ,column=0 ,pady=2 ,padx=2)
        plant_label8.grid(row=8 ,column=0 ,pady=2 ,padx=2)
        plant_label9.grid(row=9 ,column=0 ,pady=2 ,padx=2)
        plant_label10.grid(row=10 ,column=0 ,pady=2 ,padx=2)
        plant_label11.grid(row=11 ,column=0 ,pady=2 ,padx=2)
        plant_label12.grid(row=12 ,column=0 ,pady=2 ,padx=2)
        plant_label13.grid(row=1 ,column=3 ,pady=2 ,padx=2)
        plant_label14.grid(row=2 ,column=3 ,pady=2 ,padx=2)
        plant_label15.grid(row=3 ,column=3 ,pady=2 ,padx=2)
        plant_label16.grid(row=4 ,column=3 ,pady=2 ,padx=2)
        plant_label17.grid(row=5 ,column=3 ,pady=2 ,padx=2)
        plant_label18.grid(row=6 ,column=3 ,pady=2 ,padx=2)
        plant_label19.grid(row=7 ,column=3 ,pady=2 ,padx=2)
        plant_label20.grid(row=8 ,column=3 ,pady=2 ,padx=2)
        plant_label21.grid(row=9 ,column=3 ,pady=2 ,padx=2)
        plant_label22.grid(row=10 ,column=3 ,pady=2 ,padx=2)
        plant_label23.grid(row=11 ,column=3 ,pady=2 ,padx=2)
        plant_label24.grid(row=12 ,column=3 ,pady=2 ,padx=2)
        rate_count_label.grid(row=14 ,column=0 ,pady=2 ,padx=2)
        rate_count_var_label.grid(row=14 ,column=1 ,pady=2 ,padx=2)
        total_count_label.grid(row=14 ,column=3 ,pady=2 ,padx=2)
        total_count_var_label.grid(row=14 ,column=4 ,pady=2 ,padx=2)

    def check_buttons(self):
        
        global v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15
        global v16,v17,v18,v19,v20,v21,v22,v23,v24
        
        v1 = IntVar(value=1)
        v2 = IntVar(value=1)
        v3 = IntVar(value=1)
        v4 = IntVar(value=1)
        v5 = IntVar(value=1)
        v6 = IntVar(value=1)
        v7 = IntVar(value=1)
        v8 = IntVar(value=1)
        v9 = IntVar(value=1)
        v10 = IntVar(value=1)
        v11 = IntVar(value=1)
        v12 = IntVar(value=1)
        v13 = IntVar(value=1)
        v14 = IntVar(value=1)
        v15 = IntVar(value=1)
        v16 = IntVar(value=1)
        v17 = IntVar(value=1)
        v18 = IntVar(value=1)
        v19 = IntVar(value=1)
        v20 = IntVar(value=1)
        v21 = IntVar(value=1)
        v22 = IntVar(value=1)
        v23 = IntVar(value=1)
        v24 = IntVar(value=1)
        c1 = Checkbutton(self, variable=v1)
        c2 = Checkbutton(self, variable=v2)
        c3 = Checkbutton(self, variable=v3)
        c4 = Checkbutton(self, variable=v4)
        c5 = Checkbutton(self, variable=v5)
        c6 = Checkbutton(self, variable=v6)
        c7 = Checkbutton(self, variable=v7)
        c8 = Checkbutton(self, variable=v8)
        c9 = Checkbutton(self, variable=v9)
        c10 = Checkbutton(self, variable=v10)
        c11 = Checkbutton(self, variable=v11)
        c12 = Checkbutton(self, variable=v12)
        c13 = Checkbutton(self, variable=v13)
        c14 = Checkbutton(self, variable=v14)
        c15 = Checkbutton(self, variable=v15)
        c16 = Checkbutton(self, variable=v16)
        c17 = Checkbutton(self, variable=v17)
        c18 = Checkbutton(self, variable=v18)
        c19 = Checkbutton(self, variable=v19)
        c20 = Checkbutton(self, variable=v20)
        c21 = Checkbutton(self, variable=v21)
        c22 = Checkbutton(self, variable=v22)
        c23 = Checkbutton(self, variable=v23)
        c24 = Checkbutton(self, variable=v24)
        c1.grid(row=1 ,column=1 ,padx=2 ,pady=2)
        c2.grid(row=2 ,column=1 ,padx=2 ,pady=2)
        c3.grid(row=3 ,column=1 ,padx=2 ,pady=2)
        c4.grid(row=4 ,column=1 ,padx=2 ,pady=2)
        c5.grid(row=5 ,column=1 ,padx=2 ,pady=2)
        c6.grid(row=6 ,column=1 ,padx=2 ,pady=2)
        c7.grid(row=7 ,column=1 ,padx=2 ,pady=2)
        c8.grid(row=8 ,column=1 ,padx=2 ,pady=2)
        c9.grid(row=9 ,column=1 ,padx=2 ,pady=2)
        c10.grid(row=10 ,column=1 ,padx=2 ,pady=2)
        c11.grid(row=11 ,column=1 ,padx=2 ,pady=2)
        c12.grid(row=12 ,column=1 ,padx=2 ,pady=2)
        c13.grid(row=1 ,column=4 ,padx=2 ,pady=2)
        c14.grid(row=2 ,column=4 ,padx=2 ,pady=2)
        c15.grid(row=3 ,column=4 ,padx=2 ,pady=2)
        c16.grid(row=4 ,column=4 ,padx=2 ,pady=2)
        c17.grid(row=5 ,column=4 ,padx=2 ,pady=2)
        c18.grid(row=6 ,column=4 ,padx=2 ,pady=2)
        c19.grid(row=7 ,column=4 ,padx=2 ,pady=2)
        c20.grid(row=8 ,column=4 ,padx=2 ,pady=2)
        c21.grid(row=9 ,column=4 ,padx=2 ,pady=2)
        c22.grid(row=10 ,column=4 ,padx=2 ,pady=2)
        c23.grid(row=11 ,column=4 ,padx=2 ,pady=2)
        c24.grid(row=12 ,column=4 ,padx=2 ,pady=2)
        
    def drop_box(self):
        global options
        options = ['.25 gallon','.50 gallon','.75 gallon','1 gallon','1.25 gallon',
                        '1.50 gallon','1.75 gallon','2 gallon','2.25 gallon','2.50 gallon',
                        '2.75 gallon','3 gallon']
        self.drop1 = StringVar()
        self.drop2 = StringVar()
        self.drop3 = StringVar()
        self.drop4 = StringVar()
        self.drop5 = StringVar()
        self.drop6 = StringVar()
        self.drop7 = StringVar()
        self.drop8 = StringVar()
        self.drop9 = StringVar()
        self.drop10 = StringVar()
        self.drop11 = StringVar()
        self.drop12 = StringVar()
        self.drop13 = StringVar()
        self.drop14 = StringVar()
        self.drop15 = StringVar()
        self.drop16 = StringVar()
        self.drop17 = StringVar()
        self.drop18 = StringVar()
        self.drop19 = StringVar()
        self.drop20 = StringVar()
        self.drop21 = StringVar()
        self.drop22 = StringVar()
        self.drop23 = StringVar()
        self.drop24 = StringVar()
        self.drop1.set(options[3])
        self.drop2.set(options[3])
        self.drop3.set(options[3])
        self.drop4.set(options[3])
        self.drop5.set(options[3])
        self.drop6.set(options[3])
        self.drop7.set(options[3])
        self.drop8.set(options[3])
        self.drop9.set(options[3])
        self.drop10.set(options[3])
        self.drop11.set(options[3])
        self.drop12.set(options[3])
        self.drop13.set(options[3])
        self.drop14.set(options[3])
        self.drop15.set(options[3])
        self.drop16.set(options[3])
        self.drop17.set(options[3])
        self.drop18.set(options[3])
        self.drop19.set(options[3])
        self.drop20.set(options[3])
        self.drop21.set(options[3])
        self.drop22.set(options[3])
        self.drop23.set(options[3])
        self.drop24.set(options[3])
        option1 = OptionMenu(self, self.drop1, *options)
        option2 = OptionMenu(self, self.drop2, *options)
        option3 = OptionMenu(self, self.drop3, *options)
        option4 = OptionMenu(self, self.drop4, *options)
        option5 = OptionMenu(self, self.drop5, *options)
        option6 = OptionMenu(self, self.drop6, *options)
        option7 = OptionMenu(self, self.drop7, *options)
        option8 = OptionMenu(self, self.drop8, *options)
        option9 = OptionMenu(self, self.drop9, *options)
        option10 = OptionMenu(self, self.drop10, *options)
        option11 = OptionMenu(self, self.drop11, *options)
        option12 = OptionMenu(self, self.drop12, *options)
        option13 = OptionMenu(self, self.drop13, *options)
        option14 = OptionMenu(self, self.drop14, *options)
        option15 = OptionMenu(self, self.drop15, *options)
        option16 = OptionMenu(self, self.drop16, *options)
        option17 = OptionMenu(self, self.drop17, *options)
        option18 = OptionMenu(self, self.drop18, *options)
        option19 = OptionMenu(self, self.drop19, *options)
        option20 = OptionMenu(self, self.drop20, *options)
        option21 = OptionMenu(self, self.drop21, *options)
        option22 = OptionMenu(self, self.drop22, *options)
        option23 = OptionMenu(self, self.drop23, *options)
        option24 = OptionMenu(self, self.drop24, *options)
        option1.grid(row=1 ,column=2 ,padx=2 ,pady=2)
        option2.grid(row=2 ,column=2 ,padx=2 ,pady=2)
        option3.grid(row=3 ,column=2 ,padx=2 ,pady=2)
        option4.grid(row=4 ,column=2 ,padx=2 ,pady=2)
        option5.grid(row=5 ,column=2 ,padx=2 ,pady=2)
        option6.grid(row=6 ,column=2 ,padx=2 ,pady=2)
        option7.grid(row=7 ,column=2 ,padx=2 ,pady=2)
        option8.grid(row=8 ,column=2 ,padx=2 ,pady=2)
        option9.grid(row=9 ,column=2 ,padx=2 ,pady=2)
        option10.grid(row=10 ,column=2 ,padx=2 ,pady=2)
        option11.grid(row=11 ,column=2 ,padx=2 ,pady=2)
        option12.grid(row=12 ,column=2 ,padx=2 ,pady=2)
        option13.grid(row=1 ,column=5 ,padx=2 ,pady=2)
        option14.grid(row=2 ,column=5 ,padx=2 ,pady=2)
        option15.grid(row=3 ,column=5 ,padx=2 ,pady=2)
        option16.grid(row=4 ,column=5 ,padx=2 ,pady=2)
        option17.grid(row=5 ,column=5 ,padx=2 ,pady=2)
        option18.grid(row=6 ,column=5 ,padx=2 ,pady=2)
        option19.grid(row=7 ,column=5 ,padx=2 ,pady=2)
        option20.grid(row=8 ,column=5 ,padx=2 ,pady=2)
        option21.grid(row=9 ,column=5 ,padx=2 ,pady=2)
        option22.grid(row=10 ,column=5 ,padx=2 ,pady=2)
        option23.grid(row=11 ,column=5 ,padx=2 ,pady=2)
        option24.grid(row=12 ,column=5 ,padx=2 ,pady=2)

    def buttons(self):
        global water,drain,cancel
        water = Button(self, text='Begin Water Cycle', command=lambda:self.start_cycle())
        water.grid(row=13, column=3, columnspan=5,pady=2, padx=2, sticky=E)
        drain = Button(self, text='Drain Tank', command=lambda: self.drain_tank())
        drain.grid(row=13, column=2, columnspan=3,padx=2,pady=2)
        cancel = Button(self, text='Cancel', command=lambda:self.ending())
        cancel.grid(row=13, column=0, columnspan=2,padx=2,pady=2)

    def listboxs(self):
        global listbox
        scrollbar = Scrollbar(self, orient=VERTICAL)
        listbox = Listbox(self, yscrollcommand=scrollbar.set)
        listbox.config(height=10,width=70,bg='black',fg='white')
        scrollbar.config(command=listbox.yview)
        listbox.grid(row=15,column=0,columnspan=6,padx=5,pady=5)
        listbox.insert(END,'Hello, press Cancel button at anytime to safely stop application')
        
    def start_cycle(self):
        global ta1,ta2,ta3,ta4,ta5,ta6,ta7,ta8,ta9,ta10,ta11,ta12,ta13,ta14,ta15,ta16,ta17
        global ta18,ta19,ta20,ta21,ta22,ta23,ta24
        ta1 = self.drop1.get()
        ta2 = self.drop2.get()
        ta3 = self.drop3.get()
        ta4 = self.drop4.get()
        ta5 = self.drop5.get()
        ta6 = self.drop6.get()
        ta7 = self.drop7.get()
        ta8 = self.drop8.get()
        ta9 = self.drop9.get()
        ta10 = self.drop10.get()
        ta11 = self.drop11.get()
        ta12 = self.drop12.get()
        ta13 = self.drop13.get()
        ta14 = self.drop14.get()
        ta15 = self.drop15.get()
        ta16 = self.drop16.get()
        ta17 = self.drop17.get()
        ta18 = self.drop18.get()
        ta19 = self.drop19.get()
        ta20 = self.drop20.get()
        ta21 = self.drop21.get()
        ta22 = self.drop22.get()
        ta23 = self.drop23.get()
        ta24 = self.drop24.get()
        drain.config(state='disabled')
        water.config(state='disabled')
        listbox.insert(END,'Cycle Starting')
        pump_control('on')
        listbox.insert(END,'Waiting 20 seconds')
        listbox.yview(END)
        app.update()
        time.sleep(20)
        listbox.insert(END,'Lines filled')
        try:
            listbox.insert(END,'start')
            listbox.yview(END)
            GPIO.add_event_detect(inpt,GPIO.FALLING, callback=runall)
        except:
            listbox.insert(END,'error with counter, Restart program')
            listbox.yview(END)
        
    def ending(self):
        water.config(state='disabled')
        drain.config(state='disabled')
        cancel.config(state='disabled')
        GPIO.remove_event_detect(inpt)
        listbox.insert(END,'exiting, Incomplete cycle')
        pump_control('off')
        solenoid_control(25,3,1,'on')
        listbox.insert(END,'dump tube opened')
        listbox.yview(END)
        for z in stack:
            for x in relay:
                megaio.set_relay(z,x,0)
                listbox.insert(END, 'stack '+ str(z) +', relay '+str(x)+ ' off')
                listbox.yview(END)
                app.update()
                time.sleep(0.5)
        listbox.insert(END,'Waiting 40 seconds')
        listbox.yview(END)
        app.update()
        time.sleep(40)
        solenoid_control(25,3,1,'off')
        megaio.set_relay(3,1,0)
        listbox.insert(END,'dump tube closed')
        GPIO.cleanup()
        listbox.insert(END,'Cycle Ended Prematurely')
        listbox.yview(END)
        water.config(state='normal')
        drain.config(state='normal')
        cancel.config(state='normal')

    def drain_tank(self):
        pump_control('on')
        solenoid_control(25,3,1,'on')
        water.config(state='disabled')
        drain.config(state='disabled')
        GPIO.add_event_detect(inpt,GPIO.FALLING, callback=draincount)

######################
        
def pump_control(a):
    GPIO.setmode(GPIO.BOARD)
    global inpt
    inpt = 37
    GPIO.setup(inpt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    global pump
    pump = 35
    GPIO.setup(pump,GPIO.OUT)
    if a == 'on':
        GPIO.output(pump,True)
        listbox.insert(END,'Pump On')
        listbox.yview(END)
    elif a == 'off':
        GPIO.output(pump,False)
        listbox.insert(END,'Pump Off')
        listbox.yview(END)
    else:
        listbox.insert(END,'invalid pump command')
        listbox.yview(END)

def solenoid_control(number,stack,relay,power):
    if power == 'on':
        power = 1
        listbox.insert(END,'relay '+ str(number)+' on')
        listbox.yview(END)
        megaio.set_relay(stack,relay,power)
    elif power == 'off':
        power = 0
        listbox.insert(END,'relay '+str(number)+' off')
        listbox.yview(END)
        megaio.set_relay(stack,relay,power)

####################

def purge():
    global rate_count
    rate_count = rate_count+1
    rate_count_var.set(rate_count)
    if rate_count == purged:
        global purge_count
        purge_count += 0.5
    
def pulsecount(a):
    global rate_count
    global plant_count
    feed_amount = int(constant) * int(a)
    plant_count = int(feed_amount)/int(constant)/4.0
    rate_count = rate_count+1
    rate_count_var.set(rate_count)
    if rate_count == feed_amount:
        global total_count
        total_count += plant_count
        total_count_var.set(total_count)

def draincount(object):
    global rate_count
    rate_count = rate_count+1
    rate_count_var.set(rate_count)
    if rate_count == constant:
        global drain_amount
        drain_amount += 0.25
        total_count_var.set(drain_amount)
        rate_count = 0

def feed_conversion(a):
    global total_amount
    if a == options[0]:
        total_amount = 1
    elif a == options[1]:
        total_amount = 2
    elif a == options[2]:
        total_amount = 3
    elif a == options[3]:
        total_amount = 4
    elif a == options[4]:
        total_amount = 5
    elif a == options[5]:
        total_amount = 6
    elif a == options[6]:
        total_amount = 7
    elif a == options[7]:
        total_amount = 8
    elif a == options[8]:
        total_amount = 9
    elif a == options[9]:
        total_amount = 10
    elif a == options[10]:
        total_amount = 11
    elif a == options[11]:
        total_amount = 12
######################
        
def purge_solenoid():
    global rate_count
    megaio.set_relay(3,1,1)
    purge()
    if rate_count == purged:
        solenoid_control(25,3,1,'off')
        megaio.set_relay(3,1,0)
        megaio.set_relay(3,1,0)
        listbox.insert(END,'purge solenoid closed')
        listbox.yview(END)
        global purging
        rate_count = 0
        purging = False

def solenoid_1(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(0,1,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(1,0,1,'off')
        megaio.set_relay(0,1,0)
        rate_count = 0
        v1.set(0)

def solenoid_2(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(0,2,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(2,0,2,'off')
        megaio.set_relay(0,2,0)
        rate_count = 0
        v2.set(0)

def solenoid_3(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(0,3,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(3,0,3,'off')
        megaio.set_relay(0,3,0)
        rate_count = 0
        v3.set(0)

def solenoid_4(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(0,4,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(4,0,4,'off')
        megaio.set_relay(0,3,0)
        rate_count = 0
        v4.set(0)

def solenoid_5(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(0,5,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(5,0,5,'off')
        megaio.set_relay(0,4,0)
        rate_count = 0
        v5.set(0)

def solenoid_6(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(0,6,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(6,0,6,'off')
        megaio.set_relay(0,6,0)
        rate_count = 0
        v6.set(0)

def solenoid_7(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(0,7,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(7,0,7,'off')
        megaio.set_relay(0,7,0)
        rate_count = 0
        v7.set(0)

def solenoid_8(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(0,8,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(8,0,8,'off')
        megaio.set_relay(0,8,0)
        rate_count = 0
        v8.set(0)

def solenoid_9(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(1,1,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(9,1,1,'off')
        megaio.set_relay(1,1,0)
        rate_count = 0
        v9.set(0)

def solenoid_10(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(1,2,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(10,1,2,'off')
        megaio.set_relay(1,2,0)
        rate_count = 0
        v10.set(0)

def solenoid_11(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(1,3,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(11,1,3,'off')
        megaio.set_relay(1,3,0)
        rate_count = 0
        v11.set(0)

def solenoid_12(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(1,4,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(12,1,4,'off')
        megaio.set_relay(1,4,0)
        rate_count = 0
        v12.set(0)

def solenoid_13(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(1,5,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(13,1,5,'off')
        megaio.set_relay(1,5,0)
        rate_count = 0
        v13.set(0)

def solenoid_14(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(1,6,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(14,1,6,'off')
        megaio.set_relay(1,6,0)
        rate_count = 0
        v14.set(0)

def solenoid_15(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(1,7,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(15,1,7,'off')
        megaio.set_relay(1,7,0)
        rate_count = 0
        v15.set(0)

def solenoid_16(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(1,8,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(16,1,8,'off')
        megaio.set_relay(1,8,0)
        rate_count = 0
        v16.set(0)

def solenoid_17(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(2,1,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(17,2,1,'off')
        megaio.set_relay(2,1,0)
        rate_count = 0
        v17.set(0)

def solenoid_18(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(2,2,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(18,2,2,'off')
        megaio.set_relay(2,2,0)
        rate_count = 0
        v18.set(0)

def solenoid_19(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(2,3,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(19,2,3,'off')
        megaio.set_relay(2,3,0)
        rate_count = 0
        v19.set(0)

def solenoid_20(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(2,4,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(20,2,4,'off')
        megaio.set_relay(2,4,0)
        rate_count = 0
        v20.set(0)

def solenoid_21(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(2,5,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(21,2,5,'off')
        megaio.set_relay(2,5,0)
        rate_count = 0
        v21.set(0)

def solenoid_22(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(2,6,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(22,2,6,'off')
        megaio.set_relay(2,6,0)
        rate_count = 0
        v22.set(0)

def solenoid_23(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(2,7,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(23,2,7,'off')
        megaio.set_relay(2,7,0)
        rate_count = 0
        v23.set(0)

def solenoid_24(a):
    global rate_count
    feeding = int(constant) * int(a)
    megaio.set_relay(2,8,1)
    pulsecount(a)
    if rate_count == feeding:
        solenoid_control(24,2,8,'off')
        megaio.set_relay(2,8,0)
        rate_count = 0
        v24.set(0)
        
######################

def runall(object):
    sol1 = v1.get()
    sol2 = v2.get()
    sol3 = v3.get()
    sol4 = v4.get()
    sol5 = v5.get()
    sol6 = v6.get()
    sol7 = v7.get()
    sol8 = v8.get()
    sol9 = v9.get()
    sol10 = v10.get()
    sol11 = v11.get()
    sol12 = v12.get()
    sol13 = v13.get()
    sol14 = v14.get()
    sol15 = v15.get()
    sol16 = v16.get()
    sol17 = v17.get()
    sol18 = v18.get()
    sol19 = v19.get()
    sol20 = v20.get()
    sol21 = v21.get()
    sol22 = v22.get()
    sol23 = v23.get()
    sol24 = v24.get()
    if purging == True:
        purge_solenoid()

    elif sol1 == 1:
        feed_conversion(ta1)
        solenoid_1(int(total_amount))
        
    elif sol2 == 1:
        feed_conversion(ta2)
        solenoid_2(int(total_amount))
        
    elif sol3 == 1:
        feed_conversion(ta3)
        solenoid_3(int(total_amount))
        
    elif sol4 == 1:
        feed_conversion(ta4)
        solenoid_4(int(total_amount))
        
    elif sol5 == 1:
        feed_conversion(ta5)
        solenoid_5(int(total_amount))
        
    elif sol6 == 1:
        feed_conversion(ta6)
        solenoid_6(int(total_amount))
        
    elif sol7 == 1:
        feed_conversion(ta7)
        solenoid_7(int(total_amount))
        
    elif sol8 == 1:
        feed_conversion(ta8)
        solenoid_8(int(total_amount))
        
    elif sol9 == 1:
        feed_conversion(ta9)
        solenoid_9(int(total_amount))
        
    elif sol10 == 1:
        feed_conversion(ta10)
        solenoid_10(int(total_amount))
        
    elif sol11 == 1:
        feed_conversion(ta11)
        solenoid_11(int(total_amount))
        
    elif sol12 == 1:
        feed_conversion(ta12)
        solenoid_12(int(total_amount))
        
    elif sol13 == 1:
        feed_conversion(ta13)
        solenoid_13(int(total_amount))
        
    elif sol14 == 1:
        feed_conversion(ta14)
        solenoid_14(int(total_amount))
        
    elif sol15 == 1:
        feed_conversion(ta15)
        solenoid_15(int(total_amount))
        
    elif sol16 == 1:
        feed_conversion(ta16)
        solenoid_16(int(total_amount))
        
    elif sol17 == 1:
        feed_conversion(ta17)
        solenoid_17(int(total_amount))
        
    elif sol18 == 1:
        feed_conversion(ta18)
        solenoid_18(int(total_amount))
        
    elif sol19 == 1:
        feed_conversion(ta19)
        solenoid_19(int(total_amount))
        
    elif sol20 == 1:
        feed_conversion(ta20)
        solenoid_20(int(total_amount))
        
    elif sol21 == 1:
        feed_conversion(ta21)
        solenoid_21(int(total_amount))
        
    elif sol22 == 1:
        feed_conversion(ta22)
        solenoid_22(int(total_amount))
        
    elif sol23 == 1:
        feed_conversion(ta23)
        solenoid_23(int(total_amount))
        
    elif sol24 == 1:
        feed_conversion(ta24)
        solenoid_24(int(total_amount))
        
    else:
        GPIO.remove_event_detect(inpt)
        pump_control('off')
        GPIO.cleanup()
        solenoid_control(25,3,1,'on')
        listbox.insert(END,'Opened dump tube')
        listbox.insert(END,'Waiting 40 seconds')
        listbox.yview(END)
        app.update()
        time.sleep(40)
        solenoid_control(25,3,1,'off')
        megaio.set_relay(3,1,0)
        megaio.set_relay(3,1,0)
        listbox.insert(END,'Closed dump tube')
        listbox.insert(END,'Watering cycle complete')
        listbox.yview(END)
        water.config(state='normal')
        drain.config(state='normal')
        
if __name__ == "__main__":
    
    app = start()
    center(app)
    app.mainloop()
