def _fileContents(filename):
    with open(filename, 'r') as fn:
        contents = fn.read()
    return contents
    
def _getTopContent(urls={}, opts={}):
    content = ''
    
    if opts['pagetype'] in ['WIOLi', 'WIOLt']:
        content += '<strong>Split Times:</strong>'
        if urls['ws'].startswith('http'):
            content += ' <a href="' + urls['ws'] + '">Click here for WinSplits</a>'
        else:
            content += ' Coming Soon'
        content += '<br />'
    
    if opts['pagetype'] in ['WIOLi', 'WIOLt']:
        content += '<strong>Routes:</strong>'
        if urls['rg'].startswith('http'):
            content += ' <a href="' + urls['rg'] + '">Click here for RouteGadget</a>'
            content += ' &bull; <a href="http://cascadeoc.org/sites/default/files/content/RouteGadget%20(Updated).pdf"> Route Gadget Tips</a>'
        else:
            content += ' Coming Soon'
        content += '<br />'    

    if opts['pagetype'] in ['WIOLi', 'WIOLt']:        
        content += '<strong>Season Standings:</strong>'
        if urls['indv_s'].startswith('http'):
            content += ' <a href="' + urls['indv_s'] + '">Individuals</a> | '
            content += ' <a href="' + urls['team_s'] + '">Teams</a>'
        else:
            content += ' Coming Soon'
        content += '<br />'
    
    if opts['pagetype'] in ['WIOLi', 'WIOLt', 'WIOLiSeason', 'WIOLtSeason']:
        if urls['full_s'].startswith('http'):
            content += '<p>Back to <a href="' + urls['full_s'] + '">2015-16 WIOL Results</a></p>'
    
    if opts['pagetype'] == 'WIOLi':
        if urls['team'] != None:
            content += '<p>Go to <a href="' + urls['team'] + '">Team Results for this meet</a></p>'
    elif opts['pagetype'] == 'WIOLt':
        if urls['indv'] != None:
            content += '<p>Go to <a href="' + urls['indv'] + '">Individual Results for this meet</a></p>'
    
    if opts['pagetype'] in ['WIOLiSeason', 'WIOLtSeason', 'WinterOiSeason']:
        content += '<h3>Events in the Series</h3>'
        content += '<strong>Winter O\' #1</strong> Magnuson Park - Nov 7 2015</br>'
        content += '<strong>Winter O\' #2</strong> North SeaTac Park - Nov 21 2015</br>'
        content += '<strong>Winter O\' #3</strong> St Edward State Park - Dec 5 2015</br>'
        content += '<strong>Winter O\' #4</strong> Bridle Trails State Park - Dec 19 2015</br>'
        content += '<strong>Winter O\' #5</strong> Putney Woods - Jan 9 2015</br>'
        content += '<strong>Winter O\' #6</strong> Camp River Ranch - Jan 23 2015</br>'
        content += '<strong>Winter O\' #7</strong> Fire Mountain Scout Reservation - Feb 6 2015</br>'

    
    if opts['pagetype'] in ['WIOLi', 'WIOLiSeason', 'WIOLt', 'WIOLtSeason']:
        content += '<p>Scoring questions? See the <a href="http://cascadeoc.org/sites/default/files/content/WIOL%20Rules%202015-2016.pdf">WIOL Rules</a></p>'
    
    if opts['pagetype'] in ['WinterOiSeason']:
        content += '<p>Scoring questions? See the <a href="http://cascadeoc.org/pages/welcome-winter-orienteering-series">Winter O\' Overview</a></p>'
    
    if opts['pagetype'] in ['WIOLi', 'WIOLiSeason', 'WIOLt', 'WIOLtSeason']:
        content += '<p>Jump To: <br /><table>'
    if opts['pagetype'] in ['WIOLi', 'WIOLiSeason']:
        content += '<tr><td class="noborder">Elementary School</td><td class="noborder"><a href="#W1F">Girls</a></td><td class="noborder" colspan="2"><a href="#W1M">Boys</a></td></tr>'
        content += '<tr><td class="noborder">Middle School</td><td class="noborder"><a href="#W2F">Girls</a></td><td class="noborder" colspan="2"><a href="#W2M">Boys</a></td></tr>'
        content += '<tr><td class="noborder">High School Jr. Varsity</td><td class="noborder"><a href="#W3F">Girls</a></td><td class="noborder"><a href="#W4M">Boys North</a></td><td class="noborder"><a href="#W5M">Boys South</a></td></tr>'
        content += '<tr><td class="noborder">High School Varsity</td><td class="noborder"><a href="#W6F">Girls</a></td><td class="noborder" colspan="2"><a href="#W6M">Boys</a></td></tr>'
    elif opts['pagetype'] in ['WIOLt', 'WIOLtSeason']:
        content += '<tr><td class="noborder"><a href="#W2">Middle School</a></td><td class="noborder"><a href="#W3F">JV Girls</a></td></tr>'
        content += '<tr><td class="noborder"><a href="#W4M">JV Boys North</a></td><td class="noborder"><a href="#W5M">JV Boys South</a></td></tr>'
        content += '<tr><td class="noborder"><a href="#W6F">Varsity Girls</a></td><td class="noborder"><a href="#W6M">Varsity Boys</a></td></tr>'
    content += '</table></p>\n'  
    
    return content

