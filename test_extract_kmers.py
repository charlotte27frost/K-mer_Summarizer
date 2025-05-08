#!/usr/bin/env python3
# Testing the extract_kmers function

import pytest
from summarize_kmer import extract_kmers

# Basic test case where k = 3
def test_basic_case():
    sequence = "ACGTACGT"
    k = 3
    expected = [("ACG", "T"), ("CGT", "A"), ("GTA", "C"), ("TAC", "G"), ("ACG", "T"), ("CGT", "END")]
    assert extract_kmers(sequence, k) == expected

# Edge case where sequence is shorter than k
def test_short_sequence():
    sequence = "ACG"
    k = 4
    expected = []  # No k-mers can be extracted if sequence is shorter than k
    assert extract_kmers(sequence, k) == expected

# Test case where k = 1
def test_k_equals_1():
    sequence = "ACGT"
    k = 1
    expected = [("A", "C"), ("C", "G"), ("G", "T"), ("T", "END")]
    assert extract_kmers(sequence, k) == expected

# Test case with repeated characters
def test_repeated_characters():
    sequence = "AAAAAA"
    k = 2
    expected = [("AA", "A"), ("AA", "A"), ("AA", "A"), ("AA", "A"), ("AA", "END")]
    assert extract_kmers(sequence, k) == expected

# Test case where k = length of sequence, should give one k-mer with no next character
def test_k_equals_length():
    sequence = "AGCT"
    k = 4
    expected = [("AGCT", "END")]
    assert extract_kmers(sequence, k) == expected

# Test case with a sequence of length 1
def test_single_character_sequence():
    sequence = "A"
    k = 1
    expected = [("A", "END")]
    assert extract_kmers(sequence, k) == expected