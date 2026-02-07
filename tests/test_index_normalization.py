"""Tests for index file name normalization (_index.md -> index.html)."""

from pathlib import Path

import pytest
from jinja2 import Environment

from pdj_sitegen.build import build_document_tree
from pdj_sitegen.exceptions import ConflictingIndexError


class TestIndexNormalization:
	"""Tests for _index.md -> index.html normalization."""

	def test_underscore_index_becomes_index_html(
		self, temp_site_structure: dict[str, Path]
	) -> None:
		"""_index.md should produce index.html when normalize_index_names is True."""
		content_dir = temp_site_structure["content_dir"]

		# Create _index.md
		index_file = content_dir / "_index.md"
		index_file.write_text(
			"""---
title: Home
---
# Welcome
"""
		)

		jinja_env = Environment()
		docs = build_document_tree(
			content_dir=content_dir,
			frontmatter_context={},
			jinja_env=jinja_env,
			verbose=False,
			normalize_index_names=True,
		)

		# Should have one document keyed by "_index"
		assert "_index" in docs
		# But path_html should be "index.html"
		assert docs["_index"]["file_meta"]["path_html"] == "index.html"

	def test_underscore_index_in_subdir(
		self, temp_site_structure: dict[str, Path]
	) -> None:
		"""_index.md in subdirectory should produce subdir/index.html."""
		content_dir = temp_site_structure["content_dir"]

		# Create subdirectory with _index.md
		subdir = content_dir / "blog"
		subdir.mkdir()
		index_file = subdir / "_index.md"
		index_file.write_text(
			"""---
title: Blog
---
# Blog
"""
		)

		jinja_env = Environment()
		docs = build_document_tree(
			content_dir=content_dir,
			frontmatter_context={},
			jinja_env=jinja_env,
			verbose=False,
			normalize_index_names=True,
		)

		# Should have document keyed by "blog/_index"
		assert "blog/_index" in docs
		# But path_html should be "blog/index.html"
		assert docs["blog/_index"]["file_meta"]["path_html"] == "blog/index.html"

	def test_regular_index_unchanged(
		self, temp_site_structure: dict[str, Path]
	) -> None:
		"""Regular index.md should still produce index.html."""
		content_dir = temp_site_structure["content_dir"]

		# Create regular index.md
		index_file = content_dir / "index.md"
		index_file.write_text(
			"""---
title: Home
---
# Welcome
"""
		)

		jinja_env = Environment()
		docs = build_document_tree(
			content_dir=content_dir,
			frontmatter_context={},
			jinja_env=jinja_env,
			verbose=False,
			normalize_index_names=True,
		)

		assert "index" in docs
		assert docs["index"]["file_meta"]["path_html"] == "index.html"

	def test_normalization_disabled(self, temp_site_structure: dict[str, Path]) -> None:
		"""When normalize_index_names is False, _index.md stays as _index.html."""
		content_dir = temp_site_structure["content_dir"]

		# Create _index.md
		index_file = content_dir / "_index.md"
		index_file.write_text(
			"""---
title: Home
---
# Welcome
"""
		)

		jinja_env = Environment()
		docs = build_document_tree(
			content_dir=content_dir,
			frontmatter_context={},
			jinja_env=jinja_env,
			verbose=False,
			normalize_index_names=False,
		)

		assert "_index" in docs
		# path_html should remain "_index.html"
		assert docs["_index"]["file_meta"]["path_html"] == "_index.html"


class TestConflictingIndexFiles:
	"""Tests for error handling when both index.md and _index.md exist."""

	def test_conflict_in_root(self, temp_site_structure: dict[str, Path]) -> None:
		"""Both index.md and _index.md in root should raise error."""
		content_dir = temp_site_structure["content_dir"]

		# Create both index files
		(content_dir / "index.md").write_text(
			"""---
title: Home 1
---
# Welcome 1
"""
		)
		(content_dir / "_index.md").write_text(
			"""---
title: Home 2
---
# Welcome 2
"""
		)

		jinja_env = Environment()
		with pytest.raises(ConflictingIndexError) as exc_info:
			build_document_tree(
				content_dir=content_dir,
				frontmatter_context={},
				jinja_env=jinja_env,
				verbose=False,
				normalize_index_names=True,
			)

		assert "(root)" in str(exc_info.value)
		assert "_index.md" in str(exc_info.value)
		assert "index.md" in str(exc_info.value)

	def test_conflict_in_subdirectory(
		self, temp_site_structure: dict[str, Path]
	) -> None:
		"""Both index.md and _index.md in subdirectory should raise error."""
		content_dir = temp_site_structure["content_dir"]

		# Create subdirectory with both index files
		subdir = content_dir / "blog"
		subdir.mkdir()
		(subdir / "index.md").write_text(
			"""---
title: Blog 1
---
# Blog 1
"""
		)
		(subdir / "_index.md").write_text(
			"""---
title: Blog 2
---
# Blog 2
"""
		)

		jinja_env = Environment()
		with pytest.raises(ConflictingIndexError) as exc_info:
			build_document_tree(
				content_dir=content_dir,
				frontmatter_context={},
				jinja_env=jinja_env,
				verbose=False,
				normalize_index_names=True,
			)

		assert "blog" in str(exc_info.value)

	def test_no_conflict_when_normalization_disabled(
		self, temp_site_structure: dict[str, Path]
	) -> None:
		"""Conflict check should be skipped when normalize_index_names is False."""
		content_dir = temp_site_structure["content_dir"]

		# Create both index files
		(content_dir / "index.md").write_text(
			"""---
title: Home 1
---
# Welcome 1
"""
		)
		(content_dir / "_index.md").write_text(
			"""---
title: Home 2
---
# Welcome 2
"""
		)

		jinja_env = Environment()
		# Should NOT raise when normalization is disabled
		docs = build_document_tree(
			content_dir=content_dir,
			frontmatter_context={},
			jinja_env=jinja_env,
			verbose=False,
			normalize_index_names=False,
		)

		# Both files should be processed
		assert "index" in docs
		assert "_index" in docs
		assert docs["index"]["file_meta"]["path_html"] == "index.html"
		assert docs["_index"]["file_meta"]["path_html"] == "_index.html"

	def test_no_conflict_separate_directories(
		self, temp_site_structure: dict[str, Path]
	) -> None:
		"""index.md and _index.md in different directories should not conflict."""
		content_dir = temp_site_structure["content_dir"]

		# index.md in root
		(content_dir / "index.md").write_text(
			"""---
title: Home
---
# Welcome
"""
		)

		# _index.md in subdirectory
		subdir = content_dir / "blog"
		subdir.mkdir()
		(subdir / "_index.md").write_text(
			"""---
title: Blog
---
# Blog
"""
		)

		jinja_env = Environment()
		# Should NOT raise
		docs = build_document_tree(
			content_dir=content_dir,
			frontmatter_context={},
			jinja_env=jinja_env,
			verbose=False,
			normalize_index_names=True,
		)

		assert "index" in docs
		assert "blog/_index" in docs
		assert docs["index"]["file_meta"]["path_html"] == "index.html"
		assert docs["blog/_index"]["file_meta"]["path_html"] == "blog/index.html"
