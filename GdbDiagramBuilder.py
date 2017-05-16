import sys
import webbrowser
import operator

import pymysql
import json


defaultProbeId="23208"
defaultMeasurement="2957509"


conn = pymysql.connect(host="localhost",
                       user="root",
                       passwd="root",
                       db="instability")
conn.autocommit(True)
cur = conn.cursor()

#########################GDB DIAGRAM BUILDER#################################
cur.execute("select * from idProbeAnchorToPaths where id_probeAnchor='23208-200.7.6.40'")

#cur.execute("select * from idProbeAnchorToPaths where probeId="+defaultProbeId+" and idMeas="+defaultMeasurement+";")
queryOutput= cur.fetchall()

tracerouteToTimestamps=dict()

for record in queryOutput:
    tracerouteValue=(str(record[7]))
    listTimestampValue=str(record[6])
    reachingTarget= str(record[3])

    tracerouteToTimestamps[tracerouteValue]= listTimestampValue, reachingTarget

newTrace=dict()

count=100

for traceroute in tracerouteToTimestamps:
    lineaFile = ""

    listaTimestamp= tracerouteToTimestamps.get(traceroute)[0]
    reachingTarget=tracerouteToTimestamps.get(traceroute)[1]

    listaTimestamp = listaTimestamp.split(';;')
    numbersOfTimestamps = len(listaTimestamp)

    contatore=0
    for counter in range(0, numbersOfTimestamps - 1):
        if(reachingTarget=="False"):
             newTrace[listaTimestamp[contatore]]= str(0-count), str(traceroute),str(reachingTarget)

        if(reachingTarget=="True"):
            newTrace[listaTimestamp[contatore]]= str(count), str(traceroute),str(reachingTarget)
        contatore+=1
    count=count+100

timeKeys=newTrace.keys()
listaOrdinataDiChiaviTraceroute= sorted(timeKeys)

prev=listaOrdinataDiChiaviTraceroute[0]

for contaOrdinato in range(1, len(listaOrdinataDiChiaviTraceroute)):
    next=listaOrdinataDiChiaviTraceroute[contaOrdinato]

    while(int(next)>(int(prev)+1300)):
        newTrace[str(int(prev)+900)]= str(0), str("NA") , str("False")
        prev=str(int(prev)+900)

    if(int(next)<(int(prev)+1500)):
        prev=next

timeKeys=newTrace.keys()
listaOrdinataDiChiaviTraceroute= sorted(timeKeys)


#Scrittura del file letto da gdbdiagram.js
out_file = open("gdbData.tsv", "w")

out_file.write("date\tclose\n")

progressiveCounter=0
lastTraceroute= "0"
rt="False"

for traceroute in range(0, len(listaOrdinataDiChiaviTraceroute)):
    timeKeys=listaOrdinataDiChiaviTraceroute[traceroute]
    progressiveCounter= progressiveCounter + 1
    out_file.write(str(progressiveCounter) + "\t" + str(lastTraceroute) + "\t" + newTrace.get(timeKeys)[1] + "\t" + str(timeKeys) + "\t" + str(newTrace.get(timeKeys)[2]) + "\n")
    lastTraceroute= ""

    out_file.write(str(progressiveCounter) + "\t" + newTrace.get(timeKeys)[0] + "\t" + newTrace.get(timeKeys)[1] + "\t" + str(timeKeys) + "\t" + str(newTrace.get(timeKeys)[2]) + "\n")
    lastTraceroute= str(str(newTrace.get(timeKeys)[0]))

out_file.write(str(progressiveCounter + 1) + "\t" + newTrace.get(timeKeys)[0] + "\t" + newTrace.get(timeKeys)[1] + "\n")
lastTraceroute= str(str(newTrace.get(timeKeys)[0])) + "\t" + newTrace.get(timeKeys)[1] + "\t" + str(timeKeys) + "\t" + str(newTrace.get(timeKeys)[2])

out_file.close()
#########################GDB DIAGRAM BUILDER#################################