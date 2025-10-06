import logging

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s')

class InvalidMarksError(Exception):
    pass

def check_marks(m):
    if m < 0 or m > 100:
        raise InvalidMarksError("Marks must be within 0 and 100")

try:
    check_marks(102)
except InvalidMarksError as e:
    logging.error(e)
