############################################################################
#
#   FIle: Environmental parameters
#
############################################################################

# Parameter : RUNNING_ON_RASPBERRYPI
# True: Running on Raspberry Pi tool
# False: Running on Windows PC for testing the GUI
RUNNING_ON_RASPBERRYPI = False 
RUNNING_ON_WINDOWS_WAVESHARE = True

# ECU_SIMULATOR_ENABLE : Set this to True if you want a background ECU simulator to run on a channel
# False: Simulator is disabled entirely.
ECU_SIMULATOR_ENABLE = True

# ECU_SIMULATOR_CHANNEL: Specify which channel the ECU simulator should listen on.
# Waveshare indices are typically 0 (CAN 1) and 1 (CAN 2).
ECU_SIMULATOR_CHANNEL = 1

# Parameter : DEBUG
# True: Debug mode is on and so we can put any needed print statements under this
# False: Debug mode is off and hence in realtime mode it is running. Deployment mode
DEBUG = False