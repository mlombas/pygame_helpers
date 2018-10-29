#Little trick so python dont stress over little imports
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
