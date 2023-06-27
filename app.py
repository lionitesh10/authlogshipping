import datetime
from flask import *

app=Flask(__name__)

# import authlogs
import authlogs2
import pandas as pd

x = datetime.datetime.now()
current_date=x.strftime("%Y-%m-%d")

class LogBase:

    def __init__(self,time,host,process,user,sourceIp,status):
        self.time=time
        self.host=host
        self.process=process
        self.user=user
        self.sourceIp=sourceIp
        self.status=status

class UserIp:
    def __init__(self,user,ip):
        self.user=user
        self.ip=ip

@app.route('/')
def index():
    currentDate=str(datetime.datetime.now())[0:10]+'.txt'
    try:
        universalLogin,failedLogins=authlogs2.getLogs(currentDate)
        successCount=getSuccessCount(universalLogin)
        nooffailedLogins=len(failedLogins)+len(universalLogin)-successCount
        userIPdata=pd.DataFrame(columns=['User','SourceIP'])

        userlists=[]
        sourceIpLists=[]

        for i in universalLogin:
            print(i.user)
            userlists.append(i.user)
            print(i.sourceIp)
            sourceIpLists.append(i.sourceIp)

        userIPdata['User']=userlists
        userIPdata['SourceIP']=sourceIpLists

        print(userIPdata)
        print(userIPdata['SourceIP'].value_counts())
        ips=userIPdata['SourceIP'].unique().tolist()

        

        return render_template("index.html",
                           acceptedLogins=universalLogin,
                           failedlogins=failedLogins,
                           noofSuccess=successCount,
                           noofFailure=nooffailedLogins,
                           total=len(universalLogin)+len(failedLogins),
                           current_date=current_date
                           )
    except:
        return render_template("error.html")

def getSuccessCount(logsList):
    suceessCount=0
    print(len(logsList))
    for i in logsList:
        print(i.status)
        if i.status=='Accepted':
            suceessCount=suceessCount+1

    return suceessCount

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')