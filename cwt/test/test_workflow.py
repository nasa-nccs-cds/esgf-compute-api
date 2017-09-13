import cwt, os

# datainputs = """[domain=[{"name":"d0","lat":{"start":70,"end":90,"system":"values"},"lon":{"start":5,"end":45,"system":"values"}}],
# variable=[{"uri":"file:///dass/nobackup/tpmaxwel/.edas/cache/collections/NCML/MERRA_TAS1hr.ncml","name":"tas:v1","domain":"d0"}],
# operation=[{"name":"CDSpark.average","input":"v1","domain":"d0","axes":"xy"}]]"""

host = 'http://localhost:9000/wps/wps/cwt'
#host = 'https://dptomcat03-int/wps/cwt'

class TestWorkflow:

    def run( self ):
        domain_data = { 'id': 'd0', 'lat': {'start':70, 'end':90, 'crs':'values'}, 'lon': {'start':5, 'end':45, 'crs':'values'}, 'time': {'start':0, 'end':1000, 'crs':'indices'} }
        d0 = cwt.Domain.from_dict(domain_data)

#        inputs = cwt.Variable("file:///dass/nobackup/tpmaxwel/.edas/cache/collections/NCML/MERRA_TAS1hr.ncml", "tas", domain="d0" )
        inputs = cwt.Variable("collection://merra_TAS1hr", "tas", domain="d0" )

        op_data =  { 'name': "CDSpark.average", 'axes': "xy" }
        op =  cwt.Process.from_dict( op_data )
        op.set_inputs( inputs )

        wps = cwt.WPS( host, log=True, log_file=os.path.expanduser("~/esgf_api.log"), verify=False )

        wps.capabilities

        wps.execute( op, domain=d0, async=True )


executor = TestWorkflow()
executor.run()