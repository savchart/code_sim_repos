import unittest
from index_repos import extract_token_names

class TestSimilarityCalculation(unittest.TestCase):

    def test_extract_token_names(self):
        code = """
        def hello_world():
            print("Hello, World!")
            
        hello_world()
        """


        with open("tmp_test_files/temp_test_code.py", "w") as f:
            f.write(code)

        expected_tokens = ['hello_world', 'print', 'hello_world']
        actual_tokens = extract_token_names("tmp_test_files/temp_test_code.py")
        self.assertEqual(actual_tokens, expected_tokens)

    def test_similarity_percentage(self):
        code1 = """
        def greet(name):
            print("Hello, " + name + "!")

        greet("Alice")
        """

        code2 = """
        def greet_someone(name):
            print("Hi, " + name + "!")

        greet_someone("Bob")
        """

        with open("tmp_test_files/temp_test_code1.py", "w") as f:
            f.write(code1)

        with open("tmp_test_files/temp_test_code2.py", "w") as f:
            f.write(code2)

        tokens1 = set(extract_token_names("tmp_test_files/temp_test_code1.py"))
        tokens2 = set(extract_token_names("tmp_test_files/temp_test_code2.py"))
        intersection_count = len(tokens1.intersection(tokens2))
        similarity = intersection_count / len(tokens1)

        expected_similarity = 0.6666666666666666
        self.assertAlmostEqual(similarity, expected_similarity)

if __name__ == "__main__":
    unittest.main()
