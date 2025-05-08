#!/usr/bin/env python3
# Testing the read_sequences function

import pytest
from summarize_kmer import read_sequences

def test_read_sequences_basic(tmp_path):
    content = """>sequence_1
acgtacgt
>sequence_2
ggtaac
ttac
"""
    test_file = tmp_path / "test_input.txt"
    test_file.write_text(content)
    expected = ["ACGTACGT", "GGTAACTTAC"]
    assert read_sequences(test_file) == expected

def test_empty_file(tmp_path):
    test_file = tmp_path / "empty.txt"
    test_file.write_text("")
    assert read_sequences(test_file) == []

def test_only_headers(tmp_path):
    content = """>seq1
>seq2
>seq3
"""
    test_file = tmp_path / "headers_only.txt"
    test_file.write_text(content)
    assert read_sequences(test_file) == []

def test_case_and_whitespace(tmp_path):
    content = """
>seq1
ac g T
>seq2
Gta aC
"""
    test_file = tmp_path / "mixed_case.txt"
    test_file.write_text(content)
    expected = ["ACGT", "GTAAC"]
    assert read_sequences(test_file) == expected

def test_no_headers(tmp_path):
    content = """
atgc
ccatg
"""
    test_file = tmp_path / "no_headers.txt"
    test_file.write_text(content)
    expected = expected = ["ATGCCCATG"]
    assert read_sequences(test_file) == expected