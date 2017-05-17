import requests, json
import pymysql
from subprocess import call
import md5

def checkIfCached(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId):
    hash = md5.new("" + str(defaultStart) + str(defaultEnd) + str(defaultMeasurement) + str(defaultProbeId)).digest()
    # search in mysql if hash exists
    return False

def getPeriodicityFromCache(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId):
    # retrieve from mysql - table periodicity
    return False # Return false if not yet calculated


def cache(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId):
    hash = md5.new("" + str(defaultStart) + str(defaultEnd) + str(defaultMeasurement) + str(defaultProbeId)).digest()
    # store hash in mysql - table cache
    return True

def run(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId):
    periodicity = getPeriodicityFromCache(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId)
    if periodicity:
        return periodicity
    else:
        if not checkIfCached(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId):
            start_procedure(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId)
        return "We are calculating the periodicity, please refresh this page in a couple of minutes"


def start_procedure(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId):
    idProbeAnchorToIdsM=dict()
    traceroute=""
    conta=0
    url="https://atlas.ripe.net/api/v2/measurements/"+str(defaultMeasurement)+"/results?start="+str(defaultStart)+"&stop="+str(defaultEnd)+"&probe_ids="+str(defaultProbeId)+"&format=json"

    data = requests.get(url)
    #return str(data.text)
    if data:
        data = data.json()
        if True:  # TODO parisIDen
            conta = conta + 1
            if True:  # TODO measIdent
                lunghezzaRecord = len(data)

                for counterLine in range(0, lunghezzaRecord):

                    if True:  # TODO ErrorCheck
                        ipNumberProtocol = data[counterLine]["af"]
                        prbIdSource = data[counterLine]["prb_id"]
                        destinationAddress = data[counterLine]["dst_addr"]
                        idMeas = data[counterLine]["msm_id"]
                        parisId = int(data[counterLine]["paris_id"])
                        timeStampOfNew = str(data[counterLine]["timestamp"]) + ";;"

                        key = str(prbIdSource) + "-" + str(destinationAddress)
                        j = len(data[counterLine]["result"])
                        sourceAddress = data[counterLine]["src_addr"]

                        lungRes = len(data[counterLine]["result"])

                        reachingTarget = True

                        for counterIpTraceroute in range(0, j):
                            validatedField = False
                            while (validatedField is not True):
                                try:
                                    currentIp = data[counterLine]["result"][counterIpTraceroute]["result"][0]["from"]
                                    traceroute = traceroute + currentIp + ";;"
                                    validatedField = True
                                except:
                                    traceroute = traceroute + "*" + ";;"
                                    validatedField = True

                        if (key not in idProbeAnchorToIdsM.keys()):
                            idProbeAnchorToIdsM[key] = dict()
                            idProbeAnchorToIdsM[key][0] = dict()
                            idProbeAnchorToIdsM[key][0]["probeId"]=str(prbIdSource)
                            idProbeAnchorToIdsM[key][0]["idMeas"] = str(idMeas)
                            idProbeAnchorToIdsM[key][0]["reachingTarget"] = str(reachingTarget)
                            idProbeAnchorToIdsM[key][0]["destinationAddress"] = str(destinationAddress)
                            idProbeAnchorToIdsM[key][0]["ipNumberProtocol"] = str(ipNumberProtocol)
                            idProbeAnchorToIdsM[key][0]["timeStampOfNew"] = str(timeStampOfNew)
                            idProbeAnchorToIdsM[key][0]["traceroute"] = str(traceroute)
                            idProbeAnchorToIdsM[key][0]["paris_ids"] = dict()

                            for counter in range(0, 16):
                                idProbeAnchorToIdsM[key][0]["paris_ids"][counter] = 0

                            idProbeAnchorToIdsM[key][0]["paris_ids"][parisId] = 1

                        else:
                            matched = idProbeAnchorToIdsM[key]
                            presenti = len(matched)
                            TracealreadyPresent = False

                            for rec in matched:

                                if (str(idProbeAnchorToIdsM[key][rec]["traceroute"]).strip() == str(traceroute).strip()):
                                    TracealreadyPresent = True
                                    k = str(idProbeAnchorToIdsM[key][rec]["timeStampOfNew"]) + str(timeStampOfNew)
                                    break

                            if (TracealreadyPresent is True):
                                idProbeAnchorToIdsM[key][rec]["timeStampOfNew"] = str(k)
                                idProbeAnchorToIdsM[key][rec]["paris_ids"][parisId] += 1

                            if (TracealreadyPresent is False):
                                idProbeAnchorToIdsM[key][presenti] = dict()
                                idProbeAnchorToIdsM[key][presenti]["probeId"] = str(prbIdSource)
                                idProbeAnchorToIdsM[key][presenti]["idMeas"] = str(idMeas)
                                idProbeAnchorToIdsM[key][presenti]["reachingTarget"] = str(reachingTarget)
                                idProbeAnchorToIdsM[key][presenti]["destinationAddress"] = str(destinationAddress)
                                idProbeAnchorToIdsM[key][presenti]["ipNumberProtocol"] = str(ipNumberProtocol)
                                idProbeAnchorToIdsM[key][presenti]["timeStampOfNew"] = str(timeStampOfNew)
                                idProbeAnchorToIdsM[key][presenti]["traceroute"] = str(traceroute)

                                idProbeAnchorToIdsM[key][presenti]["paris_ids"] = dict()

                                for counter in range(0, 16):
                                    idProbeAnchorToIdsM[key][presenti]["paris_ids"][counter] = 0

                                idProbeAnchorToIdsM[key][presenti]["paris_ids"][parisId] = 1

                        traceroute = ""

                    else:
                        isAlreadyPresent = False
                        isMoreRecent = False

    conn = pymysql.connect(host="localhost",  # your host, usually localhost
                           user="periodicity",  # your username
                           passwd="GLzyFWpbt2yZbAPs",  # your password
                           db="periodicity")  # name of the data base
    conn.autocommit(True)
    cur = conn.cursor()


    for key in idProbeAnchorToIdsM.keys():
        matched = idProbeAnchorToIdsM[key]

        for rec in matched:
            probeId=idProbeAnchorToIdsM[key][rec]["probeId"]
            idMeas = idProbeAnchorToIdsM[key][rec]["idMeas"]
            reachingTarget = idProbeAnchorToIdsM[key][rec]["reachingTarget"]
            destinationAddress = idProbeAnchorToIdsM[key][rec]["destinationAddress"]
            ipNumberProtocol = idProbeAnchorToIdsM[key][rec]["ipNumberProtocol"]
            timeStampOfNew = idProbeAnchorToIdsM[key][rec]["timeStampOfNew"]
            traceroute = idProbeAnchorToIdsM[key][rec]["traceroute"]

            p0 = idProbeAnchorToIdsM[key][rec]["paris_ids"][0]
            p1 = idProbeAnchorToIdsM[key][rec]["paris_ids"][1]
            p2 = idProbeAnchorToIdsM[key][rec]["paris_ids"][2]
            p3 = idProbeAnchorToIdsM[key][rec]["paris_ids"][3]
            p4 = idProbeAnchorToIdsM[key][rec]["paris_ids"][4]
            p5 = idProbeAnchorToIdsM[key][rec]["paris_ids"][5]
            p6 = idProbeAnchorToIdsM[key][rec]["paris_ids"][6]
            p7 = idProbeAnchorToIdsM[key][rec]["paris_ids"][7]
            p8 = idProbeAnchorToIdsM[key][rec]["paris_ids"][8]
            p9 = idProbeAnchorToIdsM[key][rec]["paris_ids"][9]
            p10 = idProbeAnchorToIdsM[key][rec]["paris_ids"][10]
            p11 = idProbeAnchorToIdsM[key][rec]["paris_ids"][11]
            p12 = idProbeAnchorToIdsM[key][rec]["paris_ids"][12]
            p13 = idProbeAnchorToIdsM[key][rec]["paris_ids"][13]
            p14 = idProbeAnchorToIdsM[key][rec]["paris_ids"][14]
            p15 = idProbeAnchorToIdsM[key][rec]["paris_ids"][15]

            if True:#TODO gestire
                cur.execute("INSERT INTO idProbeAnchorToPaths (id_probeAnchor,id,idMeas,reachingTarget,destinationAddress,protocol,listTimestamp,traceroute,paris0 , paris1 , paris2 , paris3 , paris4 , paris5 , paris6 , paris7 , paris8 , paris9 , paris10 , paris11 , paris12 , paris13 , paris14 , paris15, probeId ) VALUES ('" + key + "','" + str(
                        rec) + "','"  + str(idMeas) + "','" + str(reachingTarget) + "','" + str(
                        destinationAddress) + "','" + str(ipNumberProtocol) + "','" + str(timeStampOfNew) + "','" + str(
                        traceroute) + "','" + str(p0) + "','" + str(p1) + "','" + str(p2) + "','" + str(p3) + "','" + str(
                        p4) + "','" + str(p5) + "','" + str(p6) + "','" + str(p7) + "','" + str(p8) + "','" + str(
                        p9) + "','" + str(p10) + "','" + str(p11) + "','" + str(p12) + "','" + str(p13) + "','" + str(
                        p14) + "','" + str(p15) + "','"+ str(probeId).strip() + "');")

    cache(defaultStart, defaultEnd, defaultMeasurement, defaultProbeId)
    cur.close()
    conn.close()

    #call(["nohup python PeriodicityCharacterizer.py &"])
    return "We are calculating the periodicity, please refresh this page in a couple of minutes"

