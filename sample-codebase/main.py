# main.py - Sample file with technical debt
import os
import sys
import json  # unused import
import datetime  # unused import
from utils import helper_function

def main():
    """Main entry point."""
    # TODO: add proper argument parsing
    print("Hello, World!")
    result = helper_function()
    unused_variable = 42
    return result

# def old_main():
#     """This was the old main function."""
#     print("Old implementation")
#     return None

if __name__ == "__main__":
    main()