#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	import dotenv
	dotenv.read_dotenv()
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taxi_ticket.settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
