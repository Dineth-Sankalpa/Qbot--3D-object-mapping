import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/netrunner/Documents/Robotics_and_Automation/CA/Qbot--3D-object-mapping/simulation/install/qbot_scanner'
