#! /usr/bin/env python

from functools import partial
import re

from esgf.wps_lib import namespace as ns
from esgf.wps_lib import xml

# Element bounds
zero_one_element = partial(xml.Element, minimum=0)
one_many_element = partial(xml.Element, maximum=None, output_list=True)
zero_many_element = partial(xml.Element, minimum=0, maximum=None, output_list=True)

# Simple namespace min/max = 1 (required)
ows_element = partial(xml.Element, namespace=ns.OWS)
wps_element = partial(xml.Element, namespace=ns.WPS)

# Common namespace element with bounds
ows_zero_one_element = partial(zero_one_element, namespace=ns.OWS)
ows_one_many_element = partial(one_many_element, namespace=ns.OWS)
ows_zero_many_element = partial(zero_many_element, namespace=ns.OWS)
wps_zero_one_element = partial(zero_one_element, namespace=ns.WPS)
wps_one_many_element = partial(one_many_element, namespace=ns.WPS)
wps_zero_many_element = partial(zero_many_element, namespace=ns.WPS)

class WPSTranslator(xml.Translator):

    def property_to_attribute(self, name):
        parts = name.split('_')

        return ''.join([parts[0]] + [x.title() for x in parts[1:]])

    def property_to_element(self, name):
        return ''.join(x.title() for x in name.split('_'))

    def attribute_to_property(self, name):
        matches = re.match('^([a-z]*)([A-Z][a-z]*)*$', name).groups()
        
        return '_'.join(x.lower() for x in matches if x is not None)

    def element_to_property(self, name):
        matches = re.findall('[A-Z][^A-Z]*', name)

        return '_'.join(x.lower() for x in matches)

