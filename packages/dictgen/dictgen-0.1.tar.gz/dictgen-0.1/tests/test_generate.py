import unittest

from dictgen import generate, max_height, max_depth
import dictgen

class TestGenerateDict(unittest.TestCase):

    def test_input_validation(self):
        with self.assertRaises(AttributeError):
            dictgen.generate(max_height=-1)

    def test_generate_dict(self):
        """Generate a dictionary using default args"""
        generate()
    
    def test_set_max_height(self):
        from pprint import pprint
        """Generate a dictionary with a specified max height"""
        for i in range(2, 9):
            result = generate(max_height=i, max_depth=3, rand_seed=i)
            self.assertLessEqual(max_height(result), i)
    
    def test_set_max_depth(self):
        """Generate a dictionary with a specified max depth"""
        for i in range(2, 100):
            result = generate(max_depth=i, rand_seed=i)
            self.assertLessEqual(max_depth(result), i)
    
    def test_seed(self):
        """Ensure using the same seed generates the same dictionary"""
        # We use json.dumps to generate a string we can use to compare the output
        import json

        for seed in range(1000, 1010):
            compare_str = json.dumps( generate(max_depth=5, max_height=5, rand_seed=seed) )
            for run_num in range(10):
                self.assertEqual( compare_str, json.dumps(generate(max_depth=5, max_height=5, rand_seed=seed)) )
    
    def test_customise_val_generators(self):
        """ Test customising the generators used to create values"""
        generate(val_generators=(dictgen.random_string, dictgen.random_bool, dictgen.random_int, dictgen.random_datetime, dictgen.random_none))
    
    def test_customise_key_generators(self):
        """ Test customising the generators used to create keys in the dictionary"""
        generate(key_generators=(dictgen.random_string, dictgen.random_bool, dictgen.random_int))
    
    def test_custom_generator(self):
        """ Test using a custom function to generate values """
        from uuid import uuid4

        def generate_uuid(**kwargs):
            return uuid4()
        
        generate(key_generators=(generate_uuid,), val_generators=(dictgen.random_string,))
