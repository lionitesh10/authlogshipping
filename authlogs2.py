# CREATE NEW AMI for password recovery

import boto3
import datetime

x = datetime.datetime.now()
# current_date=str(x.strftime("%Y-%m-%d"))+'.txt'


class LogBase:

    def __init__(self,time,host,process,user,sourceIp,status):
        self.time=time
        self.host=host
        self.process=process
        self.user=user
        self.sourceIp=sourceIp
        self.status=status

class FailedLogs:

    def __init__(self,message):
        self.message=message


currentDate=str(datetime.datetime.now())[0:10]+'.txt'

def getLogs(filekey):
    s3 = boto3.client('s3')

    response = s3.get_object(Bucket='niteshserver-authlogs', Key=filekey)
    content = response['Body'].read().decode('utf-8')

    # print(content)

    linesplitLogs=content.split('\n')

    individualNewLinelogs=[]
    failedLogins=[]

    for logs in linesplitLogs:
        # print(len(logs))
        if len(logs)>103:
            failedLogins.append(FailedLogs(logs))
        else:
            individualNewLinelogs.append(logs.split(' '))

    individualNewLinelogs=individualNewLinelogs[0:len(individualNewLinelogs)-1]

    logbaselists=[]
    for words_list in individualNewLinelogs:
        time=" "
        time=time.join(words_list[0:3])
        host=words_list[3]
        process=words_list[4]
        status=words_list[5]
        user=words_list[8]
        sourceIp=words_list[10]
        logbaselists.append(LogBase(time=time,host=host,process=process,user=user,sourceIp=sourceIp,status=status))

    return logbaselists,failedLogins
    
# logsList,failedLogslist=getLogs(currentDate)

# logsList,failedLogslist=getLogs(currentDate)

# for i in logsList:
#     print(i.host,i.process,i.status,i.user,i.sourceIp)

# for i in failedLogslist:
#     print(i.message)