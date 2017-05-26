from nltk import ngrams
import operator
import pymysql
import textwrap
import re
import sys
import math
import md5

def numberDistinctPath(prev):
    ids=set()
    for id in prev:
      #  print(id)
        ids.add(id)

    return len(ids)

def isAPeak(lag, listACFValues):
    if listACFValues[lag]> listACFValues[lag-1] and listACFValues[lag]> listACFValues[lag+1]:
        if listACFValues[lag]> listACFValues[lag-2] and listACFValues[lag]> listACFValues[lag+2]:         
            if listACFValues[lag]> listACFValues[lag-3] and listACFValues[lag]> listACFValues[lag+3]:
                return True
    return False

def computeTollerance(lengthGram):
    if(lengthGram<3):
        return 0
    else:
        return 1
        
def store(idProbe, idMeas, data):
    hash = md5.new("" + str(idProbe) + str(idMeas)).digest()
    #persist data on mysql - table periodicity
    return cur.execute('INSERT INTO periodicity (hash, body) VALUES ("'+hash+'","' + str(data) + '")')  # we should use also time

def repetitions(s):
   r = re.compile(r"(.+?)\1+")
   for match in r.finditer(s):
       yield (match.group(1), len(match.group(0))/len(match.group(1)))


def hamdist(str1, str2):

    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def cyclic_equiv(u, v):
    n, i, j = len(u), 0, 0
    if n != len(v):
        return False
    while i < n and j < n:
        k = 1
        while k <= n and u[(i + k) % n] == v[(j + k) % n]:
            k += 1
        if k > n:
            return True
        if u[(i + k) % n] > v[(j + k) % n]:
            i += k
        else:
            j += k
    return False

idProbe = sys.argv[1]
idMeas = sys.argv[2]

conn = pymysql.connect(host="localhost",  # your host, usually localhost
                       user="periodicity",  # your username
                       passwd="GLzyFWpbt2yZbAPs",  # your password
                       db="periodicity")  # name of the data base
conn.autocommit(True)

cur = conn.cursor()

cur.execute("select distinct id_probeAnchor from idProbeAnchorToPaths where probeId="+idProbe+" and idMeas="+idMeas+";")
#cur.execute("select distinct id_probeAnchor from mydef2 where id_probeAnchor='10124-193.170.114.242'")#solo per test

queryOutput= cur.fetchall()
tracerouteToTimestamps=list()
periodicitaTrovata=False
for record in queryOutput:
    tracerouteToTimestamps.append(record[0])

lm=0

globalDistinctCharacterToCount=dict()

globalPatternLegthToCount=dict()
globalOscillationToCount=dict()
globalPeriodicityLengthToCount=dict()
globalIdToTraceroute=dict()

globalCharacterToID=dict()

idToCharacter=dict()


periodicityToStartAndStop=dict()

