from cerver.utils.log import LOG_TYPE_NONE, cerver_log_both

from .lib import libauth, libmagic

DILLO_VERSION = "0.2.1"
DILLO_VERSION_NAME = "Version 0.2.1"
DILLO_VERSION_DATE = "19/04/2023"
DILLO_VERSION_TIME = "16:47 CST"
DILLO_VERSION_AUTHOR = "Erick Salas"

version = {
	"id": DILLO_VERSION,
	"name": DILLO_VERSION_NAME,
	"date": DILLO_VERSION_DATE,
	"time": DILLO_VERSION_TIME,
	"author": DILLO_VERSION_AUTHOR
}

dillo_libauth_version_print_full = libauth.dillo_libauth_version_print_full
dillo_libauth_version_print_version_id = libauth.dillo_libauth_version_print_version_id
dillo_libauth_version_print_version_name = libauth.dillo_libauth_version_print_version_name

dillo_libmagic_version_print_full = libmagic.dillo_libmagic_version_print_full
dillo_libmagic_version_print_version_id = libmagic.dillo_libmagic_version_print_version_id
dillo_libmagic_version_print_version_name = libmagic.dillo_libmagic_version_print_version_name

def pydillo_version_print_full ():
	output = "\nPyDillo Version: {name}\n" \
		"Release Date: {date} - {time}\n" \
		"Author: {author}\n".format (**version)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		output.encode ("utf-8")
	)

def pydillo_version_print_version_id ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPyDillo Version ID: {version.id}\n".encode ("utf-8")
	)

def pydillo_version_print_version_name ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPyDillo Version: {version.name}\n".encode ("utf-8")
	)
