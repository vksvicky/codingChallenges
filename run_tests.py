import unittest
import sys
import os

def run_tests():
    # Get the absolute path to the tests directory
    tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir, pattern='test_*.py')
    
    # Create test runner with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())