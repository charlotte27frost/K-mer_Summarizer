#!/usr/bin/env python3
# Testing the main function

import sys
import pytest
from summarize_kmer import main

def test_main_function(tmp_path, monkeypatch):
    # Prepare a temporary input FASTA-like file
    input_content = """>seq1
ACGTA
>seq2
ACGTT
"""
    input_file = tmp_path / "input.txt"
    input_file.write_text(input_content)

    # Prepare a path for output file
    output_file = tmp_path / "output.txt"

    # Mock sys.argv to simulate command-line arguments
    monkeypatch.setattr(sys, 'argv', [
        'summarize_kmer.py',         # fake script name
        str(input_file),             # input file
        '3',                         # k-mer size
        str(output_file)             # output file
    ])

    # Call main function
    main()

    # Read and check output
    output = output_file.read_text().strip().splitlines()
    expected_lines = [
        "ACG:2, next T:2",
        "CGT:2, next A:1, T:1",
        "GTA:1, next :1",
        "GTT:1, next :1",
        "TAC:1, next :1",
    ]
   
    # Flexible assertion: check key expected patterns
    assert "ACG:2, next T:2" in output
    assert "CGT:2, next A:1, T:1" in output
    
# Test the function with a correct k and proper input/output files
def test_main_valid_run(tmp_path, monkeypatch):
    # Prepare input and output file paths
    input_file = tmp_path / "input.fasta"
    output_file = tmp_path / "output.txt"

    # Create a small input sequence file
    input_file.write_text(">seq1\nAATGCA\n")

    # Set command-line arguments: script name, input path, k=2, output path
    test_args = ["script_name", str(input_file), "2", str(output_file)]
    monkeypatch.setattr(sys, "argv", test_args)

    # Run the main function
    main()

    # Read the output and check if the results match expected content
    output = output_file.read_text().strip().splitlines()
   
    # Check that the expected k-mers and next characters are in the output
    assert any(line.startswith("AA:1, next T:1") for line in output)
    assert any(line.startswith("AT:1, next G:1") for line in output)

# Test when k <= 0
def test_k_less_than_or_equal_to_zero(monkeypatch):
    # Mock the read_sequences function to avoid file reading
    monkeypatch.setattr('summarize_kmer.read_sequences', lambda x: [])

    # Set command-line args with k <= 0
    test_args = ["script_name", "dummy.txt", "0", "out.txt"]
    monkeypatch.setattr(sys, "argv", test_args)

    # Ensure SystemExit is raised and message is correct
    with pytest.raises(SystemExit) as e:
        main()
    
    # Check if the error message contains "k-mer length must be a positive integer"
    assert "The k-mer length must be a positive integer" in str(e.value)

# Test when k is larger than the sequences
def test_k_larger_than_all_sequences(tmp_path, monkeypatch):
    input_file = tmp_path / "input.txt"
    input_file.write_text(">seq1\nATG\n>seq2\nCCG\n")
    output_file = tmp_path / "output.txt"

    # Set command-line args with k larger than sequence length
    test_args = ["script_name", str(input_file), "5", str(output_file)]
    monkeypatch.setattr(sys, "argv", test_args)

    # Ensure SystemExit is raised and message is correct
    with pytest.raises(SystemExit) as e:
        main()
    assert "sequences are shorter than or equal to k" in str(e.value)