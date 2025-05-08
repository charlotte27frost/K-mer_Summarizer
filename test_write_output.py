#!/usr/bin/env python3
# Testing the write_output function

import pytest
from summarize_kmer import write_output

def test_write_output_custom_format(tmp_path):
    # Input dictionary
    kmer_counts = {
        "AA": {"count": 2, "next": {"A": 1, "T": 1}},
        "AT": {"count": 1, "next": {"G": 1}},
    }

    # Output file path
    output_file = tmp_path / "out.txt"

    # Run the function
    write_output(kmer_counts, output_file)

    # Read and check file contents
    result = output_file.read_text().strip().splitlines()
    expected = [
        "AA:2, next A:1, T:1",
        "AT:1, next G:1"
    ]
    assert result == expected