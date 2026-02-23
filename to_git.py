#!python3
"""Import packages"""
import sys
import subprocess

try:
    # Run the batch file to set up redirection
    # ON PC
    subprocess.run(['F:\\blrobot26\\to_git.bat'], check=False)
    # ON LAPTOP
    #subprocess.run(['C:\\Users\\enado\\Proyectos\\Python33\\blrobot26\\redir.bat'], check=False)
    #subprocess.run(['C:\\Users\\enado\\blrobot25\\redir.bat'], check=False) #or your own path
    print("Commiting to Git...")


except IndexError:
    print("Unexpected error", sys.exc_info()[0])

except OSError as err:
    print("OS error: {0}".format(err))

except ValueError:
    print("Could not convert data to an integer.", sys.exc_info()[0])

except KeyError:
    print("Unexpected error", sys.exc_info()[0])

except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

print("Task completed")
