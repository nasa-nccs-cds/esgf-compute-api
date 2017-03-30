"""
Unittest for parameter class.
"""

from unittest import TestCase

from cwt import Parameter

class TestImpl(Parameter):
    """ Test class for overriding method. """
    def __init__(self):
        """ Testimpl init. """
        super(TestImpl, self).__init__('test')

    def parameterize(self):
        """ Overridden parameterize method. """
        return 'param'

class TestParameter(TestCase):
    """ Test Case for Parameter class. """

    def test_repr(self):
        """ Test repr value. """
        param = Parameter('v0')

        self.assertEqual(repr(param),
                         "Parameter(name='v0')")

    def test_str(self):
        """ Test str value. """
        param = Parameter('v0')

        self.assertEqual(str(param),
                         "name=v0")

    def test_from_dict(self):
        """ Test from dict. """
        with self.assertRaises(NotImplementedError):
            param = Parameter.from_dict('test')

    def test_parameterize(self):
        """ Testing overriding parameterize method. """

        with self.assertRaises(NotImplementedError):
            param = Parameter('test')
            param.parameterize()

        over_param = TestImpl()

        self.assertEqual(over_param.parameterize(), 'param')