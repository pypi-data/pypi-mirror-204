import mysql.connector
import logging
import os
import constants

logger = logging.getLogger()
lambda_environment = os.environ.get('ENVIRONMENT', "DEV")
logging_level = "INFO" if lambda_environment == "DEV" else "WARN"
print("logging_level :" + logging_level)
logger.setLevel(logging_level)
logging.info("Initializing the  environment variables for the connection pool")

db_name = os.environ.get(constants.ENVIRONMENT_VARIABLE_DB_NAME,None)
db_port = os.environ.get(constants.ENVIRONMENT_VARIABLE_DB_PORT, None)
db_username = os.environ.get(constants.ENVIRONMENT_VARIABLE_DB_USERNAME, None)
db_password = os.environ.get(constants.ENVIRONMENT_VARIABLE_DB_PASSWORD, None)
rds_proxy_endpoint = os.environ.get(constants.ENVIRONMENT_VARIABLE_DB_PROXY_ENDPOINT, None)


def get_environment_variable(variable_name: object, default_value: object) -> object:
    return os.environ.get(variable_name, default_value)


def validate_parameter(parameter_name, parameter_value):
    if parameter_value is None or len(str(parameter_value)):
        raise ValueError(f"{parameter_name} must be defined")


def test_version():
    logging.info("Executing the version of this library ......................")


def delete_order(order_id):
    logging.info("Executing the delete_order(order_id) .........................")
    database_name = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_NAME, None)
    validate_parameter("db name", database_name)
    database_port = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_PORT, None)
    validate_parameter("db port", database_port)
    database_username = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_USERNAME, None)
    validate_parameter("db username", database_username)
    database_password = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_PASSWORD, None)
    validate_parameter("db password", database_password)
    rds_proxy_service_endpoint = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_PROXY_ENDPOINT, None)
    validate_parameter("rds proxy endpoint", rds_proxy_service_endpoint)

    mysql_connection = mysql.connector.connect(host=rds_proxy_service_endpoint, port=database_port, user=database_username,
                                               password=database_password, database=database_name)
    logging.info("Getting the current cursor .........................")
    current_connection_cursor = mysql_connection.cursor()
    delete_sql = "DELETE FROM ORDERS  WHERE ORDER_ID = '{orderId}';".format(orderId=order_id)
    current_connection_cursor.execute(delete_sql)
    current_connection_cursor.close()
    mysql_connection.commit()


def get_order_by_id(order_id):
    logging.info("Executing the get_order_by_id(order_id) .........................")
    database_name = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_NAME, None)
    validate_parameter("db name", database_name)
    database_port = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_PORT, None)
    validate_parameter("db port", database_port)
    database_username = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_USERNAME, None)
    validate_parameter("db username", database_username)
    database_password = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_PASSWORD, None)
    validate_parameter("db password", database_password)
    rds_proxy_service_endpoint = get_environment_variable(constants.ENVIRONMENT_VARIABLE_DB_PROXY_ENDPOINT, None)
    validate_parameter("rds proxy endpoint", rds_proxy_service_endpoint)

    mysql_connection = mysql.connector.connect(host=rds_proxy_service_endpoint, port=database_port, user=database_username,
                                               password=database_password, database=database_name)
    current_connection_cursor = mysql_connection.cursor()
    select_sql = "SELECT ORDER_ID,ORDER_NAME,ORDER_DATE FROM ORDERS WHERE ORDER_ID = '{orderId}';" .format(orderId=order_id)
    current_connection_cursor.execute(select_sql)
    orders = []
    for (orderId, orderName, orderDate) in current_connection_cursor:
        logging.info("orderId :" + str(orderId))
        logging.info("orderName :" + str(orderName))
        logging.info("orderDate :" + str(orderDate))
        order = {
            "orderId": str(orderId),
            "orderName": str(orderName),
            "orderDate": str(orderDate)
        }
        orders.append(order)
    if len(orders) > 0:
        return orders[0]
    return None

