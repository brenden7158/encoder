import requests
import gzip
import os
import shutil
import xml.dom.minidom
import logging,coloredlogs

l = logging.getLogger(__name__)
coloredlogs.install()

import sys
sys.path.append("./py2lib")
sys.path.append("./Util")
sys.path.append("./records")
import bit
import MachineProductCfg as MPC
import LFRecord as LFR

locationIds = []
zipCodes = []
epaIds = []

for i in MPC.getPrimaryLocations():
    locationIds.append(LFR.getCoopId(i))
    zipCodes.append(LFR.getZip(i))
    epaIds.append(LFR.getEpaId(i))

apiKey = '21d8a80b3d6b444998a80b3d6b1449d3'

def getData(epaId, zipcode):
    url = f"https://api.weather.com/v1/location/{zipcode}:4:US/airquality.xml?language=en-US&apiKey={apiKey}"

    res = requests.get(url=url)

    data = res.text
    newData = data[57:-11]

    # Write to i2doc file
    i2Doc = f'<AirQuality id="000000000" locationKey="{epaId}" isWxScan="0">' + '' + newData + f'<clientKey>{epaId}</clientKey></AirQuality>' 

    f = open("./.temp/AirQuality.i2m", 'a')
    f.write(i2Doc)
    f.close()

def writeData():
    useData = False 
    workingEpaIds = []

    for i in epaIds:
        if i == None:
            l.debug(f"No EPA ID found for location -- Skipping.")
        else:
            l.debug(f"EPA ID found for location! Writing data for Air Quality.")
            workingEpaIds.append(i)
            useData = True


    # Check to see if we even have EPA ids, as some areas don't have air quality reports
    if (useData):
        try:
            l.info("Writing an AirQuality record.")
            header = '<Data type="AirQuality">'
            footer = "</Data>"

            with open("./.temp/AirQuality.i2m", 'w') as doc:
                doc.write(header)

            for (x, y) in zip(workingEpaIds, zipCodes):
                getData(x, y)

            with open("./.temp/AirQuality.i2m", 'a') as end:
                end.write(footer)

            dom = xml.dom.minidom.parse("./.temp/AirQuality.i2m")
            xmlPretty = dom.toprettyxml(indent = "  ")

            with open("./.temp/AirQuality.i2m", 'w') as g:
                g.write(xmlPretty[23:])
                g.close()

            files = []
            commands = []
            with open("./.temp/AirQuality.i2m", 'rb') as f_in:
                with gzip.open("./.temp/AirQuality.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            gZipFile = "./.temp/AirQuality.gz"

            files.append(gZipFile)
            comand = commands.append('<MSG><Exec workRequest="storeData(File={0},QGROUP=__AirQuality__,Feed=AirQuality)" /><GzipCompressedMsg fname="AirQuality" /></MSG>')
            numFiles = len(files)

            bit.sendFile(files, commands, numFiles, 0)

            os.remove("./.temp/AirQuality.i2m")
            os.remove("./.temp/AirQuality.gz")
        except Exception as e:
            l.error("DO NOT REPORT THE ERROR BELOW")
            l.error("Failed to write an AirQuality record.")
            os.remove('./.temp/AirQuality.i2m')
    else:
        l.info("Not writing an AirQuality record due to a lack of working EPA ids.")


    
