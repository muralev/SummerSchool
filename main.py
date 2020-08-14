from google.oauth2 import service_account
import pandas_gbq 
import pandas as pd
from lib_main import workloadScoringByStatuses, workloadScoringByStatusesAndChannels, workloadScoreStatuses, totalScoringByStatus

#CREDENTIALS = 

def getFreshData(Credentials,ProjectId):
    bigquery_sql = " ".join(["SELECT id, DATE(CAST(created_at AS DATETIME)) AS created, DATE(CAST(updated_at AS DATETIME)) AS updated, status, channel, assignee_id",
                             "FROM `xsolla_summer_school.customer_support`",
                             "WHERE status IN ('closed','solved')",
                             "ORDER BY updated_at"])

    dataframe = pandas_gbq.read_gbq(bigquery_sql,project_id=ProjectId, credentials=Credentials, dialect="standard")

    return dataframe

def getFreshDataWithChannel(Credentials,ProjectId):
    bigquery_sql = " ".join(["SELECT id, DATE(CAST(created_at AS DATETIME)) AS created, DATE(CAST(updated_at AS DATETIME)) AS updated, status, channel, assignee_id",
                             "FROM `xsolla_summer_school.customer_support`",
                             "WHERE status IN ('closed','solved') and channel IN ('chat','help_widget','email','call', 'zendesk', 'other')",
                             "ORDER BY updated_at"])

    dataframe = pandas_gbq.read_gbq(bigquery_sql,project_id=ProjectId, credentials=Credentials, dialect="standard")

    return dataframe

def insertScoreResultData(InsertDataFrame,ProjectId,DatasetId,TableId):
    destination_table = f"{DatasetId}.{TableId}"
    
    res_df = pd.DataFrame()
    res_df['assignee_id'] = InsertDataFrame['assignee_id'].astype('int64')
    res_df['status'] = InsertDataFrame['status'].astype('str')
    res_df['count_last_period'] = InsertDataFrame['count_last_period'].astype('int64')
    res_df['count_mean_calc_period'] = InsertDataFrame['count_mean_calc_period'].astype('float')
    res_df['count_sem_calc_period'] = InsertDataFrame['count_sem_calc_period'].astype('float')
    res_df['score_value'] = InsertDataFrame['score_value'].astype('int')
    res_df['developer'] = 'Unknown'
    res_df['developer'] = res_df['developer'].astype('str')

    pandas_gbq.to_gbq(res_df, destination_table=destination_table, project_id=ProjectId, if_exists='append')
    
def insertTotalScoreResultData(InsertDataFrame,ProjectId,DatasetId,TableId):
    destination_table = f"{DatasetId}.{TableId}"
    
    res_df = pd.DataFrame()
    res_df['assignee_id'] = InsertDataFrame['assignee_id'].astype('int64')
    res_df['score_value'] = InsertDataFrame['score_value'].astype('float')
    res_df['developer'] = 'Unknown'
    res_df['developer'] = res_df['developer'].astype('str')

    pandas_gbq.to_gbq(res_df, destination_table=destination_table, project_id=ProjectId, if_exists='append')    
    
def insertChannelScoreResultData(InsertDataFrame,ProjectId,DatasetId,TableId):
    destination_table = f"{DatasetId}.{TableId}"
    
    res_df = pd.DataFrame()
    res_df['assignee_id'] = InsertDataFrame['assignee_id'].astype('int64')
    res_df['status'] = InsertDataFrame['status'].astype('str')
    res_df['count_last_period'] = InsertDataFrame['count_last_period'].astype('int64')
    res_df['count_mean_calc_period'] = InsertDataFrame['count_mean_calc_period'].astype('float')
    res_df['count_sem_calc_period'] = InsertDataFrame['count_sem_calc_period'].astype('float')
    res_df['score_value'] = InsertDataFrame['score_value'].astype('int')
    res_df['developer'] = 'Unknown'
    res_df['developer'] = res_df['developer'].astype('str')
    res_df['channel'] = InsertDataFrame['channel'].astype('str')

    pandas_gbq.to_gbq(res_df, destination_table=destination_table, project_id=ProjectId, if_exists='append')

print('Start downloading...')
DataFrameWithoutChannel = getFreshData(CREDENTIALS,'findcsystem')  
DataFrameWithChannel = getFreshDataWithChannel(CREDENTIALS,'findcsystem')
print('End downloading.')

ResultWithChannel = DataFrameWithChannel
ResultWithoutChannel = DataFrameWithoutChannel


ResultWithChannel.reset_index(inplace=True, drop=True)
ResultWithoutChannel.reset_index(inplace=True, drop=True)

print('workloadScoringByStatusesAndChannels')
ResultWithChannel = workloadScoringByStatusesAndChannels(ResultWithChannel,63,7)
print('workloadScoringByStatuses')
ResultWithoutChannel = workloadScoringByStatuses(ResultWithoutChannel,63,7)
print('totalScoringByStatus')
TotalResult = totalScoringByStatus(ResultWithoutChannel)
print('Start uploading...')
insertScoreResultData(ResultWithoutChannel,'findcsystem','xsolla_summer_school','score_result_status')
insertChannelScoreResultData(ResultWithChannel,'findcsystem','xsolla_summer_school','score_result_status_channel')
insertTotalScoreResultData(TotalResult,'findcsystem','xsolla_summer_school','score_result_total')
print('End uploading.')




