"""Command-line entry point for pdj-sitegen.

This module provides the main entry point when running pdj-sitegen as a module
(python -m pdj_sitegen). It handles:

- Invoking the build pipeline via build.main()
- Catching KeyboardInterrupt for clean exit (exit code 130)
- Catching and formatting build errors using the error_report module
"""

import sys
from pathlib import Path

from pdj_sitegen.build import main
from pdj_sitegen.error_report import handle_build_error

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nInterrupted.", file=sys.stderr)
		sys.exit(130)
	except Exception as e:
		handle_build_error(e, Path.cwd())
		sys.exit(1)
