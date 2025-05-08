#!/usr/bin/env python3

import sys
import argparse

def read_sequences(file_path):
    """
    The function processes the file line by line:
        - Lines starting with `>` are considered FASTA headers and signal the start of a new sequence.
        - Lines that are not headers are added to the current sequence.
        - Sequences are split by headers (each header starts a new sequence).
    After processing, all sequences are returned as a list of strings, where each string represents
    a single, combined sequence in uppercase, with any whitespace removed.
      
    Argument:  path to the input file
    Returns:  list of cleaned sequence strings
    """
    sequences = []                                  # This will hold the cleaned sequences
    current_seq = []                                # Temporary storage to build a sequence (useful for multi-line sequences)
    
    # Append the last sequence after the loop
    with open(file_path, 'r') as file:
         for line in file:
            line = line.strip()                     # Removes whitespace
            if line.startswith('>'):                # Headers starting with > indicates the start of a new sequence in FASTA files      
                if current_seq:
                    # If there is an ongoing sequence being built, join it and add it to the list                    
                    sequences.append(''.join(current_seq).upper())  # Normalize to uppercase
                    current_seq = []                                # Reset the current sequence for the next sequence
            elif line:
                current_seq.append(line.replace(' ', ''))           # Append current sequence and remove spaces *inside* the line

    # Append the last sequence after the loop
    if current_seq:
        sequences.append(''.join(current_seq).upper())
    return sequences

def extract_kmers(sequence, k):
    """
    Extracts k-mers and their subsequent character from a sequence.
        - If there is a character following the k-mer, include it in the pair.
        - If there is no following character (i.e., it's a terminal k-mer), record it with None.
      
    Argument:
        sequence (str): The genome sequence.
        k (int): Length of each k-mer.
    Returns: list of (k-mer, following character) pairs.
    """
    kmers = []              
    # Loop through each position in the sequence where we can extract a full k-mer    
    for i in range(len(sequence) - k):   # Loop iterates through the length of sequence minus k
        kmer = sequence[i:i+k]           # Extract k-mer
        next_char = sequence[i+k]        # Get character after k-mer
        kmers.append((kmer, next_char))  # Append the k-mer and next character as a pair
    
    # Append the final terminal k-mer if it's long enough, with no next character
    if len(sequence) >= k:
        final_kmer = sequence[-k:]
        kmers.append((final_kmer, "END"))
            
    return kmers
           
def count_kmers(sequences, k):
    """
    Counts how often each k-mer appears, and how often each k-mer is followed by a specific character.  
    Includes terminal k-mers that do not have a subsequent character.
        
    Argument:
        sequences (List[str]): List of genome sequences.
        k (int): Length of each k-mer.
    Returns:
        Dictionary of k-mer counts and their next nucleotide distributions.
    """
    kmer_counts = {}   # Initializes empty dictionary
       
    # For each sequence, extract all (k-mer, next char) pairs
    for seq in sequences:
        for kmer, next_char in extract_kmers(seq, k):
            # Add the k-mer entry if it doesn't exist
            if kmer not in kmer_counts:                        # If the k-mer has not been added yet, initialize it in dictionary
                kmer_counts[kmer] = {'count': 0, 'next': {}}   # along with a count of 0 and an associated dictionary of next sequences
            kmer_counts[kmer]['count'] += 1                                                        
            # Increase total k-mer count by 1
            label = next_char if next_char is not None else 'END' # Use 'END' to represent terminal k-mers (with no next character) 
            kmer_counts[kmer]['next'][next_char] = kmer_counts[kmer]['next'].get(next_char, 0) + 1  # Increase count for the next character
    return kmer_counts

def write_output(kmer_counts, output_file):
    """
    Writes the k-mer counts and next character frequencies to a file.
        Argument:
            kmer_counts (dict): The dictionary returned by count_kmers().
            output_file (str): Path where output will be saved.
    """
    with open(output_file, 'w') as f:                           # Opens the output file to write in
        for kmer, data in sorted(kmer_counts.items()):          # Sorts the k-mer
            next_counts = ', '.join(                            # Sorts the next character
                f'{char if char is not None else "END"}:{count}' 
                for char, count in sorted(data['next'].items(), key=lambda x: ("" if x[0] is None else x[0]))
            )
            f.write(f"{kmer}:{data['count']}, next {next_counts}\n") # Write one line per k-mer

def main():
    """
    Main function that sets up command-line argument parsing and runs the pipeline.
    """
    # Set up a command-line parser to accept arguments
    parser = argparse.ArgumentParser(
        description="Count k-mers and following character frequencies from genome sequences."
    )
    
    # Define expected command-line arguments
    parser.add_argument('input_file', type=str, help='Path to input file containing genome fragments')
    parser.add_argument('k', type=int, help='Length of k-mers to extract')
    parser.add_argument('output_file', type=str, help='Path to output file to write results')

    # Parse the command-line arguments
    args = parser.parse_args()

    sequences = read_sequences(args.input_file)    # Load and clean sequences from input file
    kmer_counts = count_kmers(sequences, args.k)   # Count k-mer frequencies and their following characters
    write_output(kmer_counts, args.output_file)    # Write k-mer pair statistics to output file

    # Input validation
    # If user enters a negative number
    if args.k <= 0:                 
        sys.exit("Error: The k-mer length must be a positive integer.")
    # If user enters a k larger than the sequence
    if all(len(seq) <= args.k for seq in sequences):
        sys.exit("Error: All sequences are shorter than or equal to k. Cannot extract any k-mers.")
        
# Runs the pipeline
if __name__ == '__main__':
    main()