for id_proAncora in tracerouteToTimestamps:
    try:
        patternToPeriodi=dict()
        periodicitaIndividuate=set()
        cur.execute("select * from idProbeAnchorToPaths where id_probeAnchor='"+str(id_proAncora)+"'")#TODO da ricambiare in idProbeAnchorToPaths

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

            for counter in range(0, numbersOfTimestamps - 1):
                if(reachingTarget=="False"):
                     newTrace[listaTimestamp[counter]]= str(0-count), str(traceroute),str(reachingTarget)
                     globalIdToTraceroute[str(0-count)]=str(traceroute)


                if(reachingTarget=="True"):
                     newTrace[listaTimestamp[counter]]= str(count), str(traceroute),str(reachingTarget)
                     globalIdToTraceroute[str(count)]=str(traceroute)

            count=count+100

        l=newTrace.keys()
        listaOrdinataDiChiaviTraceroute= sorted(l)

        prev=listaOrdinataDiChiaviTraceroute[0]


        for contaOrdinato in range(1, len(listaOrdinataDiChiaviTraceroute)):
            next=listaOrdinataDiChiaviTraceroute[contaOrdinato]

            while(int(next)>(int(prev)+1300)):
                newTrace[str(int(prev)+900)]= str(0), str("NA") , str("False")
                prev=str(int(prev)+900)

            if(int(next)<(int(prev)+1500)):
                prev=next


        l=newTrace.keys()
        listaOrdinataDiChiaviTraceroute= sorted(l)

        GDBdString=""
        GDBdString+=("date\tclose\n")
       
        out_file=open("gdbData.tsv","w")
        out_file.write("date\tclose\n")

        co=0
        t="0"
        rt="False"


        for traceroute in range(0, len(listaOrdinataDiChiaviTraceroute)):
            l=listaOrdinataDiChiaviTraceroute[traceroute]
            co=co+1
            GDBdString+=(str(co)+"\t"+str(t)+"\t"+newTrace.get(l)[1]+"\t"+str(l)  +"\t"+ str(newTrace.get(l)[2]+"\n" ))
            out_file.write(str(co)+"\t"+str(t)+"\t"+newTrace.get(l)[1]+"\t"+str(l)  +"\t"+ str(newTrace.get(l)[2]+"\n" ))
            t=""

            GDBdString+=(str(co)+"\t"+newTrace.get(l)[0]+"\t"+newTrace.get(l)[1]+"\t"+str(l) + "\t"+ str(newTrace.get(l)[2]+"\n"))
            out_file.write(str(co)+"\t"+newTrace.get(l)[0]+"\t"+newTrace.get(l)[1]+"\t"+str(l) + "\t"+ str(newTrace.get(l)[2]+"\n"))
            
            t= str(str(newTrace.get(l)[0]))


        GDBdString+=(str(co+1)+"\t"+newTrace.get(l)[0]+"\t"+newTrace.get(l)[1]+"\n")
        t= str(str(newTrace.get(l)[0]))   +"\t"+newTrace.get(l)[1]+"\t"+str(l) + "\t"+ str(newTrace.get(l)[2])

        out_file.close()

        listaIDTraceroute=list()

        for traceroute in range(0, len(listaOrdinataDiChiaviTraceroute)): #qui veniva generato il traceroute.tsv
            l = listaOrdinataDiChiaviTraceroute[traceroute]

          #  listaIDTraceroute.append(newTrace.get(l)[0].strip())
            listaIDTraceroute.append(newTrace.get(l)[0].strip())

            t = str(str(newTrace.get(l)[0]))

        periodicitaTrovata=False


        '''acf'''
        i=0
        tracerouteIDUnique=set()

        for tracerrouteId in listaIDTraceroute:
            tracerouteIDUnique.add(tracerrouteId)

        charTracerouteSequence=list()

        lagToScore=dict()

        #trasformo la sequenza di id in una sequenza di caratteri
        for id in listaIDTraceroute:
      #      charTracerouteSequence.append(idToCharacter[id])
         charTracerouteSequence.append(id)


        a1=charTracerouteSequence[:]
        a2=charTracerouteSequence[:]

        for k in range(0,len(charTracerouteSequence)):
            sommaUguali=0
            for count in range(0,len(a1)):
                if(a1[count]==a2[count]):
                    sommaUguali+=1

            lagToScore[k]=sommaUguali
            
            a1 = a1[1:]
            a2 = a2[:-1]


        ACFValuesList=list()
        lagToValuesOfPeaks=dict()

        for lag in lagToScore:
            ACFValuesList.append(lagToScore[lag])

        #indiviidua i picchi
        for counter in range (3,len(ACFValuesList)):
            if isAPeak(counter,ACFValuesList):
                lagToValuesOfPeaks[counter]=ACFValuesList[counter]


        i=0
        stringatrace=""

        '''trasforma l'elenco in una stringa per facilitare l'ngramm'''

        for id in listaIDTraceroute:
            stringatrace+=" "+id.strip()

        estimatedPeriods=list()
        di=dict()
        l=0

        for peakLag in lagToValuesOfPeaks:
            estimatedPeriods.append(peakLag)

        for c in range(1,len(estimatedPeriods)):
            diff= (int(estimatedPeriods[c])-int(estimatedPeriods[c-1]))
            if diff in di:
                di[diff]+=1
            else:
                di[diff]=1


        sorted_ByY=sorted(lagToValuesOfPeaks.items(),key=operator.itemgetter(1))
        sortedByYList=list()

        for c in sorted_ByY:
            sortedByYList.append(c)

        for c in range(1,len(sortedByYList)):
            diff= abs((int(sortedByYList[c][0])-int(sortedByYList[c-1][0])))
            if diff in di:
                di[diff]+=1
            else:
                di[diff]=1

        idTochar = dict()



        for m in di.keys():


            sentence = stringatrace
            n = int(m)
            sixgrams = ngrams(sentence.split(), n)

            diz=dict()
            i=0

            for grams in sixgrams:
                if i==0:
                    prev=grams
                else:
                    if(i%n==0):
                        if hamdist(grams,prev)<computeTollerance(len(grams)):
                            if grams in diz:
                                diz[grams] += 1
                                prev=grams
                            else:
                                diz[grams] = 1
                                prev=grams

                        else:
                            prev=grams
                i+=1

            currentPeriodicitaTrovate=list()


            for patternFound in diz:

                idsPresent=set()
                tuttoUguale=True
                if diz[patternFound]>0: #inutile, rifattorizzare
                    prev=patternFound[0]

                    for counter in range(0,len(patternFound)):

                        idsPresent.add(patternFound[counter])
                        if len(idsPresent)>1:#almeno 3
                            tuttoUguale=False
                            break   #ce ne sono almeno 2 !!!!!!!!

                    if tuttoUguale is False:
                      stringaPeriodicita=""

                      for id in patternFound:
                        stringaPeriodicita+=id+" "
                      stringaPeriodicita=stringaPeriodicita.strip()
                      periodicitaIndividuate.add(stringaPeriodicita)

                      osservazioneToStringa=stringatrace
                      periodicitaTrovata = True


        if(periodicitaTrovata is True):
                for pattern in periodicitaIndividuate:
                    max=0
                    lunghezzaPattern=len(pattern)
                    

                    numeroSpaziBianchi=1
                    for carattere in pattern:
                        if carattere==" ":
                            numeroSpaziBianchi+=1


                    sentence = osservazioneToStringa
                    n = numeroSpaziBianchi
                    ngramsFound = ngrams(listaIDTraceroute, n)

                    i=0
                    periodicitaIncorso=False
                    for grams in ngramsFound:
                        if(i==0):
                            prev=grams
                            i+=1
                        else:
                            if(i%n==0):
                                if(hamdist(prev,grams)<computeTollerance(len(prev))):
                                    if(periodicitaIncorso==False):
                                        periodicitaIncorso=True
                                        inizio=i-len(prev)
                                else:
                                    if(periodicitaIncorso==True):
                                        periodicitaIncorso=False
                                        if(numberDistinctPath(prev)>1):
                                            periodicityToStartAndStop[str(prev)+"-"+str(inizio)]=[inizio,i]

                                prev=grams
                            i+=1

        periodicita=0
        if periodicitaTrovata is True:
            periodicita+=1

    except:
        pass

    if(periodicitaTrovata==True):
        store("idProbe", "idMeas", {
            "idToTraceroute":globalIdToTraceroute,
            "periodicitaIndividuate": periodicitaIndividuate, #lista delle periodicita  in caratteri
         #   "gdbDiagramData":GDBdString #corrisponde al file gdbDiagramData.tsv ceh veniva letto in precedenza
        })
     #   print(globalIdToTraceroute)
    else:
        store("idProbe", "idMeas", {
            "idToTraceroute":globalIdToTraceroute,
            "periodicitaIndividuate": "noPeriodicity", #lista delle periodicita  in caratteri
          #  "gdbDiagramData":GDBdString #corrisponde al file gdbDiagramData.tsv ceh veniva letto in precedenza
        })

#print(periodicityToStartAndStop)

#print(GDBdString)
