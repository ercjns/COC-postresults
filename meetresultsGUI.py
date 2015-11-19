from Tkinter import *
import ttk
import os
import re
import csv

import OutilsParse as Oparse
import OutilsOut as Oout



class Application(Frame):
    def process_results(self):

        path = "C:\\WIOL_SEASON_RESULTS_XML\\"
        p = re.compile('^WIOL(\d|c)\.xml$')
        events = [ f for f in os.listdir(path) if p.match(f) != None]
        
        # TODO: is this working? Feels like GUI is frozen? flush?
        self.status['text'] = 'Processing ' + str(len(events)) + ' results files.'
        
        urls = Oparse.getURLs('ResultURLs.csv')
        meetdata = {}
        
        for file in events:
            # TODO: use os module to split file names base vs extension
            infile = path + file
            outfileroot = path + file[:-4]
            runners, teams = self._processMeetResults(infile)
            
            meeturls = urls[file[:-4]]
            meeturls['indv_s'] = urls['season']['indv']
            meeturls['team_s'] = urls['season']['team']
            meeturls['full_s'] = urls['season']['ws']
            
            Oout.writeIndividualHTML(runners, meeturls, outfileroot+'-individualresults.html')
            Oout.writeIndividualHTML(runners, meeturls, outfileroot+'-WIOLIndividuals.html', {'WIOL':True})
            Oout.writeTeamHTML(teams, meeturls, outfileroot+'-teamresults.html')
            meetdata[file[:-4]] = {'indv': runners, 'teams': teams}
        
        seasonurls = {} # urls['season']  but keys are renamed.
        seasonurls['indv_s'] = urls['season']['indv']
        seasonurls['team_s'] = urls['season']['team']
        seasonurls['full_s'] = urls['season']['ws']
        
        Sindv, Steam = self._processSeasonResults(meetdata)
        
        Oout.writeSeasonIndivHTML(Sindv, seasonurls, path+'WIOLseason-INDV.html', {'WIOL':True})
        Oout.writeSeasonIndivHTML(Sindv, seasonurls, path+'WinterOseason.html', {'WIOL':False})
        Oout.writeSeasonTeamsHTML(Steam, seasonurls, path+'WIOLseason-TEAM.html')
        
        self.status['text'] = 'Done processing results'
        return

        
    def _processMeetResults(self, fn):
        runners = Oparse.getRunners(fn)
        cclasses = set([r.cclass for r in runners])
        for c in cclasses:
            incclass = [r for r in runners if r.cclass == c]
            Oparse.assignPositions(incclass)
            Oparse.assignScore(incclass, "COC")
            
        teams = Oparse.calcTeams(runners, "COC")
        Oparse.assignTeamPositions(teams, "COC")
        
        resultrunners = [r for r in runners if r.status != "DidNotStart"]
        return resultrunners, teams
        
    def _processSeasonResults(self, meetdata):
        Sindv, Steam = Oparse.createSeasonResults(meetdata)
        Sindv = Oparse.assignSeasonPositions(Sindv)
        Steam = Oparse.assignSeasonPositions(Steam)
        return Sindv, Steam

    def createWidgets(self):
        self.title = Label(self, text="Results Processor")
        self.title["font"] = {"size": 20, "weight": "bold"}
        self.title.grid(row=0, column=0, columnspan=2, sticky=W)
        
        self.inst1 = Label(self)
        self.inst1["text"] = "1. Save xml results to the 'C:\\WIOL_SEASON_RESULTS_XML' folder."
        
        self.inst2 = Label(self)
        self.inst2["text"] = "     * file names follow format 'WIOL#.xml'"
       
        self.inst3 = Label(self)
        self.inst3["text"] = "2. Click GO and html files will be generated in the same folder."
        
        self.inst1.grid(row=1, column=0, sticky=W, columnspan=2)
        self.inst2.grid(row=2, column=0, sticky=W, columnspan=2)
        self.inst3.grid(row=3, column=0, sticky=W, columnspan=2)
    
        self.status = Label(self)
        self.status['text'] = 'Nothing to report... ready'
        self.status.grid(row=4, column=0, columnspan=2)
        
        self.go = Button(self)
        self.go["text"] = "GO!"
        self.go["bg"] = "darkgreen"
        self.go["fg"] = "white"
        self.go["command"] = self.process_results

        self.go.grid(row=5, column=0)
    
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.grid(row=5, column=1)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

