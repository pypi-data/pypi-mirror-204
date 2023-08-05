from ctypes import c_void_p, c_char_p

from .lib import libauth

auth_service_new = libauth.auth_service_new
auth_service_new.restype = c_void_p

auth_service_delete = libauth.auth_service_delete
auth_service_delete.argtypes = [c_void_p]

auth_service_create = libauth.auth_service_create
auth_service_create.argtypes = [c_char_p, c_char_p, c_char_p]
auth_service_create.restype = c_void_p

auth_service_print = libauth.auth_service_print
auth_service_print.argtypes = [c_void_p]
