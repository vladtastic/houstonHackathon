import re
import requests
import time
import smtplib
import time
from time import gmtime, strftime, localtime

username = 'airalliancehackaton'
password = 'h@ck4ch@nge'
fromaddr = 'airalliancehackaton@gmail.com'
toaddrs  = '0000000000@tmomail.net'


def recordExtractor(url):

        eventRecordRequest = requests.get(url)

        eventRecordResponse = eventRecordRequest.text

#       print(eventRecordResponse)

        records = parsePageResponseForRecordNumbers(eventRecordResponse)

        return records
#       return tuple(records,checkPageForNext(response))

def parsePageResponseForRecordNumbers(response):

        # Give a page response, get a list of record IDs on that page

        recordListOnPage = []

        regExPattern = r'target=+\d\d\d\d\d\d+'
        matches = re.findall(regExPattern,response)

        print 'Found',len(matches), 'records'

        for match in matches:
                recordListOnPage += extractRecordNumber(match)

        return recordListOnPage


def extractRecordNumber(recordMatch):

        # Given a potential record match, try and extract a Record ID Number

        recordIDPattern = r'\d\d\d\d\d\d'

        matches = re.findall(recordIDPattern,recordMatch)

        return matches


def checkPageForNext(response):

        # Given a page response, return the url to the next page if it exists

        nextPagePattern = r'Next'
        matches = re.findall(nextPagePattern, response)

        if len(matches) == 1:
                # Give me the url to the next page
                return True

        return False


def getIndividualRecordResponse(recordNumber):

        # Given a record number, (record number, RN number,zipcode)

#       print(recordNumber)

        baseURL = 'http://www11.tceq.texas.gov/oce/eer/index.cfm?fuseaction=main.getDetails&target='

        individualRecordURL = baseURL + recordNumber

        #print('Current URL:'+individualRecordURL)

        try:
                pageRecordRequest = requests.get(individualRecordURL)
                pageRecordResponse = pageRecordRequest.text

#               print(pageRecordResponse)

        except requests.ConnectionError:

                time.sleep(0.5)
                getIndividualRecordResponse(individualRecordURL)

        return recordNumber,extractCompanyName(pageRecordResponse),parseRecordResponseForRN(pageRecordResponse)

def parseRecordResponseForRN(response):

        # Given a response for an RN record, return the associated zip

        rnPattern = r'<td>RN\d\d\d\d\d\d\d\d\d</td>'

        rnMatch = re.findall(rnPattern, response)

        for match in rnMatch:

                rnID = re.findall(r'\d\d\d\d\d\d\d\d\d', match )

                for x in rnID:

                        return x,fetchZipCodeFromRN(x)


def fetchZipCodeFromRN(rnID):


#       print('\t',rnID.encode('ascii','ignore'))

        baseURL = 'http://www15.tceq.texas.gov/crpub/index.cfm?fuseaction=regent.validateRE&re_ref_num_txt=RN'

        individualRNURL = baseURL+rnID

        try:

                rnRecordRequest = requests.get(individualRNURL)
                rnRecordResponse = rnRecordRequest.text

        except requests.ConnectionError:
                time.sleep(0.5)
                fetchZipCodeFromRN(rnID)

        return parseRNResponseForZip(rnRecordResponse)


def parseRNResponseForZip(response):

        tagPattern = re.compile('<p+>.*?<label+>Near&nbsp;ZIP&nbsp;Code:</label+>.*?</p+>',re.IGNORECASE|re.DOTALL)

        tagMatch = re.findall(tagPattern, response)

        for tag in tagMatch:

                zipMatch = re.findall('[^0-9]\d\d\d\d\d[^0-9]',tag)

                for zip in zipMatch:
#                       print('\t\t',zip.encode('ascii','ignore'))
                        return zip

#       print(pageRecordResponse)

#       nextPageFlag, currentRecordList = recordExtractor(initialUrl)
#       masterRecordsList += currentRecordList



#       while(nextPageFlag):
#               nextPageFlag, currentRecordList = recordExtractor(initialUrl)
#               masterRecordsList += currentRecordList

