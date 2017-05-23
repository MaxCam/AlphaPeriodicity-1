from nltk import ngrams
import operator
import pymysql
import textwrap
import re
import sys
import md5

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

cur.execute("select * from idProbeAnchorToPaths where probeId="+idProbe+" and idMeas="+idMeas+";")
#cur.execute("select * from tracerouteWithDifferentParisMEM where id_probeAnchor='23208-200.7.6.40'")#solo per test

queryOutput= cur.fetchall()
tracerouteToTimestamps=list()

for record in queryOutput:
    tracerouteToTimestamps.append(record[0])

lm=0

globalDistinctCharacterToCount=dict()

globalPatternLegthToCount=dict()
globalOscillationToCount=dict()
globalPeriodicityLengthToCount=dict()

idToCharacter=dict()
asciiCount=97 #lettere minuscole

for id_proAncora in tracerouteToTimestamps:
    patternToPeriodi=dict()
    periodicitaIndividuate=set()
    cur.execute("select * from idProbeAnchorToPaths where id_probeAnchor='"+str(id_proAncora)+"'")

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


            if(reachingTarget=="True"):
                 newTrace[listaTimestamp[counter]]= str(count), str(traceroute),str(reachingTarget)

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

    out_file = open("listaTraceroute.tsv", "w")

    co = 0
    t = "0"
    rt = "False"

    for traceroute in range(0, len(listaOrdinataDiChiaviTraceroute)):
        l = listaOrdinataDiChiaviTraceroute[traceroute]

        out_file.write(newTrace.get(l)[0]+",\n")
        out_file.write(newTrace.get(l)[0]+",\n")

        t = str(str(newTrace.get(l)[0]))

    out_file.close()

    periodicitaTrovata=False
    '''acf'''
    i=0
    tracerouteIdsList=[]


    #salvo tutti gli id  in una lista
    with open('listaTraceroute.tsv') as f:
        pass
        for line in f:
          if(i%2==0):
              tracerouteIdsList.append(line.strip())
          i+=1



    #associo ad ogni id un carattere
    for id in tracerouteIdsList:
        if id not in idToCharacter.keys():
            idToCharacter[id]=chr(asciiCount)
            if(asciiCount==122):
                asciiCount=64 #maiuscole

            else:
                asciiCount+=1

    charTracerouteSequence=[]

    #trasformo la sequenza di id in una sequenza di caratteri
    for id in tracerouteIdsList:
        charTracerouteSequence.append(idToCharacter[id])

    a1=charTracerouteSequence[:]
    a2=charTracerouteSequence[:]

    out_file=open("autocorrelationWithMatch.txt","w")
    out_file.write("x,y\n")
    for k in range(0,len(charTracerouteSequence)):
        sommaUguali=0
        for count in range(0,len(a1)):
            if(a1[count]==a2[count]):
                sommaUguali+=1

        out_file.write(str(k)+","+str(sommaUguali)+"\n")
        a1 = a1[1:]
        a2 = a2[:-1]

    out_file.close()

    listId=list()
    with open('autocorrelationWithMatch.txt') as f:
        pass
        for line in f:
          count=line.split(",")[1].strip()
          listId.append(count)


    out_file=open("sortedByX.txt","w")
    out_file.write("x\ty\n")

    for counter in range(4,len(listId)-4):
        if(listId[counter]>listId[counter+1] and listId[counter]>listId[counter-1]):
            if (listId[counter] > listId[counter + 2] and listId[counter] > listId[counter - 2]):
                if (listId[counter] > listId[counter + 3] and listId[counter] > listId[counter - 3]):
                    if(counter<(len(listId)-4)/2):
                        out_file.write(str(counter)+"\t"+str(int(listId[counter]))+"\n")
    out_file.close()


    i=0
    stringatrace=""

    '''trasforma l'elenco in una stringa per facilitare l'ngramm'''
    with open('listaTraceroute.tsv') as f:
        pass
        for line in f:
            if (i % 2 == 0):
             stringatrace=stringatrace+" "+line.strip()
            i+=1


    listId=list()
    di=dict()
    l=0

    '''esamina le x dei picchi per individuare le frequenze'''
    with open('sortedByX.txt') as f:
        for line in f:
            if l is not 0:
              count=line.split("\t")[0].strip()
              listId.append(count)
            l+=1


    for c in range(1,len(listId)):
        diff= (int(listId[c])-int(listId[c-1]))
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
                    if grams==prev:
                        if grams in diz:
                            diz[grams] += 1
                        else:
                            diz[grams] = 1
                    else:
                        prev=grams
            i+=1

        currentPeriodicitaTrovate=list()

        asciiCount = 97

        for m in diz:
            idsPresent=set()
            tuttoUguale=True
            if diz[m]>0:
                prev=m[0]
                for counter in range(0,len(m)):
                    idsPresent.add(m[counter])
                    if len(idsPresent)>1:#almeno 3
                        tuttoUguale=False
                        break
                if tuttoUguale is False:
                  stringa=""
                  for patternCharacter in m:
                      if(patternCharacter[:-1] not in idTochar.keys()):
                         # print("no")
                          idTochar[patternCharacter[:-1]]=chr(asciiCount)
                          if(asciiCount == 122):
                                asciiCount = 64
                          else:
                            asciiCount+=1
                      stringa+=str(idTochar[patternCharacter[:-1]])

                  periodicitaIndividuate.add(stringa)

                  osservazioneToStringa=""
                  periodicitaTrovata = True

    if(periodicitaTrovata is True):
            with open('listaTraceroute.tsv') as f:
                          pass
                          for line in f:
                              if (i % 2 == 0):
                                  if(line.strip()[:-1] in idTochar):
                                      osservazioneToStringa+=str(idTochar[line.strip()[:-1]])
                                  else:
                                      osservazioneToStringa+=("X")
                              i += 1

            for pattern in periodicitaIndividuate:
                max=0
                lunghezzaPattern=len(pattern)

                substring = textwrap.wrap(osservazioneToStringa, lunghezzaPattern)

                dizionario = dict()
                conta = 0
                somma = 2

                for it in range(0, len(substring)):

                    subsequence = substring[it]

                    if conta == 0:
                        prev = subsequence
                    else:
                        if hamdist(prev, subsequence) ==0:
                            somma += 1
                        else:
                            somma=1

                        prev = subsequence
                    conta += 1
                if(somma>max):
                    max=somma
                patternToPeriodi[pattern]=max

            for s in patternToPeriodi:
                patternLength=len(s)

                numberOscillation=patternToPeriodi[s]
                periodicityLength=int(patternLength)*int(numberOscillation)

                differentChar=set()
                for character in s:
                    differentChar.add(character)

                if(len(differentChar)>1):
                    if len(differentChar) in globalDistinctCharacterToCount.keys():
                        globalDistinctCharacterToCount[len(differentChar)]+=1
                    else:
                        globalDistinctCharacterToCount[len(differentChar)] = 1


                    if numberOscillation in globalOscillationToCount.keys():
                        globalOscillationToCount[numberOscillation]+=1                    
                    else:
                        globalOscillationToCount[numberOscillation]=1

                    if patternLength in globalPatternLegthToCount.keys():
                        globalPatternLegthToCount[patternLength]+=1
                    else:
                        globalPatternLegthToCount[patternLength] = 1

                    if periodicityLength in globalPeriodicityLengthToCount:
                        globalPeriodicityLengthToCount[periodicityLength]+=1
                    else:
                        globalPeriodicityLengthToCount[periodicityLength] = 1


    periodicita=0
    if periodicitaTrovata is True:
        periodicita+=1

