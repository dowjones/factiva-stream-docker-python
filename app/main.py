from factiva.core import logger
from factiva.news import Listener
# I just noticed BQ handler is inside Listener, please group them in a handlers module inside factiva.news.stream
from factiva.news.stream.handlers import JSONFilesHandler, BigQueryHandler
import util as u

logger.info('************************************ Factiva Stream Docker Client - Start *************************************')

# To optimise connections, a connection instance can be created at the BigQueryHandler class __init__
# method to avoid a new client creation with each mesasage processing.
bq_handler = BigQueryHandler()  
json_handler = JSONFilesHandler()
listener = Listener()

logger.info(f'Listener is started')

def message_handler(message: dict, subscription_id: str) -> bool:
    ret_val = False
    message = u.my_custom_function(message)
    ret_val = bq_handler.save_on_bigquery_table(message, subscription_id)
    ret_val = ret_val & json_handler.save_json_file(message, subscription_id)
    logger.info('My Custom Log - Processed a message')
    message_handler.counter += 1
    return ret_val

message_handler.counter = 0
listener.listen(message_handler)

logger.info('************************************* Factiva Stream Docker Client - Stop *************************************')
logger.info('***************************************************************************************************************')
