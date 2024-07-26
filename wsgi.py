import sys
sys.path.insert(0, '/var/www/iot_lab_game')

from iotgame import create_app
application = create_app()
