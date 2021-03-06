""" Domain Unittest """

import unittest

import cwt

class TestDomain(unittest.TestCase):
    """ Domain Test Case """

    def test_parameterize(self):
        expected = { 'id': 'd0', 'lat': { 'start': 0, 'end': 90, 'step': 1, 'crs': 'values' } }

        dom = cwt.Domain([cwt.Dimension('lat', 0, 90)], name='d0')

        self.assertDictContainsSubset(expected, dom.parameterize())

    def test_add_dimension(self):
        dom = cwt.Domain()

        dom.add_dimension(cwt.Dimension('lat', 0, 90))

        self.assertEqual(len(dom.dimensions), 1)

    def test_get_dimension(self):
        dom = cwt.Domain([cwt.Dimension('lat', 0, 90)])

        dimension = dom.get_dimension('lat')

        self.assertIsNotNone(dimension)

    def test_from_dict_missing_id(self):
        data = { }

        with self.assertRaises(cwt.ParameterError):
            cwt.Domain.from_dict(data)

    def test_from_dict(self):
        data = {
                'id': 'd0',
                'mask': 'var_data>0.5',
                'lat': {
                        'start': 0,
                        'end': 90,
                        'crs': 'values',
                        'step': 2
                       }
               }

        dom = cwt.Domain.from_dict(data)

        self.assertEqual(dom.name, 'd0')
        self.assertIsInstance(dom.dimensions, list)
        self.assertEqual(len(dom.dimensions), 1)
        self.assertIsInstance(dom.mask, cwt.Mask)
        

    def test_empty_domain(self):
        expected = {}

        dom = cwt.Domain()

        self.assertDictContainsSubset(expected, dom.parameterize())

if __name__ == '__main__':
    unittest.main()
