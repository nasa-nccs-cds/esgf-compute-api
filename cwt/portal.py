import json
import logging
import sys
import cdms2, genutil, cdutil, sys
import xml.etree.ElementTree as ET
from cwt import named_parameter
from cwt import process
from cwt.wps_lib import metadata
from cwt.wps_lib import operations
from pycdas.portal.cdas import *
import time, sys
logger = logging.getLogger()

class PortalError(Exception):
    pass

class PortalExeResponse(object):
    namespaces = {'owl': 'http://www.opengis.net/ows/1.1', "wps": "http://www.opengis.net/wps/1.0.0"}

    def __init__(self, responseStr ):
        self._element = ET.fromstring(responseStr)
        self._references = self._element.findall( "./wps:ProcessOutputs/wps:Output/wps:Reference", self.namespaces )

    def getReferenceValue(self, type, field ):
        for ref in self._references:
            if( ref.attrib.get('id', '') == type ):
                return ref.attrib.get(field, '')
        return ''

    def getFilePath( self ):
        return self.getReferenceValue( 'file', 'href' )

    def subaxis(self, axis, range ):
        return axis.subaxis( range[0], range[1] )

    def getVariable(self):
        filePath = result.getFilePath()
        print( "Plotting File at: " + filePath )
        cdmsfile = cdms2.open( filePath )
        vardata = cdmsfile( "Nd4jMaskedTensor" )
        # gridFile = cdms2.open( vardata.gridfile )
        # global_axes = [ gridFile.axes.get(dim) for dim in vardata.dimensions.split(',') ]
        # roiSpec = [ toks.split(',') for toks in vardata.roi.split('+') ]
        # roi = dict([ (spec[0],(int(spec[1]),int(spec[2]))) for spec in roiSpec ])
        # axes = [ self.subaxis( axis, roi.get(axis.axis)) for axis in global_axes ]
        # variable = cdms2.createVariable( vardata, vardata.dtype, True, False, None, vardata.missing, vardata.getGrid(), axes, vardata.attributes, vardata.name )
        # gridFile.close()
        cdmsfile.close()
        return vardata


class Portal(object):

    def __init__(self, host="localhost", request_port=4356, response_port=4357, **kwargs):
        self.__capabilities = None
        self.resultType = kwargs.get( "resultType" , "xml" )
        self.portal = CDASPortal(ConnectionMode.CONNECT, host, request_port, response_port)
        self.response_manager = self.portal.createResponseManager()

        if kwargs.get('log') is not None:
            formatter = logging.Formatter('[%(asctime)s][%(filename)s[%(funcName)s:%(lineno)d]] %(message)s')
            # TODO make level configurable
            logger.setLevel(logging.DEBUG)
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
            log_file = kwargs.get('log_file')
            if log_file is not None:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

    @property
    def capabilities(self):
        return self.__capabilities

    def __parse_response(self, response, response_type):
        data = None
        try:
            data = response_type.from_xml(response)
        except Exception:
            logger.exception('Failed to parse CDAS2 response.')
        else:
            return data

        if data is None:
            try:
                data = metadata.ExceptionReport.from_xml(response)
            except Exception:
                logger.exception('Failed to parse ExceptionReport')
                raise PortalError('Failed to parse server response')
            else:
                raise PortalError(data)

    def __get_capabilities(self):
        rId = self.portal.sendMessage("getCapabilities", ["WPS"])
        responses = self.response_manager.getResponses(rId)
        capabilities = [ self.__parse_response(response, operations.GetCapabilitiesResponse) for response in responses ]
        return capabilities

    def processes(self, refresh=False):
        if self.__capabilities is None or refresh: self.__capabilities = self.__get_capabilities()
        return [ process.Process(procSpec) for capResponse in self.__capabilities for procSpec in capResponse.process_offerings ]

    def get_process(self, identifier):
        if self.__capabilities is None:
            self.__capabilities = self.__get_capabilities()

        for process in self.processes():
            if ( process.identifier.strip() == identifier.strip() ):
                return process

        logger.debug('Failed to find process with identifier "%s"', identifier)
        return None

    def describe(self, process ):
        rId = self.portal.sendMessage("describeProcess", [ process.identifier ] )
        responses = self.response_manager.getResponses(rId)
        descriptions = [ self.__parse_response(response, operations.DescribeProcessResponse) for response in responses ]
        return descriptions[0]

    def __prepare_data_inputs(self, process, inputs, domains, **kwargs):
        variables = [x.parameterize() for x in inputs]
        domains = [x.parameterize() for x in domains]
        parameters = [named_parameter.NamedParameter(x, *y) for x, y in kwargs.iteritems()]
        process.inputs = inputs
        process.parameters = parameters
        operation = [process.parameterize()]
        return {'variable': variables, 'domain': domains, 'operation': operation}


    def execute( self, process, inputs=None, domains=None, **kwargs ):
        if inputs is None: inputs = []
        if domains is None: domains = []
        data_inputs = self.__prepare_data_inputs( process, inputs, domains, **kwargs )
        serialized_datainputs = '[{0}]'.format(';'.join('{0}={1}'.format(x, json.dumps(y)) for x, y in data_inputs.iteritems()))
        logger.info( "Sending Execute request: " + serialized_datainputs )
        return self.sendExeMsg( serialized_datainputs )


    def sendExeMsg( self, datainputs ):
        rId = self.portal.sendMessage( "execute", [ "CDSpark.workflow", datainputs, { "result": self.resultType } ] )
        responses = self.response_manager.getResponses(rId)
        for response in responses: print " ----------------- Response: ----------------- \n" + str(response)
        return [ PortalExeResponse(response) for response in responses ]




if __name__ == '__main__':
    from variable import Variable
    from cwt import Domain, Dimension, CRS
    import vcs, EzTemplate

    portal = Portal( resultType="file" )
    domain = Domain( [ Dimension( 'time', 0, 10, CRS('indices') ) ] )
    tas = Variable('collection:/giss_r1i1p1', 'tas', domains=domain )
    process = portal.get_process('CDSpark.max')
    results = portal.execute( process, [tas], [domain], axes="t" )
    M = EzTemplate.Multi( rows=len(results), columns=1 )
    for result in results:
        t = M.get(legend='local')
        var = result.getVariable()
        x = vcs.init()
        plot = x.createboxfill()
        x.plot(var, t, plot )
        x.interact()