class MyConstants(Frame):
    def _importConstValues(self):
        consts = {}
        with open('ResultURLs.csv') as file:
            reader = list(csv.DictReader(file))
            for meet in reader:
                consts[meet['meet']] = meet
        return consts
    
    def _updateConstValues(self, fieldmap):
        for m, d in self.urls.items():
            fieldmap = fieldmap
            for k, v in d.items():
                if k in fieldmap.keys():
                    try:
                        newv = self.urls[m][fieldmap[k]].get()
                        self.urls[m][k] = newv
                    except:
                        continue
        return    
    
    def _saveConstValues(self):
        self.status['text'] = 'Working on it...'
        fieldmap = {'indv':'indv_e', 'team':'team_e', 'ws':'ws_e', 'rg':'rg_e'}
        fieldnames = list(fieldmap.keys())
        fieldnames.insert(0, 'meet')
        self._updateConstValues(fieldmap)
        with open('ResultURLs.csv', 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, restval='', extrasaction='ignore')
            writer.writeheader()
            for minfo in self.urls.values():
                writer.writerow(minfo)
        self.status['text'] = 'Changes saved. Generate pages on the main tab.'
        return
    
    def createWidgets(self):
        self.title = Label(self, text="Enter results, WinSplits, and RG URLs on each tab")
        self.title["font"] = {"size": 20, "weight": "bold"}
        self.title.grid(row=0, column=0, columnspan=2, sticky=W)
        
        meets = ['season', 'WIOL1', 'WIOL2', 'WIOL3', 'WIOL4', 'WIOL5', 'WIOL6', 'WIOL7', 'WIOLc']

        self.meetnb = ttk.Notebook(self)
        for m in meets:
            row = 0
            meetframe = Frame(self)

            if m == 'season':
                sURLlabel = Label(meetframe, text='Season Results Main')
                sURLlabel.grid(row=row, column=0)
                sURLentry = Entry(meetframe, width=80)
                sURLentry.delete(0, 'end')
                sURLentry.insert(0, self.urls[m]['ws'])
                sURLentry.grid(row=row, column=1)
                self.urls[m]['ws_e'] = sURLentry
            
            row += 1
            iURLlabel = Label(meetframe, text='Individual Results')
            iURLlabel.grid(row=row, column=0)
            iURLentry = Entry(meetframe, width=80)
            iURLentry.delete(0, 'end')
            iURLentry.insert(0, self.urls[m]['indv'])
            iURLentry.grid(row=row, column=1)
            self.urls[m]['indv_e'] = iURLentry
            row += 1
            tURLlabel = Label(meetframe, text='Team Results')
            tURLlabel.grid(row=row, column=0)
            tURLentry = Entry(meetframe, width=80)
            tURLentry.delete(0, 'end')
            tURLentry.insert(0, self.urls[m]['team'])
            tURLentry.grid(row=row, column=1)
            self.urls[m]['team_e'] = tURLentry
            
            if m != 'season':
                row += 1
                sURLlabel = Label(meetframe, text='WinSplits')
                sURLlabel.grid(row=row, column=0)
                sURLentry = Entry(meetframe, width=80)
                sURLentry.delete(0, 'end')
                sURLentry.insert(0, self.urls[m]['ws'])
                sURLentry.grid(row=row, column=1)
                self.urls[m]['ws_e'] = sURLentry
                row += 1
                rURLlabel = Label(meetframe, text='RouteGadget')
                rURLlabel.grid(row=row, column=0)
                rURLentry = Entry(meetframe, width=80)
                rURLentry.delete(0, 'end')
                rURLentry.insert(0, self.urls[m]['rg'])
                rURLentry.grid(row=row, column=1)
                self.urls[m]['rg_e'] = rURLentry
            
            meetframe.grid()
            self.meetnb.add(meetframe, text=m)
        
        self.meetnb.grid(row=1, column=0)
    
        self.status = Label(self)
        self.status['text'] = 'Edit urls, click save, then generate files via the main tab'
        self.status.grid(row=4, column=0, columnspan=2)
        
        self.save = Button(self)
        self.save['text'] = 'Save'
        self.save['fg'] = 'blue'
        self.save['command'] = self._saveConstValues

        self.save.grid(row=5, column=0)
    
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.urls = self._importConstValues()
        self.grid()
        self.createWidgets()
        
root = Tk()
nb = ttk.Notebook(root)
tab1 = Application(master=nb)
tab2 = MyConstants(master=nb)
nb.add(tab1, text='Main')
nb.add(tab2, text='Constants')
nb.grid()
nb.mainloop()
root.destroy()
