import numpy as np
import pandas as pd
import math as mt
import datetime as dt

def workloadScoringByStatuses(Data,NumOfAllDays,NumOfIntervalDays):
    list_assignee_id = np.unique(Data.assignee_id)
    #assignee_id = assignee_id[0]
    statuses = np.unique(Data.status)
    assignee_id_list = []
    status_list = []
    avg_num_of_task_per_week_list = []
    ste_list = []
    num_tasks_per_current_week_list = []
    score_for_status_list = []
        
    for ass_id in list_assignee_id:
        #splitting by status
        
        for status in statuses:
            dataframe_status = Data[(Data.status == str(status)) & (Data.assignee_id == ass_id)][:]
        
            #time borders params
            curr_date = dt.datetime.strptime(str('2017-04-01'),'%Y-%m-%d')
            curr_date = curr_date.date()
            delta = dt.timedelta(days=NumOfAllDays)
            first_date = curr_date-delta
        
            #time interval params
            delta_interval = dt.timedelta(days=NumOfIntervalDays)
            first_interval = first_date+delta_interval
                
            num_of_intervals = int(NumOfAllDays/NumOfIntervalDays)
            num_tasks_per_week = []
            for i in range(0,num_of_intervals):
                interval = dataframe_status[(dataframe_status.updated >= str(first_date)) & (dataframe_status.updated <= str(first_interval))][:]
                first_date = first_date + delta_interval
                first_interval = first_interval + delta_interval
        
                if i != (num_of_intervals-1):        
                    num_of_tasks = len(np.unique(interval['id']))
                    num_tasks_per_week.append(num_of_tasks) #history number of tasks
                else:
                    num_tasks_per_current_week = len(np.unique(interval['id'])) #currently number of tasks
            
            avg_num_of_task_per_week = round(np.mean(num_tasks_per_week),2)
            #avg_num_of_task_per_week = round(np.median(num_tasks_per_week),2)
    
            #squared deviations
            x_values = []
            for num in num_tasks_per_week:
                x = round((num - avg_num_of_task_per_week)**2,2)
                x_values.append(x)
    
            #data sampling statistics
            x_sum = round(sum(x_values),2) #sum of squared deviations
            dispersion = round(x_sum/(num_of_intervals-1),2) #dispersion
            std = round(mt.sqrt(dispersion),2) #standart deviation for sample
            ste = round(std/mt.sqrt(num_of_intervals),2) #standart error for sample
    
            #confidence interval
            left_border = int(avg_num_of_task_per_week - ste)
            right_border = int(avg_num_of_task_per_week + ste)
    
            #workload scoring for status
            score_for_status = workloadScoreStatuses(left_border,right_border,num_tasks_per_current_week)        
            assignee_id_list.append(ass_id)
            status_list.append(status)
            avg_num_of_task_per_week_list.append(avg_num_of_task_per_week)
            ste_list.append(ste)
            num_tasks_per_current_week_list.append(num_tasks_per_current_week)
            score_for_status_list.append(score_for_status)
        
    score_data = {"assignee_id":assignee_id_list,
                  "status":status_list,
                  "count_last_period":num_tasks_per_current_week_list,
                  "count_mean_calc_period":avg_num_of_task_per_week_list,
                  "count_sem_calc_period":ste_list,
                  "score_value":score_for_status_list}
    scores = pd.DataFrame(data=score_data)

    return scores


def workloadScoringByStatusesAndChannels(Data,NumOfAllDays,NumOfIntervalDays):
    list_assignee_id = np.unique(Data.assignee_id)
    statuses = np.unique(Data.status)
    assignee_id_list = []
    status_list = []
    channel_list = []
    avg_num_of_task_per_week_list = []
    ste_list = []
    num_tasks_per_current_week_list = []
    score_for_status_list = []
    #splitting by assignee_id    
    for ass_id in list_assignee_id:
        channels = np.unique(Data.channel)
        #splitting by channels
        for channel in channels:
            #splitting by status
            for status in statuses:
                dataframe_status = Data[(Data.status == str(status)) & (Data.assignee_id == ass_id) & (Data.channel == channel)][:]

                #time borders params
                curr_date = dt.datetime.strptime(str('2017-04-01'),'%Y-%m-%d')
                curr_date = curr_date.date()
                delta = dt.timedelta(days=NumOfAllDays)
                first_date = curr_date-delta

                #time interval params
                delta_interval = dt.timedelta(days=NumOfIntervalDays)
                first_interval = first_date+delta_interval

                num_of_intervals = int(NumOfAllDays/NumOfIntervalDays)
                num_tasks_per_week = []
                for i in range(0,num_of_intervals):
                    interval = dataframe_status[(dataframe_status.updated >= str(first_date)) & (dataframe_status.updated <= str(first_interval))][:]
                    first_date = first_date + delta_interval
                    first_interval = first_interval + delta_interval

                    if i != (num_of_intervals-1):        
                        num_of_tasks = len(np.unique(interval['id']))
                        num_tasks_per_week.append(num_of_tasks) #history number of tasks
                    else:
                        num_tasks_per_current_week = len(np.unique(interval['id'])) #currently number of tasks

                avg_num_of_task_per_week = round(np.mean(num_tasks_per_week),2)
                #avg_num_of_task_per_week = round(np.median(num_tasks_per_week),2)

                #squared deviations
                x_values = []
                for num in num_tasks_per_week:
                    x = round((num - avg_num_of_task_per_week)**2,2)
                    x_values.append(x)

                #data sampling statistics
                x_sum = round(sum(x_values),2) #sum of squared deviations
                dispersion = round(x_sum/(num_of_intervals-1),2) #dispersion
                std = round(mt.sqrt(dispersion),2) #standart deviation for sample
                ste = round(std/mt.sqrt(num_of_intervals),2) #standart error for sample

                #confidence interval
                left_border = int(avg_num_of_task_per_week - ste)
                right_border = int(avg_num_of_task_per_week + ste)

                #workload scoring for status
                score_for_status = workloadScoreStatuses(left_border,right_border,num_tasks_per_current_week)        
                assignee_id_list.append(ass_id)
                status_list.append(status)
                avg_num_of_task_per_week_list.append(avg_num_of_task_per_week)
                ste_list.append(ste)
                num_tasks_per_current_week_list.append(num_tasks_per_current_week)
                score_for_status_list.append(score_for_status)
                channel_list.append(channel)
                
    score_data = {"assignee_id":assignee_id_list,
                  "status":status_list,
                  "count_last_period":num_tasks_per_current_week_list,
                  "count_mean_calc_period":avg_num_of_task_per_week_list,
                  "count_sem_calc_period":ste_list,
                  "score_value":score_for_status_list,
                  "channel": channel_list}
    scores = pd.DataFrame(data=score_data)

    return scores

def workloadScoreStatuses(LeftBoard,RightBoard,CurrentNumOfTasks):
    if (LeftBoard == 0) & (CurrentNumOfTasks == 0) & (RightBoard == 0):
        score = 0
    elif (CurrentNumOfTasks >= 0) & (CurrentNumOfTasks < LeftBoard):
        score = 0
    elif (CurrentNumOfTasks >= LeftBoard) & (CurrentNumOfTasks <= RightBoard):
        score = 1
    else:
        score = 2
    
    return score

def totalScoringByStatus(DataFrame):
    Data = DataFrame
    Data1 = DataFrame.groupby("assignee_id", as_index= False)[["score_value"]].mean()
    return pd.DataFrame(data=Data1)
