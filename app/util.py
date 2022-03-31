from factiva.core import get_factiva_logger

logger = get_factiva_logger()

def my_custom_function(message) -> dict:
    logger.info('my custom message from my custom function')
    message['custom'] = 'Custom value'
    return message
