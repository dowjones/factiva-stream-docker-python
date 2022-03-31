from factiva.core import get_factiva_logger
from factiva.core.tools import load_environment_value

from factiva.news import (BigQueryHandler, JSONLFileHandler, Listener,
                          MongoDBHandler, Stream)

import util as u

VALID_WHERE_STATEMENT = "publication_datetime >= '2021-04-01 00:00:00' AND LOWER(language_code)='en' AND UPPER(source_code) = 'DJDN'"
VALID_STREAM_ID = load_environment_value('FACTIVA_STREAMID')

# To optimise connections, a connection instance can be created at the BigQueryHandler class __init__
# method to avoid a new client creation with each mesasage processing.
# All hadlers uses a message: dict & subscription_id: str as entry vars and the main function is "save"

#bq_handler = BigQueryHandler()
json_handler = JSONLFileHandler()
mongoDB = MongoDBHandler()

# Create logger instance
logger = get_factiva_logger()
logger.info(
    '************************************ Factiva Stream Docker Client - Start *************************************'
)
logger.info(f'Listener is started')

# Custom handler message_handler. On this example
# 1- Take the incomming message and make a transformation defined at my_custom_function
# 2- Save the message into a mongoDB
# 3- Save the message in to a jsonl file
def message_handler(message: dict, subscription_id: str) -> bool:
    ret_val = False
    message = u.my_custom_function(message)
    ret_val = mongoDB.save(message, subscription_id)
    ret_val = ret_val & json_handler.save(message, subscription_id)
    logger.info('My Custom Log - Processed a message')
    message_handler.counter += 1
    return ret_val

# Create a Stream instance using a existing streamId
stream = Stream(stream_id=VALID_STREAM_ID)

# Get the default subscription and the listener created on it
subscription = stream.get_suscription_by_index(0)
listener = subscription.listener

message_handler.counter = 0

# Use of the custom_handler to process all incomming messages
listener.listen(callback=message_handler, maximum_messages=100, batch_size=100)

#Also can be use the defined handlers directly
# listener.listen(callback=mongoDB.save, maximum_messages=100, batch_size=100)

logger.info(
    '************************************* Factiva Stream Docker Client - Stop *************************************'
)
logger.info(
    '***************************************************************************************************************'
)
