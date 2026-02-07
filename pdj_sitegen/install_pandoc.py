"install pandoc using pypandoc"

from pypandoc.pandoc_download import download_pandoc  # type: ignore[import-untyped]  # pyright: ignore[reportMissingTypeStubs]

if __name__ == "__main__":
	download_pandoc(targetfolder=".venv/pandoc/")
