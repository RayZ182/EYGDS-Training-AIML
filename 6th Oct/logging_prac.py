import logging

# configure logging
logging.basicConfig(
    level = logging.WARNING,
    filename = 'app.log',
    format = '%(asctime)s - %(name)s - %(message)s'
)

# logging examples
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')