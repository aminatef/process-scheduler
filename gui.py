from tkinter import *
from cpu_scheduler import *


def add_proccess():
    sch_type = choice.get()
    if sch_type == 1:
        list_pro.append(Process("P"+str(1+len(list_pro)),
                                int(arrival1.get()), int(Brust1.get())))
        Label(master, text="Number of Processes you entered :" +
              str(len(list_pro))).grid(row=30, sticky=W)
        arrival1.delete(0, END)
        Brust1.delete(0, 'end')

    elif sch_type == 2:
        list_pro.append(Process("P"+str(1+len(list_pro)),
                                int(arrival2.get()), int(Brust2.get())))
        Label(master, text="Number of Processes you entered :" +
              str(len(list_pro))).grid(row=30, sticky=W)
        arrival2.delete(0, END)
        Brust2.delete(0, END)

    elif sch_type == 3:
        list_pro.append(Process("P"+str(1+len(list_pro)),
                                int(arrival3.get()), int(Brust3.get()), int(Priorty.get())))
        Label(master, text="Number of Processes you entered :" +
              str(len(list_pro))).grid(row=30, sticky=W)
        arrival3.delete(0, END)
        Brust3.delete(0, END)
        Priorty.delete(0, END)

    elif sch_type == 4:

        list_pro.append(Process("P"+str(1+len(list_pro)),
                                int(arrival4.get()), int(Brust4.get())))
        Label(master, text="Number of Processes you entered :" +
              str(len(list_pro))).grid(row=30, sticky=W)
        arrival4.delete(0, END)
        Brust4.delete(0, END)


def PlotGant():
    sch_type = int(choice.get())
    scheduler = Scheduler(*list_pro)
    Label(master, text="Number of Processes you entered :" +
          str(0)).grid(row=30, sticky=W)
    if sch_type == 1:
        result = scheduler.FCFS()
        list_pro.clear()
        create_gantt(result,scheduler)
        
        print(result)

    elif sch_type == 2:
        result = scheduler.SJF(Preemtive1.get())
        list_pro.clear()
        create_gantt(result,scheduler)
        
        print(result)

    elif sch_type == 3:
        result = scheduler.priority_scheduleing(Preemtive2.get())
        list_pro.clear()
        create_gantt(result,scheduler)
        
        print(result)

    elif sch_type == 4:
        quantum = int(q.get())
        result = scheduler.RR(quantum)
        list_pro.clear()
        create_gantt(result,scheduler)
        
        print(result)


def create_gantt(result,scheduler):

    gant = Tk(className="Gantt Chart")

    w = Canvas(gant, width=1200, height=100)
    w.pack()
    s = ["red", "green"]
    sel = 0
    time = 50
    # getting all running time
    runningtime = 0
    for i in result:
        runningtime = runningtime + (i["endTime"])-(i["startTime"])
    # -------------------
    print(runningtime)
    for i in result:
        sel = (sel+1) % len(s)
        duration = (i["endTime"])-(i["startTime"])

        scaled_duration = (duration*1100)/runningtime

        upper_x = time
        time += scaled_duration
        lower_x = time
        w.create_rectangle(upper_x, 0, lower_x, 50, fill=s[sel])

        x = (upper_x + lower_x)/2
        y = 50/2
        w.create_text(x, y, text=i["Pname"])

        x = (upper_x)
        y = 60

        w.create_text(x, y, text=str(i["startTime"]))

    x = time  # ((int(result[-1]["endTime"])*scaled_duration))
    y = 60
    w.create_text(x, y, text=str(i["endTime"]))
    w.create_text(1200/2, 80, text="Avarage aiting Time: "+str(scheduler.get_avarege_waiting_time(result)))

    gant.mainloop()


master = Tk(className="Scheduler")

master.geometry("600x700")
list_pro = list()
#new_win = Tk(className="States")

choice = IntVar()
Radiobutton(master, text="FCFS", variable=choice,
            value=1).grid(row=0, sticky=W)
Label(master,
      text="arrival time").grid(row=1, column=0)
Label(master,
      text="brust time").grid(row=1, column=3)
arrival1 = Entry(master)
arrival1.grid(row=2, column=0)

Brust1 = Entry(master)

Brust1.grid(row=2, column=3)

Button(master,
       text='Add Proccess', command=add_proccess).grid(row=3, sticky=W)


Radiobutton(master, text="SJF", variable=choice, value=2).grid(row=4, sticky=W)
Preemtive1 = IntVar()
Radiobutton(master, text="Preemtive", variable=Preemtive1,
            value=1).grid(row=5, sticky=W)
Radiobutton(master, text="non-Preemtive", variable=Preemtive1,
            value=0).grid(row=6, sticky=W)

Label(master,
      text="arrival time").grid(row=7, column=0)
Label(master,
      text="brust time").grid(row=7, column=3)

arrival2 = Entry(master)
arrival2.grid(row=8, column=0)

Brust2 = Entry(master)
Brust2.grid(row=8, column=3)
Button(master,
       text='Add Proccess', command=add_proccess).grid(row=9, sticky=W, column=0)


Radiobutton(master, text="Priorty", variable=choice,
            value=3).grid(row=10, sticky=W)
Preemtive2 = IntVar()
Radiobutton(master, text="Preemtive", variable=Preemtive2,
            value=1).grid(row=11, sticky=W)
Radiobutton(master, text="non-Preemtive", variable=Preemtive2,
            value=0).grid(row=12, sticky=W)
Label(master,
      text="arrival time").grid(row=13, column=0)
Label(master,
      text="brust time").grid(row=13, column=3)
Label(master,
      text="Priorty").grid(row=13, column=6)

arrival3 = Entry(master)
arrival3.grid(row=14, column=0)

Brust3 = Entry(master)
Brust3.grid(row=14, column=3)

Priorty = Entry(master)
Priorty.grid(row=14, column=6)
Button(master,
       text='Add Proccess', command=add_proccess).grid(row=15, sticky=W, column=0)


Radiobutton(master, text="RR", variable=choice, value=4).grid(row=16, sticky=W)
Label(master,
      text="arrival time").grid(row=17, column=0)
Label(master,
      text="brust time").grid(row=17, column=3)

arrival4 = Entry(master)
arrival4.grid(row=18, column=0)

Brust4 = Entry(master)
Brust4.grid(row=18, column=3)
Button(master,
       text='Add Proccess', command=add_proccess).grid(row=19, sticky=W, column=0)
Label(master,
      text="quantum").grid(row=20)

q = Entry(master)
q.grid(row=21)


Button(master,
       text='Plot ', command=PlotGant).grid(row=22, sticky=W, column=0)

Label(master,
      text="steps:").grid(row=23, column=0, sticky=W)
Label(master,
      text="1)choose the schudeling algorthim").grid(row=24, column=0, sticky=W)
Label(master,
      text="2) enter the neccesery inputs").grid(row=25, column=0, sticky=W)
Label(master,
      text="3)press add Proccess").grid(row=26, column=0, sticky=W)
Label(master,
      text="4)do step 3 and 4 for A number of Proccesses").grid(row=27, column=0, sticky=W)
Label(master,
      text="5)press plot").grid(row=28, column=0, sticky=W)


master.mainloop()
