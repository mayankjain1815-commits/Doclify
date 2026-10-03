from doclify.utils.extract import extract_file_content, MAX_FILE_SIZE


def _is_treated_as_valid_content(chunks):
    """Exact validity predicate used by doclify/components/run.py and update.py."""
    return not any(c.startswith("Error") or c.startswith("File not found") for c in chunks)


def test_oversized_file_placeholder_is_not_sent_as_content(tmp_path):
    big = tmp_path / "big.py"
    big.write_text("x = 1\n" * (MAX_FILE_SIZE // 6 + 10), encoding="utf-8")

    chunks = extract_file_content(str(big))

    assert chunks, "expected a placeholder chunk"
    assert not _is_treated_as_valid_content(chunks), (
        f"oversized-file placeholder was treated as real content: {chunks}"
    )
