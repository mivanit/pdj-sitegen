from pathlib import Path
import pdj_sitegen.setup_site

TEMP_DIR: Path = Path("tests/_temp/test_setup")


def test_setup():
	TEMP_DIR.mkdir(parents=True, exist_ok=True)
	pdj_sitegen.setup_site.setup_site(TEMP_DIR)