def writeIndividualHTML(runners, urls, filename="results-individuals.html", opts={'WIOL':False}):
    """Save HTML to filename than can be pasted into COC results website."""
    COCcclasses = ['1', '3', '7', '8F', '8M', '8G', 'W1F', 'W1M', 'W2F', 'W2M',
                   'W3F', 'W4M', 'W5M', 'W6F', 'W6M']
    if opts['WIOL']:
        COCcclasses = [c for c in COCcclasses if c[0] == 'W']
    
    COCclassnames = {
                    '1': 'Beginner',
                    '3': 'Intermediate',
                    '7': 'Short Advanced',
                    '8F': 'Long Advanced Women',
                    '8M': 'Long Advanced Men',
                    '8G': 'Long Advanced Groups',
                    'W1F': 'Elementary School Girls',
                    'W1M': 'Elementary School Boys',
                    'W2F': 'Middle School Girls',
                    'W2M': 'Middle School Boys',
                    'W3F': 'High School JV Girls',
                    'W4M': 'High School JV Boys North',
                    'W5M': 'High School JV Boys South',
                    'W6F': 'High School Varsity Girls',
                    'W6M': 'High School Varsity Boys'
                    }
    statusCodes = {'OK': 'OK',
                   'NotCompeting': 'NC',
                   'MissingPunch': 'MSP',
                   'DidNotFinish': 'DNF',
                   'Disqualified': 'DSQ'
                  }
                        
    with open(filename, 'w') as fn:
        # includes
        fn.write('<style>' + _fileContents('OutilsStyle.css') + '</style>\n')
        
        # header content
        if opts['WIOL']:
            fn.write(_getTopContent(urls, {'pagetype':'WIOLi'}))
            
        # TODO: add top content for full results (some of this is taken care of by
        # the existing install. Don't need everything.
        
        # results content
        for c in COCcclasses:
            points = False if c in ['1','3','7','8G'] else True
            school = True if c[0] == 'W' else False
            
            fn.write('<div class="classResults" id="' + c + '">\n')
            fn.write('<a name="' + c + '"></a>\n')
            fn.write('<h3>' + COCclassnames[c] + "</h3>\n")
            fn.write('<table class="fullwidth">\n')
            fn.write('<tr>\n')
            fn.write('<th>Place</th>\n')
            fn.write('<th>Name</th>\n')
            if school:
                fn.write('<th>School</th>\n')
            else:
                fn.write('<th>Club</th>\n')
            fn.write('<th>Result</th>\n')
            if points:
                fn.write('<th>Points</th>\n')
            fn.write('</tr>\n')

            for r in runners:
                if r.cclass == c:
                    if r.status == 'OK':
                        fn.write('<tr>\n')
                        fn.write('<td class="fixright thin">' + str(r.position) + '</td>\n')
                        fn.write('<td>' + r.name + '</td>\n')
                        fn.write('<td>' + r.clubfull + '</td>\n')
                        fn.write('<td class="fixright">' + r.mmmss + '</td>\n')
                        if points:
                            fn.write('<td class="fixright thin">' + str(r.score) + '</td>\n')
                        fn.write('</tr>\n')
                    elif r.status in ['NotCompeting', 'Disqualified']:
                        fn.write('<tr>\n')
                        fn.write('<td>' + '</td>\n') # blank place
                        fn.write('<td>' + r.name + '</td>\n')
                        fn.write('<td>' + r.clubfull + '</td>\n')
                        if r.status == 'NotCompeting':
                            fn.write('<td class="fixright">' + 'NC ' + r.mmmss + '</td>\n')
                        else:
                            fn.write('<td class="fixright">' + 'DQ ' + r.mmmss + '</td>\n')
                        if points:
                            fn.write('<td>' + '</td>\n') # blank score
                        fn.write('</tr>\n')
                    else:
                        statuscode = statusCodes.setdefault(r.status, r.status)
                        fn.write('<tr>\n')
                        fn.write('<td>' + '</td>\n') # blank place
                        fn.write('<td>' + r.name + '</td>\n')
                        fn.write('<td>' + r.clubfull + '</td>\n')
                        fn.write('<td class="fixright">' + statuscode + '</td>\n')
                        if points:
                            fn.write('<td class="fixright thin">' + str(r.score) + '</td>\n')
                        fn.write('</tr>\n')
                        
            fn.write('</table>\n\n')
    return


