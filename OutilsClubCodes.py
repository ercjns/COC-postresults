# OutilsClubCodes.py

class ClubCodes(object):
    def __init__(self, file):
        with open(file, 'r') as fn:
            self.codes = {}
            for l in fn:
                club, clubfull = l.split(',')
                self.codes[club] = clubfull.strip()
    
    def getClubFull(self, clubshort):
        if clubshort == None:
            return 'None'
        return self.codes.setdefault(clubshort, clubshort + ' (not recognized)')
        
        
if __name__ == '__main__':
    mycodes = ClubCodes('ClubCodes.csv')
    print 'COC -> ', mycodes.getClubFull('COC')