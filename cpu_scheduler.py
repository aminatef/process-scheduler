from operator import attrgetter


class Process():

    processes_n = 0
    PID = 1

    def __init__(self, name, arr_t, burst_t, priorty=0):
        self.name = name  # process name
        self.arr_t = arr_t  # arrival time
        self.burst_t = burst_t  # burst time
        self.remain_t = burst_t  # remaining time
        self.priorty = priorty
        Process.processes_n += 1  # sebak men dool mesh mohemen awe ya3ne fe el logic
        Process.PID += 1

    def __str__(self):
        return f"PID: {self.name}"

    def __lt__(self, other):
        return self.arr_t < other.arr_t


class Scheduler():

    def __init__(self, *processes):
        self.processes = processes
        self.arr_t_sorted = sorted(
            processes, key=lambda process: process.arr_t)

    def FCFS(self):
        result = []
        alloc_t = 0
        for p in self.arr_t_sorted:
            start_t = alloc_t
            end_t = alloc_t+p.burst_t
            alloc_t += p.burst_t
            result.append(
                dict({"Pname": p.name, "startTime": start_t, "endTime": end_t}))
        return result

    def SJF(self, Preemptive=False):
        result = []
        pList = self.arr_t_sorted
        # store orig_values
        origvalues = []
        for p in self.processes:
            origvalues.append(dict(arr_t=p.arr_t, burst_t=p.burst_t,))
        # ----------------
        alloc_t = pList[0].arr_t
        if(Preemptive):
            n = len(pList)
            finished = 0
            while(finished != n):
                pList = sorted(pList, key=attrgetter('arr_t', 'remain_t'))
                size = len(pList)
                found = False
                for i in range(size):
                    for j in range(i, size):  # forloop for handling interrupt
                        remain = pList[i].remain_t + \
                            (pList[i].arr_t-pList[j].arr_t)
                        if(remain > pList[j].remain_t):
                            found = True
                            pList[i].remain_t = remain
                            consumed_t = pList[i].burst_t-remain
                            start_t = alloc_t
                            end_t = alloc_t+consumed_t
                            alloc_t += consumed_t
                            result.append(
                                dict({"Pname": pList[i].name, "startTime": start_t, "endTime": end_t}))
                            for k in range(j-1, -1, -1):
                                pList[k].arr_t += consumed_t
                            break
                    if (found):
                        break

                    else:  # process will finish with no interrupt
                        start_t = alloc_t
                        end_t = alloc_t + pList[i].remain_t
                        alloc_t += pList[i].remain_t
                        result.append(
                            dict({"Pname": pList[i].name, "startTime": start_t, "endTime": end_t}))
                        for p in range(i+1, size):
                            if pList[p].arr_t < pList[i].arr_t+pList[i].remain_t:
                                pList[p].arr_t = pList[i].remain_t + \
                                    pList[i].arr_t
                        pList[i].remain_t = 0
                        break
                # remove finished process
                for p in pList:
                    if (p.remain_t == 0):
                        pList.remove(p)
                        finished += 1

        else:
            for p in pList:
                start_t = alloc_t
                end_t = alloc_t+p.burst_t
                alloc_t += p.burst_t
                result.append(
                    dict({"Pname": p.name, "startTime": start_t, "endTime": end_t}))
        # load orig_values
        for p in range(len(self.processes)):
            self.processes[p].arr_t = origvalues[p]['arr_t']
            self.processes[p].burst_t = origvalues[p]['burst_t']
            self.processes[p].remain_t = origvalues[p]['burst_t']
        # ----------------
        return result

    def RR(self, quantum):
        bridge_list = []
        after_operations = []
        ordered_processes = self.arr_t_sorted
        l = 0
        while len(ordered_processes) > 0:
            for process in ordered_processes:
                if process.burst_t > quantum:
                    process.burst_t -= quantum
                    applied_process = {
                        "Pname": process.name, 'startTime': l, 'endTime': l+quantum}
                    l += quantum
                    bridge_list.append(process)
                    after_operations.append(applied_process)
                elif process.burst_t <= quantum:
                    applied_process = {
                        "Pname": process.name, 'startTime': l, 'endTime': l+process.burst_t}
                    l += process.burst_t
                    after_operations.append(applied_process)
            ordered_processes = []
            for process in bridge_list:
                ordered_processes.append(process)
            bridge_list = []

        return after_operations

    def get_processes_toRun(self, time):
        list_proccesses = list()
        for i in range(len(self.arr_t_sorted)):
            if self.arr_t_sorted[i].arr_t <= time and self.arr_t_sorted[i].remain_t != 0:
                list_proccesses.append(self.arr_t_sorted[i])
        return list_proccesses

    def get_max_priorty(self, proccess):
        min1 = 100
        idx = 0
        for i in range(len(proccess)):
            if proccess[i].priorty < min1:
                min1 = proccess[i].priorty
                idx = i
        return proccess[idx]

    def finshed(self):
        for i in self.arr_t_sorted:
            if i.remain_t != 0:
                return False
        return True

    def priority_scheduleing(self, prememtive=False):

        self.arr_t_sorted.sort()
        last_res = None
        result = list()
        time = 0
        while not self.finshed():
            startTime = time
            proccesses = self.get_processes_toRun(time)
            if len(proccesses) == 0:
                time += 1
                continue
            toRun = self.get_max_priorty(proccesses)
            if prememtive:
                time += 1
                toRun.remain_t -= 1
            else:
                while (toRun.remain_t != 0):
                    time += 1
                    toRun.remain_t -= 1
            endTime = time
            if last_res == toRun.name:
                result[-1]["endTime"] = endTime
            else:
                result.append(
                    dict(Pname=toRun.name, startTime=startTime, endTime=endTime))
            last_res = toRun.name
        return result

    def get_proccess(self, name):
        for i in self.processes:
            if name == i.name:
                return i
        return None

    def get_avarege_waiting_time(self, scheduled_result):
        waitingTime = 0
        for i in scheduled_result:
            proccess = self.get_proccess(i["Pname"])
            waitingTime += i["startTime"] - proccess.arr_t
            proccess.arr_t += (i["endTime"]-i["startTime"])
        for p in self.processes:
            p.arr_t -= p.burst_t
        return float(waitingTime)/len(self.processes)


# list_pro = []
# list_pro.append(Process("P1", 0, 10, 3))
# list_pro.append(Process("P2", 0, 1, 1))
# list_pro.append(Process("P3", 0, 2, 4))
# list_pro.append(Process("P4", 0, 1, 5))
# list_pro.append(Process("P5", 0, 5, 2))

# S = Scheduler(*list_pro)


# output = S.FCFS()
# print(output)
# print(S.get_avarege_waiting_time(output))


# output = S.priority_scheduleing(False)
# print(output)
# print(S.get_avarege_waiting_time(output))