def writeTeamHTML(teams, urls, filename="results-teams.html"):
    WIOLcclasses = ['W2', 'W3F', 'W4M', 'W5M', 'W6F', 'W6M']
    WIOLteamclassnames = {'W2': 'Middle School Teams',
                          'W3F': 'High School JV Girls Teams',
                          'W4M': 'High School JV Boys North Teams',
                          'W5M': 'High School JV Boys South Teams',
                          'W6F': 'High School Varsity Girls Teams',
                          'W6M': 'High School Varsity Boys Teams'
                         }


    with open(filename, 'w') as fn:
        # includes
        fn.write('<style>' + _fileContents('OutilsStyle.css') + '</style>\n')
        fn.write('<script type="text/javascript">' + _fileContents('OutilsJs.js') + '</script>')
        
        # header content
        fn.write(_getTopContent(urls, {'pagetype':'WIOLt'}))

        # results content
        for c in WIOLcclasses:
            fn.write('<div class="classResults" id="' + c + '">\n')
            fn.write('<a name="' + c + '"></a>\n')
            fn.write('<h3>' + WIOLteamclassnames[c] + ' | ')
            fn.write('<button onclick="toggleTeamDetails(\''  + c + '\')">Toggle details</button>' + '</h3>\n')
            fn.write('<table class="fullwidth">\n')
            fn.write('<tr>\n')
            fn.write('<th>Place</th>\n<th>Points</th>\n<th>School / Name</th>\n<th>Finish %</th>\n')
            fn.write('</tr>\n')

            cteams = [t for t in teams if t.cclass == c]
            cteams.sort(key=lambda x: x.position)
            for t in cteams:
                fn.write('<tr>\n')
                fn.write('<td class="team fixright thin">' + str(t.position) + '</td>\n')
                fn.write('<td class="team fixright thin">' + str(t.score) + '</td>\n')
                fn.write('<td class="team">' + str(t.clubfull) + ' (' + t.club + ')</td>\n')
                completed = str(int(100*(float(len(t.finishers))/len(t.runners)))) + '%'
                completedcount = ' (' + str(len(t.finishers)) + ' of ' + str(len(t.runners)) + ')'
                fn.write('<td class="team">' + completed + completedcount + '</td>\n')
                fn.write('</tr>\n')
                for r in t.scorers:
                    fn.write('<tr class="tmember" style="display:none;">\n')
                    fn.write('<td class="noborder fixright thin">' + '</td>\n') # blank place
                    fn.write('<td class="member fixright vborder">' + str(r.score) + '</td>\n')
                    fn.write('<td class="member vborder">' + r.name + ' (' + t.club + ')</td>\n')
                    fn.write('<td class="member noborder">' + r.mmmss + '</td>\n')
                    fn.write('</tr>\n')
            fn.write('</table>\n\n')
            fn.write('</div>')
    
    return
    
