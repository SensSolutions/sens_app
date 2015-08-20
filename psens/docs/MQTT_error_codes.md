# Error values

MQTT_ERR_AGAIN = -1
MQTT_ERR_SUCCESS = 0
MQTT_ERR_NOMEM = 1
MQTT_ERR_PROTOCOL = 2
MQTT_ERR_INVAL = 3
MQTT_ERR_NO_CONN = 4
MQTT_ERR_CONN_REFUSED = 5
MQTT_ERR_NOT_FOUND = 6
MQTT_ERR_CONN_LOST = 7
MQTT_ERR_TLS = 8
MQTT_ERR_PAYLOAD_SIZE = 9
MQTT_ERR_NOT_SUPPORTED = 10
MQTT_ERR_AUTH = 11
MQTT_ERR_ACL_DENIED = 12
MQTT_ERR_UNKNOWN = 13
MQTT_ERR_ERRNO = 14


## mqtt_errno

"""Return the error string associated with an mqtt error number."""

MQTT_ERR_SUCCESS = "No error."
MQTT_ERR_NOMEM = "Out of memory."
MQTT_ERR_PROTOCOL = "A network protocol error occurred when communicating with the broker."
MQTT_ERR_INVAL = "Invalid function arguments provided."
MQTT_ERR_NO_CONN = "The client is not currently connected."
MQTT_ERR_CONN_REFUSED = "The connection was refused."
MQTT_ERR_NOT_FOUND = "Message not found (internal error)."
MQTT_ERR_CONN_LOST = "The connection was lost."
MQTT_ERR_TLS = "A TLS error occurred."
MQTT_ERR_PAYLOAD_SIZE = "Payload too large."
MQTT_ERR_NOT_SUPPORTED = "This feature is not supported."
MQTT_ERR_AUTH = "Authorisation failed."
MQTT_ERR_ACL_DENIED = "Access denied by ACL."
MQTT_ERR_UNKNOWN = "Unknown error."
MQTT_ERR_ERRNO = "Error defined by errno."
    else = "Unknown error."


## connack_code

    """Return the string associated with a CONNACK result."""

connack_code == 0 = "Connection Accepted."
connack_code == 1 = "Connection Refused: unacceptable protocol version."
connack_code == 2 = "Connection Refused: identifier rejected."
connack_code == 3 = "Connection Refused: broker unavailable."
connack_code == 4 = "Connection Refused: bad user name or password."
connack_code == 5 = "Connection Refused: not authorised."
             else   "Connection Refused: unknown reason."
