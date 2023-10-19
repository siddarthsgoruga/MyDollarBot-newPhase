# Import necessary modules to manage sys.path and directories
import os
import sys

# Add the current working directory to sys.path
# This is useful for locating and importing modules or packages in the current directory
sys.path.insert(0, os.getcwd() + "/code")
