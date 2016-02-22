class IOFXMLreader(object):
    def getClassFromSoup(CR, iofV):
        if iofV == 2:
            try:
                cclass = CR.ClassShortName.string
            except:
                raise ValueError
        elif iofV == 3:
            try:
                cclass = CR.Class.ShortName.string
            except:
                raise ValueError
        else:
            raise ValueError
        return cclass
        
    def getCourseFromSoup(CR, iofV):
        if iofV == 2:
            course = None
        elif iofV == 3:
            try:
                course = CR.Course.Name.string
            except:
                raise ValueError
        else:
            raise ValueError
        return course

    def getNameFromSoup(PR, iofV):
        if iofV == 2:
            try:
                gn = PR.Person.PersonName.Given.string
            except:
                gn = None
            try:
                fn = PR.Person.PersonName.Family.string
            except:
                fn = None
        elif iofV == 3:
            try:
                gn = PR.Person.Name.Given.string
            except:
                gn = None
            try:
                fn = PR.Person.Name.Family.string
            except:
                fn = None
        else:
            raise ValueError

        if (gn != None) and (fn != None):
            name = gn + ' ' + fn
        elif (gn != None):
            name = gn
        elif (fn != None):
            name = fn
        else:
            name = None
        return name


    def getClubFromSoup(PR, iofV):
        if iofV == 2:
            try:
                club = PR.Person.CountryId.string
            except:
                club = None
        elif iofV == 3:
            try:
                club = PR.Organisation.ShortName.string
            except:
                club = None
        else:
            raise ValueError
        return club


    def getFinishFromSoup(PR, iofV):
        if iofV == 2:
            try:
                finish = PR.Result.FinishTime.string
            except:
                finish = None
        elif iofV == 3:
            try:
                finish = PR.Result.FinishTime.string
            except:
                finish = None
        else:
            raise ValueError
        return finish


    def getMMMSSFromSoup(PR, iofV):
        if iofV == 2:
            try:
                mmmss = PR.Result.Time.string
            except:
                mmmss = None
        else:
            raise ValueError
        return mmmss


    def getTimeFromSoup(PR, iofV):
        if iofV == 3:
            try:
                time = int(PR.Result.Time.string)
            except:
                time = None
        else:
            raise ValueError
        return time


    def getStartFromSoup(PR, iofV):
        if iofV == 2:
            try:
                start = PR.Result.StartTime.string
            except:
                start = None
        elif iofV == 3:
            try:
                start = PR.Result.StartTime.string
            except:
                start = None
        else:
            raise ValueError
        return start


    def getStatusFromSoup(PR, iofV):
        if iofV == 2:
            try:
                status = PR.Result.CompetitorStatus['value']
            except:
                raise NameError
        elif iofV == 3:
            try:
                status = PR.Result.Status.string
            except:
                raise NameError
        else:
            raise ValueError
        return status


    def getSIIDFromSoup(PR, iofV):
        if iofV == 2:
            estick = None
        elif iofV == 3:
            try:
                estick = PR.Result.ControlCard.string
            except:
                estick = None
        else:
            raise ValueError("Invalid iofVersion")
        return estick
        
    def getBibFromSoup(PR, iofV):
        if iofV == 2:
            bib = None
        elif iofV == 3:
            try:
                bib = PR.Result.BibNumber.string
            except:
                bib = None
        else:
            raise ValueError("Invalid iofVersion")
        return bib
    
    
def getRunners(file):
    """
    Import XML of runners and info into python structures.

    Input: file path to xml
    Return: List of Runner objects.
    Caller will need to handle any merging of runner objects as needed.
    """
    clubdict = OCC.ClubCodes('ClubCodes.csv')
    runners = []
    with open(file, 'r') as fn:
        soup = BS(fn, 'xml')
    
    v = soup.ResultList.find_all('IOFVersion')
    if len(v) > 0:
        iofV = 2
    else:
        iofV = 3

    cclasses = soup.ResultList.find_all('ClassResult')
    for c in cclasses:
        cclass = getClassFromSoup(c, iofV)
        course = getCourseFromSoup(c, iofV)
        for PR in c.find_all("PersonResult"):
            estick = getSIIDFromSoup(PR, iofV)
            start = getStartFromSoup(PR, iofV)
            club = getClubFromSoup(PR, iofV)
            bib = getBibFromSoup(PR, iofV) if cclass[0] == 'W' else None
            info = {"name": getNameFromSoup(PR, iofV),
                    "club": club,
                    "clubfull": clubdict.getClubFull(club),
                    "cclass": cclass,
                    "course": course, 
                    "bib": bib
                    }
            if iofV == 2:
                mmmss = getMMMSSFromSoup(PR, iofV)
                time = timeToInt(mmmss)
            elif iofV == 3:
                time = getTimeFromSoup(PR, iofV)
                mmmss = timeToMMMSS(time)
            result = {"finish": getFinishFromSoup(PR, iofV),
                      "mmmss": mmmss,
                      "time": time,
                      "status": getStatusFromSoup(PR, iofV),
                      }
            runners.append(Runner(estick, start, info, result))
    
    return runners
    
    
