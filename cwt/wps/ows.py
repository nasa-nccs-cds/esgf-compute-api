from cwt.wps.raw.ows import *

MissingParameterValue = 'MissingParameterValue'
InvalidParameterValue = 'InvalidParameterValue'
NoApplicableCode = 'NoApplicableCode'
NotEnoughStorage = 'NotEnoughStorage'
ServerBusy = 'ServerBusy'
FileSizeExceeded = 'FileSizeExceeded'
StorageNotSupported = 'StorageNotSupported'
VersionNegotiationFailed = 'VersionNegotiationFailed'

def exception(text, code, locator=None):
    """ Exception

    Args:
        text: A str exception text.
        code: A str exception code, see ows module.
        locator: A str indicating where the error occurred.

    Returns:
        cwt.wps.raw.ows.Exception: Minimally filled instance.
    """
    ex = ExceptionType()

    ex.ExceptionText = [text]

    ex.exceptionCode = code

    if locator is not None:
        ex.locator = locator

    return ex

def exception_report(version, exceptions):
    """ ExceptionReport

    Args:
        version: A str version of which this conforms to.
        exceptions: A list of cwt.wps.raw.ows.Exception instances.

    Returns:
        cwt.wps.raw.ows.ExceptionReport: Minimally filled instance.
    """
    er = ExceptionReport()

    er.version = VersionType(version)

    er.Exception.extend(exceptions) 

    return er

def operation(name, get=None, post=None):
    """ Operation

    Either get or post needs to be set.

    Args:
        name (str): Name of the operation.
        get (str): GET url for the operation. Defaults to None.
        post (str): POST url for the operation. Defaults to None.

    Returns:
        cwt.wps.raw.ows.Operation: Minimally filled instance.
    """
    operation = Operation(name=name)

    http = HTTP()

    if get is not None:
        http.Get = [RequestMethodType(href=get)]

    if post is not None:
        http.Post = [RequestMethodType(href=post)]

    dcp = DCP()

    dcp.HTTP = http
    
    operation.DCP = [dcp]

    return operation

def operations_metadata(operations):
    """ Operations Metadata

    Returns:
        cwt.wps.raw.ows.OperationsMetadata: Minimally filled instance.
    """
    metadata = OperationsMetadata()

    metadata.Operation = operations

    return metadata

def service_contact():
    """ Service Contact

    Returns:
        cwt.wps.raw.ows.ResponsiblePartySubsetType: Minimally filled instance.
    """
    contact = ResponsiblePartySubsetType()

    return contact

def service_provider(name, contact):
    """ Service Provider

    Args:
        name (str): The provider name.
        contact (cwt.wps.raw.ows.ResponsiblePartySubsetType): Provider contact.

    Returns:
        cwt.wps.raw.ows.ServiceProvider: Minimally filled instance.
    """
    service = ServiceProvider()

    service.ProviderName = name

    service.ServiceContact = contact

    return service

def service_identification(title, abstract, keywords=None):
    """ Service Identification

    Args:
        title (str): The service title.
        abstract (str): The service abstract.
        keywords (list): A list of string keywords. Defaults to None.

    Returns:
        cwt.wps.raw.ows.ServiceIdentification: Minimally filled instance.
    """
    service = ServiceIdentification()

    service.Title = [title]

    service.Abstract = [abstract]

    if keywords is None:
        keywords = []

    service.Keywords = keywords

    service.ServiceType = 'WPS'

    service.ServiceTypeVersion = [VersionType('1.0.0')]

    return service