#       for record in masterRecordsList:
#               print(record.encode('ascii','ignore'))


        # get initial response from search
        # parse page for records
        # check page for next
                # if next
                #  get new url
                #  get response from search

def extractCompanyName(response):

#       print('CompanyNameMatch')

#       print(response)

        companyNamePattern = re.compile('<th+.*?>.*?</th>\r\n\t\t\r\n\t\t<td>.*?</td>',re.IGNORECASE|re.DOTALL)

        companyNameMatch = re.findall(companyNamePattern, response)

#       First is RN entity

#       Later may be the pollutants

#       print(companyNameMatch[0])

        for company in companyNameMatch:

                entityMatches = re.findall('<td>.*?</td>', companyNameMatch[0])

                for entity in entityMatches:
                        return entity.encode('ascii','ignore').strip('<td>').strip('</')
                        #return entity

def findRelevantEntries(resultTupleList, targetZipCode):

        relevantRecordList = []

        for x in resultTupleList:


                recordZipCode = x[2][1]
                print(recordZipCode)

                if recordZipCode == targetZipCode:
                        relevantRecordList.append(x)
        print(len(relevantRecordList))
        return relevantRecordList


def test():

        initialURL = r'http://www11.tceq.texas.gov/oce/eer/index.cfm?fuseaction=main.dispatchSearch&principalid=&principalname=&startmonth=1&startday=10&startyear=2014&endmonth=&endday=&endyear=&doit=Submit'

        masterRecordList = []
        rnList = []
        resultsList = []

        nextPageFlag = False

        currentRecordList = recordExtractor(initialURL)

#       print('Current record list')
#       print(currentRecordList)

        for record in currentRecordList:

                temp = getIndividualRecordResponse(record)
                resultsList.append(temp)
                print 'Querying',len(resultsList), 'records (Total)'


                print('Found an event in your area!')
                print('Sending text message')
                sendText('http://www11.tceq.texas.gov/oce/eer/index.cfm?fuseaction=main.getDetails&target=214281')


#       targetZip=' 79741'

#       relevantResults = findRelevantEntries(resultsList,targetZip)

#       for relevantEntry in relevantResults:
#               print(relevantEntry)

#               print(temp)

#       for z in resultsList:
#               print(z)


def sendText(recordURL):

    username = 'airalliancehackaton'
    password = 'h@ck4ch@nge'
    fromaddr = 'airalliancehackaton@gmail.com'
    toaddrs  = '7138854350@tmomail.net'

    #print('Text message routine!')
    start_Time=get_Time()
    end_Time=get_Time()
    process='test'
    doneTextSend(start_Time,end_Time,recordURL)

def get_Time() :
    return time.time()

def show_Full_Time() :
    return strftime("%a, %d %b %Y %H:%M:%S", localtime())



def show_Time(start_Time, end_Time) :
    '''
    THERE IS AN ERROR in this formatting. If this section is important
    to you, correct it. It takes floating point numbers as its input.
    '''
    timeUsed = end_Time - start_Time
    hoursHold = int(timeUsed / 3600)
    minutesHold = int(timeUsed / 60 - int(hoursHold * 60))
    secondsHold = int(timeUsed - int(minutesHold*60))
    formatedTime = str(hoursHold) + ':' + str(minutesHold) + ':' + str(secondsHold)
    return formatedTime


def errorTextSend(errorName) :
    '''
    function takes in an error name (as a string), and sends
    a text message alerting the user of the error
    '''
    msg = ('\nERROR\nProcess: Errored Out\n' + str(errorName))

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def doneTextSend(start_Time, end_Time, process) :
    '''
    function takes the start and end time (both are floating points) of whatever
    your function is, and the function title (string).
    '''
    timeUsed = end_Time - start_Time
    hoursHold = int(timeUsed / 3600)
    minutesHold = int(timeUsed / 60 - int(hoursHold * 60))
    secondsHold = int(timeUsed - int(minutesHold*60))
    formatedTime = str(hoursHold) + ':' + str(minutesHold) + ':' + str(secondsHold)


    msg = ('\nALERT\nNotice:\n' + str(process))
#    msg = (str(process))


    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    print('Text message sent!')

if __name__ == '__main__':
        test()
