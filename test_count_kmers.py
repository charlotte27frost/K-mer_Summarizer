#!/usr/bin/env python3
# Testing the count_kmers function

import pytest
from summarize_kmer import count_kmers

def test_count_kmers_basic():
    sequences = ["ACGTACG"]
    k = 3
    result = count_kmers(sequences, k)
    
    expected = {
        "ACG": {"count": 2, "next": {"T": 1, "END": 1}},
        "CGT": {"count": 1, "next": {"A": 1}},
        "GTA": {"count": 1, "next": {"C": 1}},
        "TAC": {"count": 1, "next": {"G": 1}},
    }
    assert result == expected

def test_count_kmers_empty():
    assert count_kmers([], 3) == {}

def test_sequence_shorter_than_k():
    sequences = ["AG"]
    k = 3
    assert count_kmers(sequences, k) == {}

def test_case_normalization():
    sequences = ["acgTACg"]
    k = 3
    # simulate normalization that read_sequences would do
    sequences = [s.upper() for s in sequences]
    result = count_kmers(sequences, k)
    expected = {
        "ACG": {"count": 2, "next": {"T": 1, "END": 1}},
        "CGT": {"count": 1, "next": {"A": 1}},
        "GTA": {"count": 1, "next": {"C": 1}},
        "TAC": {"count": 1, "next": {"G": 1}},
    }
    assert result == expected

    
def test_count_kmers_multiple_sequences():
    sequences = ["ACGT", "ACGA"]
    k = 2
    expected = {
        "AC": {"count": 2, "next": {"G": 2}},
        "CG": {"count": 2, "next": {"T": 1, "A": 1}},
        "GT": {"count": 1, "next": {"END": 1}},
        "GA": {"count": 1, "next": {"END": 1}},
    }
    result = count_kmers(sequences, k)
    assert result == expected