class Exception(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    MissingParameterValue = 'MissingParameterValue'
    InvalidParameterValue = 'InvalidParameterValue'
    VersionNegotiationFailed = 'VersionNegotiationFailed'
    InvalidUpdateSequence = 'InvalidUpdateSequence'
    NoApplicableCode = 'NoApplicableCode'
    NotEnoughStorage = 'NotEnoughStorage'
    ServerBusy = 'ServerBusy'
    FileSizeExceeded = 'FileSizeExceeded'
    StorageNotSupported = 'StorageNotSupported'

    def __init__(self):
        super(Exception, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

    @ows_zero_many_element()
    def exception_text(self):
        pass

    @xml.Attribute(required=True)
    def exception_code(self):
        pass

    @xml.Attribute()
    def locator(self):
        pass

class ExceptionReport(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ExceptionReport, self).__init__(namespace=ns.OWS,
                nsmap=ns.NSMAP,
                translator=WPSTranslator())

    @ows_one_many_element(value_type=Exception)
    def exception(self):
        pass

    @xml.Attribute(required=True)
    def version(self):
        pass

class ComplexData(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ComplexData, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

    @xml.Attribute()
    def mime_type(self):
        pass

    @xml.Attribute()
    def encoding(self):
        pass

    @xml.Attribute()
    def schema(self):
        pass

    @xml.Element(store_value=True)
    def value(self):
        pass

class LiteralData(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(LiteralData, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

    @xml.Attribute()
    def data_type(self):
        pass

    @xml.Attribute()
    def uom(self):
        pass

    @xml.Element(store_value=True)
    def value(self):
        pass

class BoundingBoxData(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(BoundingBoxData, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

    @ows_element(value_type=float, output_list=True)
    def lower_corner(self):
        pass

    @ows_element(value_type=float, output_list=True)
    def upper_corner(self):
        pass

    @ows_zero_one_element()
    def crs(self):
        pass

    @ows_zero_one_element(value_type=int)
    def dimensions(self):
        pass

class OutputReference(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(OutputReference, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @xml.Attribute()
    def format(self):
        pass

    @xml.Attribute()
    def encoding(self):
        pass

    @xml.Attribute()
    def schema(self):
        pass

    @xml.Attribute(required=True)
    def href(self):
        pass

class Output(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(Output, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @ows_element()
    def identifier(self):
        pass

    @ows_element()
    def title(self):
        pass

    @ows_zero_one_element()
    def abstract(self):
        pass

    @wps_zero_one_element(value_type=OutputReference)
    def reference(self):
        pass

    @zero_one_element(value_type=(ComplexData, LiteralData, BoundingBoxData))
    def data(self):
        pass

class DocumentOutputDefinition(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(DocumentOutputDefinition, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @ows_zero_one_element()
    def mime_type(self):
        pass

    @ows_zero_one_element()
    def encoding(self):
        pass

    @ows_zero_one_element()
    def schema(self):
        pass

    @ows_zero_one_element()
    def uom(self):
        pass

    @xml.Attribute(default_value=False)
    def as_reference(self):
        pass

    @ows_element()
    def identifier(self):
        pass

    @ows_zero_one_element()
    def title(self):
        pass

    @ows_zero_one_element()
    def abstract(self):
        pass

class ResponseDocument(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ResponseDocument, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @xml.Attribute(value_type=bool, default_value=False)
    def store_execute_resposne(self):
        pass

    @xml.Attribute(value_type=bool, default_value=False)
    def lineage(self):
        pass

    @xml.Attribute(value_type=bool, default_value=False)
    def status(self):
        pass

    @zero_many_element(value_type=DocumentOutputDefinition)
    def output(self):
        pass

class RawDataOutput(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(RawDataOutput, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @ows_element()
    def identifier(self):
        pass

    @ows_zero_one_element()
    def mime_type(self):
        pass
    
    @ows_zero_one_element()
    def encoding(self):
        pass

    @ows_zero_one_element()
    def schema(self):
        pass

    @ows_zero_one_element()
    def uom(self):
        pass

class Reference(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(Reference, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @xml.Attribute()
    def mime_type(self):
        pass

    @xml.Attribute()
    def encoding(self):
        pass

    @xml.Attribute()
    def schema(self):
        pass

    @wps_element(store_attr=True, attr_namespace=ns.XLINK)
    def href(self):
        pass

    @wps_zero_one_element()
    def method(self):
        pass
    
    @wps_zero_one_element()
    def header(self):
        pass

    @wps_zero_one_element()
    def body(self):
        pass

    @wps_zero_one_element()
    def body_reference(self):
        pass

class Input(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(Input, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @ows_element()
    def identifier(self):
        pass

    @ows_zero_one_element()
    def title(self):
        pass

    @ows_zero_one_element()
    def abstract(self):
        pass

    @xml.Element(value_type=(Reference, ComplexData, LiteralData, BoundingBoxData))
    def data(self):
        pass

class Format(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(Format, self).__init__(nsmap=ns.NSMAP)

    @xml.Element()
    def mime_type(self):
        pass

    @xml.Element(minimum=0)
    def encoding(self):
        pass

    @xml.Element(minimum=0)
    def schema(self):
        pass

class ComplexDataDescription(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ComplexDataDescription, self).__init__(nsmap=ns.NSMAP)

    @xml.Element(path='Default', value_type=Format)
    def default(self):
        pass

    @xml.Element(maximum=None, value_type=Format, output_list=True)
    def supported(self):
        pass

    @xml.Attribute(value_type=int)
    def maximum_megabytes(self):
        pass

class UOMS(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(UOMS, self).__init__(nsmap=ns.NSMAP)

    @xml.Element(child_pag='UOM', child_namespace=ns.OWS)
    def default(self):
        pass

    @xml.Element(child_tag='UOM', child_namespace=ns.OWS, maximum=None,
            output_list=True)
    def supported(self):
        pass

class Range(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(Range, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

    @ows_zero_one_element()
    def minimum_value(self):
        pass

    @ows_zero_one_element()
    def maximum_value(self):
        pass

    @ows_zero_one_element()
    def spacing(self):
        pass

    @ows_zero_one_element()
    def range_closure(self):
        pass

class AllowedValues(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(AllowedValues, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

    @ows_zero_many_element()
    def value(self):
        pass

    @ows_zero_many_element(value_type=Range)
    def range(self):
        pass

class AnyValue(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(AnyValue, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

class ValuesReference(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ValuesReference, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

    @ows_element()
    def reference(self):
        pass

    @ows_element()
    def values_form(self):
        pass

class LiteralDataDescription(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(LiteralDataDescription, self).__init__(nsmap=ns.NSMAP)

    @ows_zero_one_element()
    def data_type(self):
        pass

    @xml.Element(minimum=0, value_type=UOMS)
    def uoms(self):
        pass

    @xml.Element(value_type=(AllowedValues, AnyValue, ValuesReference))
    def value(self):
        pass

    @xml.Element(minimum=0)
    def default_value(self):
        pass

class BoundingBoxDataDescription(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(BoundingBoxDataDescription, self).__init__(nsmap=ns.NSMAP)

    @xml.Element()
    def default(self):
        pass

    @xml.Element(maximum=None, output_list=True)
    def supported(self):
        pass

class InputDescription(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(InputDescription, self).__init__(nsmap=ns.NSMAP)

    @ows_element()
    def identifier(self):
        pass

    @ows_element()
    def title(self):
        pass

    @ows_zero_one_element()
    def abstract(self):
        pass

    @xml.Attribute(required=True, value_type=int)
    def min_occurs(self):
        pass

    @xml.Attribute(required=True, value_type=int)
    def max_occurs(self):
        pass

    @ows_zero_many_element()
    def metadata(self):
        pass

    @xml.Element(value_type=(ComplexDataDescription,
        LiteralDataDescription,
        BoundingBoxDataDescription))
    def value(self):
        pass

class OutputDescription(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(OutputDescription, self).__init__(nsmap=ns.NSMAP)

    @ows_element()
    def identifier(self):
        pass

    @ows_element()
    def title(self):
        pass

    @ows_zero_one_element()
    def abstract(self):
        pass

    @ows_zero_many_element()
    def metadata(self):
        pass

    @xml.Element(value_type=(ComplexDataDescription,
        LiteralDataDescription,
        BoundingBoxDataDescription))
    def value(self):
        pass

class ProcessDescription(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ProcessDescription, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @ows_element()
    def identifier(self):
        pass

    @ows_element()
    def title(self):
        pass

    @ows_zero_one_element()
    def abstract(self):
        pass

    @ows_zero_many_element()
    def metadata(self):
        pass

    @wps_zero_many_element()
    def profile(self):
        pass

    @xml.Attribute(required=True, namespace=ns.WPS)
    def process_version(self):
        pass

    @wps_zero_one_element()
    def wsdl(self):
        pass

    @xml.Element(path='DataInputs', value_type=InputDescription, minimum=0,
            maximum=None,
            output_list=True)
    def input(self):
        pass

    @xml.Element(path='ProcessOutputs', value_type=OutputDescription,
            maximum=None,
            output_list=True)
    def output(self):
        pass

    @xml.Attribute(value_type=bool, default=False)
    def store_supported(self):
        pass

    @xml.Attribute(value_type=bool, default=False)
    def status_supported(self):
        passs

class Languages(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(Languages, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @wps_element(child_tag='Language', child_namespace=ns.OWS)
    def default(self):
        pass

    @wps_one_many_element(child_tag='Language', child_namespace=ns.OWS, combine=True)
    def supported(self):
        pass

class Process(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(Process, self).__init__(namespace=ns.WPS, nsmap=ns.NSMAP)

    @xml.Attribute(namespace=ns.WPS)
    def process_version(self):
        pass

    @wps_element()
    def identifier(self):
        pass

    @wps_element()
    def title(self):
        pass

    @wps_zero_one_element()
    def abstract(self):
        pass

    @ows_zero_many_element(store_attr=True, name='title',
            attr_namespace=ns.XLINK)
    def metadata(self):
        pass

    @wps_zero_many_element()
    def profile(self):
        pass

    @wps_zero_one_element()
    def wsdl(self):
        pass

class Operation(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(Operation, self).__init__(namespace=ns.OWS, nsmap=ns.NSMAP)

    @xml.Attribute(required=True) 
    def name(self):
        pass

    @ows_zero_one_element(path='DCP/HTTP', store_attr=True, name='href',
            nsmap={'DCP': ns.OWS, 'HTTP': ns.OWS}, attr_namespace=ns.XLINK)
    def get(self):
        pass

    @ows_zero_one_element(path='DCP/HTTP', store_attr=True, name='href',
            nsmap={'DCP': ns.OWS, 'HTTP': ns.OWS}, attr_namespace=ns.XLINK)
    def post(self):
        pass

class ServiceContact(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ServiceContact, self).__init__(namespace=ns.OWS,
                nsmap=ns.NSMAP)
    
    @ows_element()
    def individual_name(self):
        pass

    @ows_element()
    def position_name(self):
        pass

    @ows_zero_one_element(path='ContactInfo/Phone',
            nsmap={'ContactInfo': ns.OWS,'Phone': ns.OWS,})
    def voice(self):
        pass

    @ows_zero_one_element(path='ContactInfo/Phone',
            nsmap={'ContactInfo': ns.OWS,'Phone': ns.OWS,})
    def facsimile(self):
        pass

    @ows_zero_one_element(path='ContactInfo/Address',
            nsmap={'ContactInfo': ns.OWS,'Address': ns.OWS})
    def delivery_point(self):
        pass

    @ows_zero_one_element(path='ContactInfo/Address',
            nsmap={'ContactInfo': ns.OWS,'Address': ns.OWS})
    def city(self):
        pass

    @ows_zero_one_element(path='ContactInfo/Address',
            nsmap={'ContactInfo': ns.OWS,'Address': ns.OWS})
    def administrative_area(self):
        pass

    @ows_zero_one_element(path='ContactInfo/Address',
            nsmap={'ContactInfo': ns.OWS,'Address': ns.OWS})
    def postal_code(self):
        pass

    @ows_zero_one_element(path='ContactInfo/Address',
            nsmap={'ContactInfo': ns.OWS,'Address': ns.OWS})
    def country(self):
        pass

    @ows_zero_one_element(path='ContactInfo/Address',
            nsmap={'ContactInfo': ns.OWS,'Address': ns.OWS})
    def electronic_mail_address(self):
        pass

class ServiceProvider(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ServiceProvider, self).__init__(namespace=ns.OWS,
                nsmap=ns.NSMAP)

    @ows_element()
    def provider_name(self):
        pass

    @ows_zero_one_element(store_attr=True, name='href', attr_namespace=ns.XLINK)
    def provider_site(self):
        pass

    @ows_zero_one_element()
    def service_contact(self):
        pass

class ServiceIdentification(xml.XMLDocument):
    __metaclass__ = xml.XMLDocumentMarkupType

    def __init__(self):
        super(ServiceIdentification, self).__init__(namespace=ns.OWS,
                nsmap=ns.NSMAP)

    @ows_element()
    def service_type(self):
        pass

    @ows_one_many_element()
    def service_type_version(self):
        pass

    @ows_zero_many_element()
    def profile(self):
        pass

    #@ows_one_many_element()
    @ows_element()
    def title(self):
        pass

    @ows_zero_many_element()
    def abstract(self):
        pass

    @ows_zero_many_element(child_tag='Keyword', child_namespace=ns.OWS, combine=True)
    def keywords(self):
        pass

    @ows_zero_one_element()
    def fees(self):
        pass

    @ows_zero_many_element()
    def access_constraints(self):
        pass
