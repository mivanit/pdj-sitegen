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
