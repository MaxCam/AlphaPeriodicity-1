# url="https://atlas.ripe.net/api/v2/measurements/2055768/results?start=1493596800&stop=1494201599&probe_ids=23099&format=json"
import urllib.request, json
import pymysql

idProbeAnchorToIdsM=dict()
traceroute=""
conta=0

with urllib.request.urlopen("http://localhost:8000/test.json") as url:
    data = json.loads(url.read().decode())
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
                       user="root",  # your username
                       passwd="root",  # your password
                       db="instability")  # name of the data base
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

        try:
            cur.execute("INSERT INTO idProbeAnchorToPaths (id_probeAnchor,id,probeId,idMeas,reachingTarget,destinationAddress,protocol,listTimestamp,traceroute,paris0 , paris1 , paris2 , paris3 , paris4 , paris5 , paris6 , paris7 , paris8 , paris9 , paris10 , paris11 , paris12 , paris13 , paris14 , paris15 ) VALUES ('" + key + "','" + str(
                    rec) + "','" + str(probeId).strip() + "','" + str(idMeas) + "','" + str(reachingTarget) + "','" + str(
                    destinationAddress) + "','" + str(ipNumberProtocol) + "','" + str(timeStampOfNew) + "','" + str(
                    traceroute) + "','" + str(p0) + "','" + str(p1) + "','" + str(p2) + "','" + str(p3) + "','" + str(
                    p4) + "','" + str(p5) + "','" + str(p6) + "','" + str(p7) + "','" + str(p8) + "','" + str(
                    p9) + "','" + str(p10) + "','" + str(p11) + "','" + str(p12) + "','" + str(p13) + "','" + str(
                    p14) + "','" + str(p15) + "');")
        except:
            pass
cur.close()
conn.close()

# CREATE TABLE  idProbeAnchorToPaths (     id_probeAnchor char(30) NOT NULL, id MEDIUMINT NOT NULL, probeId CHAR(40), idMeas CHAR(40),    reachingTarget CHAR(30) NOT NULL,     destinationAddress CHAR(40) NOT NULL,     protocol CHAR(5) NOT NULL,     listTimestamp MEDIUMTEXT NOT NULL, traceroute MEDIUMTEXT NOT NULL, paris0 MEDIUMINT, paris1 MEDIUMINT, paris2 MEDIUMINT, paris3 MEDIUMINT, paris4 MEDIUMINT, paris5 MEDIUMINT, paris6 MEDIUMINT, paris7 MEDIUMINT, paris8 MEDIUMINT, paris9 MEDIUMINT, paris10 MEDIUMINT, paris11 MEDIUMINT, paris12 MEDIUMINT, paris13 MEDIUMINT, paris14 MEDIUMINT, paris15 MEDIUMINT, isPeriodicByParis CHAR(40),  isPeriodicByNotParis CHAR(40), PRIMARY KEY (id_probeAnchor,id) ) ENGINE=MyISAM;
