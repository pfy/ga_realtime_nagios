#!/usr/bin/python
__author__ = "David Gunzinger"
__copyright__ = "Copyright 2013, Smooh GmbH"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "David Gunzinger"
__email__ = "david@smooh.ch"
__status__ = "Production"
                    

import argparse
import nagiosplugin

import httplib2
from oauth2client.file import Storage
from apiclient.discovery import build


# data acquisition
class RealtimeVisitors(nagiosplugin.Resource):


    def __init__(self, data, view):
        self.data = data
        self.view = view

    def probe(self):
        #       try:
            storage = Storage(self.data)
            credentials = storage.get()
            
            http = httplib2.Http()
            http = credentials.authorize(http)
            # Construct the service object for the interacting with the Google Analytics API.
            service = build('analytics', 'v3', http=http)
            request = service.data().realtime().get(ids="ga:%s"%(self.view),metrics="ga:activeVisitors")
            response = request.execute()
#            print response
            activeVisitors =  int(response["totalsForAllResults"]["ga:activeVisitors"])
#            print activeVisitors
            return [nagiosplugin.Metric("activeVisitors", activeVisitors, min=0,context='activeVisitors')]
            #        except:
#return [nagiosplugin.Metric("activeVisitors", None, context='activeVisitors')]



# runtime environment and data evaluation

@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument('-w', '--warning', metavar='RANGE', default='',
                      help='return warning if activeVisitors is outside RANGE')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='',
                      help='return critical if activeVisitors is outside RANGE')
    argp.add_argument('-D', '--data', action='store',required=True)
    argp.add_argument('-V', '--view', action='store',required=True)
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase output verbosity (use up to 3 times)')

    args = argp.parse_args()
    check = nagiosplugin.Check(
        RealtimeVisitors(args.data,args.view),
        nagiosplugin.ScalarContext('activeVisitors', args.warning, args.critical))
    check.main(verbose=args.verbose)

if __name__ == '__main__':
    main()
