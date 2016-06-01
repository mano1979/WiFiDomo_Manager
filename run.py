
from app.wifidomo_manager import app
from modules.config import config

app.run(
    port=config.getint('system', 'port'),
    host=config.get('system', 'listen'),
    debug=config.getboolean('system', 'debug')
)