def writeSeasonIndivHTML(seasonindvs, urls, filename='season-ind.html', opts={'WIOL':False}):
    # TODO: Options for handling Winter O in addition to WIOL
    COCclassnames = {
                '1': 'Beginner',
                '3': 'Intermediate',
                '7': 'Short Advanced',
                '8F': 'Long Advanced Women',
                '8M': 'Long Advanced Men',
                '8G': 'Long Advanced Groups',
                'W1F': 'Elementary School Girls',
                'W1M': 'Elementary School Boys',
                'W2F': 'Middle School Girls',
                'W2M': 'Middle School Boys',
                'W2':  'Middle School',
                'W3F': 'High School JV Girls',
                'W4M': 'High School JV Boys North',
                'W5M': 'High School JV Boys South',
                'W6F': 'High School Varsity Girls',
                'W6M': 'High School Varsity Boys'
                }
    with open(filename, 'w') as fn:
        # includes
        fn.write('<style>' + _fileContents('OutilsStyle.css') + '</style>\n')
        
        # header content
        if opts['WIOL']:
            fn.write(_getTopContent(urls, {'pagetype':'WIOLiSeason'}))
        else:
            fn.write(_getTopContent(urls, {'pagetype':'WinterOiSeason'}))
        
        # results content
        for cclass in sorted(seasonindvs.keys()):
            if opts['WIOL']:
                if cclass in ['8M', '8F']:
                    continue
            elif not opts['WIOL']:
                if cclass not in ['8M', '8F']:
                    continue
            fn.write('<div class="classResults" id="' + cclass + '">\n')
            fn.write('<a name="' + cclass + '"></a>\n')
            fn.write('<h3>' + COCclassnames[cclass] + '</h3>')
            fn.write('<table class="fullwidth">\n')
            fn.write('<tr>\n')
            fn.write('<th>Place</th><th>Name</th><th>#1</th><th>#2</th><th>#3</th><th>#4</th><th>#5</th><th>#6</th><th>#7</th><th>Season</th>')
            fn.write('</tr>\n')
            
            # TODO order by posoition rather than by points
            # TODO order runners by points
            
            for runner in seasonindvs[cclass]:
                fn.write('<tr>')
                fn.write('<td class="fixright xthin">' + str(runner.position) + '</td>')
                fn.write('<td>' + runner.name + ' (' + runner.club +')' + '</td>')
                for meet in ['WIOL1', 'WIOL2', 'WIOL3', 'WIOL4', 'WIOL5', 'WIOL6', 'WIOL7']:
                    try:
                        fn.write('<td class="fixright xthin">' + str(runner.scores[meet]) + '</td>')
                    except KeyError:
                        fn.write('<td class="fixright xthin"> -- </td>')
                fn.write('<td class="fixright thin">' + str(runner.score) + '</td>')
                fn.write('</tr>')
            fn.write('</table></div>')
                        
    return
    
def writeSeasonTeamsHTML(seasonteams, urls, filename='season-team.html'):
    WIOLteamclassnames = {'W2': 'Middle School Teams',
                          'W3F': 'High School JV Girls Teams',
                          'W4M': 'High School JV Boys North Teams',
                          'W5M': 'High School JV Boys South Teams',
                          'W6F': 'High School Varsity Girls Teams',
                          'W6M': 'High School Varsity Boys Teams'
                         }
                         
    
    with open(filename, 'w') as fn:
        # includes
        fn.write('<style>' + _fileContents('OutilsStyle.css') + '</style>\n')
        
        # header content
        fn.write(_getTopContent(urls, {'pagetype':'WIOLtSeason'}))
        
        # results content
        for cclass in sorted(seasonteams.keys()):
            fn.write('<div class="classResults" id="' + cclass + '">\n')
            fn.write('<a name="' + cclass + '"></a>\n')
            fn.write('<h3>' + WIOLteamclassnames[cclass] + '</h3>')
            fn.write('<table class="fullwidth">\n')
            fn.write('<tr>\n')
            fn.write('<th>Place</th><th>School</th><th>#1</th><th>#2</th><th>#3</th><th>#4</th><th>#5</th><th>#6</th><th>#7</th><th>Season</th>')
            fn.write('</tr>\n')
            
            # TODO order by place rather than by points
            # TODO order teams by points
            seasonteams[cclass].sort(key=lambda x: -x.score)
            
            for team in seasonteams[cclass]:
                fn.write('<tr>')
                fn.write('<td class="fixright xthin">' + str(team.position) + '</td>')
                fn.write('<td>' + team.clubfull + ' (' + team.club + ')' + '</td>')
                for meet in ['WIOL1', 'WIOL2', 'WIOL3', 'WIOL4', 'WIOL5', 'WIOL6', 'WIOL7']:
                    try:
                        fn.write('<td class="fixright xthin">' + str(team.scores[meet]) + '</td>')
                    except KeyError:
                        fn.write('<td class="fixright xthin"> -- </td>')
                fn.write('<td class="fixright thin">' + str(team.score) + '</td>')
                fn.write('</tr>')
            fn.write('</table></div>')
                        
    return