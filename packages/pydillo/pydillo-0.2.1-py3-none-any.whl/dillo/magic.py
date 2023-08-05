from ctypes import c_void_p, c_char_p, c_int, c_uint

from .lib import libmagic

SERVICE_STATUS_NONE = 0
SERVICE_STATUS_CONNECTED = 1
SERVICE_STATUS_READY = 2
SERVICE_STATUS_IDLE = 3
SERVICE_STATUS_WORK = 4
SERVICE_STATUS_DISCONNECTED = 5
SERVICE_STATUS_ENDING = 6
SERVICE_STATUS_ERROR = 7

service_status_to_string = libmagic.service_status_to_string
service_status_to_string.argtypes = [c_int]
service_status_to_string.restype = c_char_p

service_status_description = libmagic.service_status_description
service_status_description.argtypes = [c_int]
service_status_description.restype = c_char_p

MAGIC_REQUEST_NONE = 0
MAGIC_REQUEST_STORE_REGISTER = 1
MAGIC_REQUEST_STORE_UNREGISTER = 2
MAGIC_REQUEST_STORE_STATUS = 3
MAGIC_REQUEST_STORE_OPEN = 4
MAGIC_REQUEST_STORE_CLOSE = 5
MAGIC_REQUEST_STORE_DISABLE = 6
MAGIC_REQUEST_STORE_INFO = 7
MAGIC_REQUEST_STORE_STATS = 8
MAGIC_REQUEST_STORE_STREAM_UPDATE = 9
MAGIC_REQUEST_STORE_STREAM_FRAME = 10
MAGIC_REQUEST_STORE_ADD_CLIENT = 11
MAGIC_REQUEST_STORE_RMV_CLIENT = 12
MAGIC_REQUEST_STORE_ACCESS = 13
MAGIC_REQUEST_STORE_EXIT = 14
MAGIC_REQUEST_FRAME = 21
MAGIC_REQUEST_HUMANS_COUNT = 32
MAGIC_REQUEST_HANDS_COORDS = 33
MAGIC_REQUEST_FACE_COORDS = 34
MAGIC_REQUEST_POSE_STREAM = 41
MAGIC_REQUEST_POSE_OUTPUT = 42
MAGIC_REQUEST_CLIENT_STATUS = 51
MAGIC_REQUEST_CLIENT_CART = 52
MAGIC_REQUEST_CLIENT_ADD_PRODUCT = 53
MAGIC_REQUEST_CLIENT_RMV_PRODUCT = 54
MAGIC_REQUEST_TEST = 100
MAGIC_REQUEST_TEST_MSG = 101

magic_request_type_to_string = libmagic.magic_request_type_to_string
magic_request_type_to_string.argtypes = [c_int]
magic_request_type_to_string.restype = c_char_p

magic_request_type_description = libmagic.magic_request_type_description
magic_request_type_description.argtypes = [c_int]
magic_request_type_description.restype = c_char_p

magic_init = libmagic.magic_init
magic_init.argtypes = [c_char_p, c_char_p, c_void_p, c_void_p]
magic_init.restype = c_uint

magic_end = libmagic.magic_end

magic_handler_make_request = libmagic.magic_handler_make_request
magic_handler_make_request.argtypes = [c_void_p, c_int, c_char_p, c_char_p, c_char_p]
magic_handler_make_request.restype = c_uint
