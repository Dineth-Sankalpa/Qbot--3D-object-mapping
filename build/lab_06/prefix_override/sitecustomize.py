import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sanjuna/Desktop/FP_Robotics_and_Automation/Qbot--3D-object-mapping/install/lab_06'
