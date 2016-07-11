#!/usr/bin/env python

def dasQuery(queryString, entryTitle) :
    import das_client
    dasinfo = das_client.get_data('https://cmsweb.cern.ch', queryString, 0, 0, False)
    if dasinfo['status'] != 'ok' :
        raise Exception('DAS query failed.\nQuery: %s\nDAS Status returned: %s' % (queryString, dasinfo['status']))

    for entry in dasinfo['data'] :
        if len(entry[entryTitle]) > 0 :
            yield entry[entryTitle][0]

def files(dataset, run) :
    query = 'file dataset=%s run=%d' % (dataset, run)
    for entry in dasQuery(query, 'file') :
        lfn = entry['name'].encode('ascii','ignore')
        if len(lfn) > 0 :
            yield lfn

def runs(lumiJSONFile) :
    import json
    with open(lumiJSONFile) as f :
        jdict = json.load(f)
        for runstring in jdict.keys() :
            yield int(runstring)

jsonFile = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt'
dataset = '/ZeroBias/Run2015B-v1/RAW'

# Not sure when to use these, they appear to not have any events in golden json
#    '/ZeroBias1/Run2015B-v1/RAW',
#    '/ZeroBias2/Run2015B-v1/RAW',
#    '/ZeroBias3/Run2015B-v1/RAW',
#    '/ZeroBias4/Run2015B-v1/RAW',
#    '/ZeroBias5/Run2015B-v1/RAW',
#    '/ZeroBias6/Run2015B-v1/RAW',
#    '/ZeroBias7/Run2015B-v1/RAW',
#    '/ZeroBias8/Run2015B-v1/RAW'

for run in runs(jsonFile) :
    print "\n".join(list(files(dataset, run)))