if(periodicitaTrovata==True):
    store(idProbe, idMeas, {
        "idTochar": idTochar,
        #"idToTraceroute":globalIdToTraceroute,
        "periodicitaIndividuate": periodicitaIndividuate, #lista delle periodicita  in caratteri
     #   "gdbDiagramData":GDBdString #corrisponde al file gdbDiagramData.tsv ceh veniva letto in precedenza
    })

else:
    store(idProbe, idMeas, {
        "idTochar": "noPeriodicity",
        #"idToTraceroute":globalIdToTraceroute,
        "periodicitaIndividuate": "noPeriodicity", #lista delle periodicita  in caratteri
      #  "gdbDiagramData":GDBdString #corrisponde al file gdbDiagramData.tsv ceh veniva letto in precedenza
    })


#print(periodicita)
#print(globalPeriodicityLengthToCount)
#print(globalPatternLegthToCount)
#print(globalOscillationToCount)
#print(globalDistinctCharacterToCount)
#print(idTochar)
#print(periodicitaIndividuate)

# charToId=dict()
# for id in idTochar:
#     charToId[id]=idTochar[id]
#
# for periodicita in periodicitaIndividuate:
#     stringa=""
#     for carattere in periodicita:
#         stringa+=charToId[carattere]+"-"
#     print("**********")
#     print(stringa[:-1])
#     print(periodicita)

#store(idProbe, idMeas, {
#    "idTochar": idTochar,
#    "periodicitaIndividuate": periodicitaIndividuate
#})
