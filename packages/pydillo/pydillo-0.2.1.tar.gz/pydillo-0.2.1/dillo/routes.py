from ctypes import c_void_p, c_char_p, c_int

from cerver.http import HTTP_ROUTE_AUTH_TYPE_CUSTOM
from cerver.http import RequestMethod
from cerver.http import HttpHandler
from cerver.http import http_route_create
from cerver.http import http_route_set_custom_data
from cerver.http import http_route_set_delete_custom_data
from cerver.http import http_route_set_auth
from cerver.http import http_route_set_authentication_handler

from cerver.http import http_cerver_enable_admin_routes
from cerver.http import http_cerver_admin_routes_set_custom_data
from cerver.http import http_cerver_admin_routes_set_delete_custom_data
from cerver.http import http_cerver_enable_admin_routes_authentication
from cerver.http import http_cerver_admin_routes_set_authentication_handler

from .lib import libauth

from .auth import DILLO_AUTH_SCOPE_SINGLE
from .auth import DILLO_AUTH_SCOPE_MANAGEMENT
from .auth import dillo_custom_authentication_handler

auth_route_delete = libauth.auth_route_delete
auth_route_delete.argtypes = [c_void_p]

auth_route_create = libauth.auth_route_create
auth_route_create.restype = c_void_p

auth_route_create_action = libauth.auth_route_create_action
auth_route_create_action.argtypes = [c_char_p]
auth_route_create_action.restype = c_void_p

auth_route_create_role = libauth.auth_route_create_role
auth_route_create_role.argtypes = [c_char_p, c_char_p]
auth_route_create_role.restype = c_void_p

auth_route_print = libauth.auth_route_print
auth_route_print.argtypes = [c_void_p]

# create route with common values
def dillo_route_create_internal (
	method: RequestMethod, path: str, handler: HttpHandler
) -> c_void_p:
	dillo_route = http_route_create (method, path.encode ("utf-8"), handler)

	http_route_set_auth (dillo_route, HTTP_ROUTE_AUTH_TYPE_CUSTOM)
	# http_route_set_delete_custom_data (dillo_route, auth_route_delete)
	http_route_set_authentication_handler (dillo_route, dillo_custom_authentication_handler)

	return dillo_route

def dillo_route_create (
	method: RequestMethod, path: str, handler: HttpHandler
) -> c_void_p:
	dillo_route = dillo_route_create_internal (method, path, handler)

	http_route_set_custom_data (dillo_route, auth_route_create ())

	return dillo_route

def dillo_action_route_create (
	method: RequestMethod, path: str, handler: HttpHandler, action: str
) -> c_void_p:
	action_route = dillo_route_create_internal (method, path, handler)

	http_route_set_custom_data (
		action_route, auth_route_create_action (action.encode ("utf-8"))
	)

	return action_route

def dillo_role_route_create (
	method: RequestMethod, path: str, handler: HttpHandler, role: str, action: str
) -> c_void_p:
	role_route = dillo_route_create_internal (method, path, handler)

	http_route_set_custom_data (
		role_route, auth_route_create_role (
			action.encode ("utf-8"), role.encode ("utf-8")
		)
	)

	return role_route

def dillo_admin_routes_configuration (http_cerver: c_void_p):
	http_cerver_enable_admin_routes (http_cerver, True)
	http_cerver_enable_admin_routes_authentication (http_cerver, HTTP_ROUTE_AUTH_TYPE_CUSTOM)
	http_cerver_admin_routes_set_custom_data (http_cerver, auth_route_create ())
	# http_cerver_admin_routes_set_delete_custom_data (http_cerver, auth_route_delete)
	http_cerver_admin_routes_set_authentication_handler (
		http_cerver, dillo_custom_authentication_handler
	)
