import unittest
import numpy as np

from graph_model_parser import GraphModelParser


class TestGraphModelParser(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        self.model_description = '''
            a_{t} = a_{t-1} + 1
            b_{t} = b_{t-1} + 2*b_{t-2} + a_{t}
            c_{t} = c_{t-1} + normal(1, 2)
            '''
        self.initial_values = {'a_0': 0, 'a_1': 1, 'b_0': 0, 'b_1': 1, 'c_0': 0}
        self.model = GraphModelParser(self.model_description, self.initial_values)

        # Missing initial values
        self.model_description_2 = ''' 
            b_{t} = b_{t-1} + 2*b_{t-2} + a_0
            c_{t} = c_{t-1} + normal(1, 2)
            '''
        self.initial_values_2 = {'b_0': 0, 'b_1': 1}
        self.model_2 = GraphModelParser(self.model_description_2, self.initial_values_2)

    def test_parse_model_description(self):
        self.assertEqual(len(self.model.formulas), 3)

    def test_variables(self):
        self.assertListEqual(self.model.variables, ['a', 'b', 'c'])

    def test_max_time_computed(self):
        self.assertEqual(self.model.max_time_computed, 0)

    def test_flatten_values(self):
        flattened_values = self.model.flatten_values(1)
        expected_values = {'a_0': 0, 'a_1': 1, 'b_0': 0, 'b_1': 1, 'c_0': 0}
        self.assertDictEqual(flattened_values, expected_values)

    def test_compute(self):
        computed_values_t2 = self.model.compute(2)
        self.assertIn('a_2', computed_values_t2)
        self.assertIn('b_2', computed_values_t2)
        self.assertIn('c_2', computed_values_t2)
        self.assertAlmostEqual(computed_values_t2['a_2'], 2, places=4)
        self.assertAlmostEqual(computed_values_t2['b_2'], 3, places=4)

    def test_call(self):
        computed_values_t3 = self.model(3)
        self.assertIn('a_3', computed_values_t3)
        self.assertIn('b_3', computed_values_t3)
        self.assertIn('c_3', computed_values_t3)
        self.assertAlmostEqual(computed_values_t3['a_3'], 3, places=4)
        self.assertAlmostEqual(computed_values_t3['b_3'], 8, places=4)

    def test_missing_initial_values(self):
        with self.assertRaises(ValueError):
            self.model_2(1)


if __name__ == '__main__':
    unittest.main()
