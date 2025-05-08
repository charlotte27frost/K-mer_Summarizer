# K-mer Summarizer
The K-mer summarizer is a command-line Python script for counting k-mers and collecting their subsequent nucleotides in a genome sequence.
------------
## Features
- Parses sequences from FASTA-formatted files
- Extracts all possible k-mers of a given length `k`
- Tracks how often each k-mer is followed by a specific nucleotide
- Includes terminal k-mers (e.g., `ACG` at the end of a sequence)
- Outputs results to a text file in a clear format
- Includes a suite of Pytest unit tests for reliability
------------
## Project Structure
```
kmer-summarizer/
│
├── design_choices.md       # Document elaborating on data usage, edge cases, and efficiency
├── input.fa                # Example input file
├── output.txt              # Example output file created by script
├── README.md               # Project documentation
├── summarize_kmer.py       # Main script for parsing, counting, and output
├── test_count_kmer.py      # Tests the count_kmer function in the main script
├── test_extract_kmer.py    # Tests the extract_kmer function in the main script
├── test_main.py            # Tests the main function in the main script
├── test_read_sequences.py  # Tests the read_sequences function in the main script
└── test_write_output.py    # Tests the write_output function in the main script
```
------------
## Usage
### 1. Requirements
- Python 3.6+
- pytest (https://docs.pytest.org/en/stable/) for running tests

Install pytest if not already installed:
```bash
pip install pytest
```
### 2. Running the Script
The script is run in the command line using python as shown below.  Specify the path to the input .fa file, the desired k length, and the name of the desired output file, which will populate in the user's current directory.

```bash
python summarize_kmer.py input.fa 3 output.txt
```
Arguments:
    - input.fa: Path to the FASTA file with sequences
    - 3: Value of k (must be a positive integer)
    - output.txt: Path to the output file

### 3. Output Format
Each line in the output will take on the following format:

```vbnet
ACG:2, next T:1, END:1
```
This means the k-mer ACG appears 2 times, once followed by T, and once with no character after (END).

------------
## Design Decisions
### 1. Data Structures
K-mer data is stored using a nested dictionary:

```python
{
    'ACG': {
        'count': 2,
        'next': {
            'T': 1,
            'END': 1
        }
    }
}
```

- The outer dictionary uses each unique k-mer as a key.
- Each k-mer maps to a sub-dictionary:
    - 'count': the total number of times the k-mer appears.
    - 'next': a dictionary of the characters that immediately follow this k-mer and how many times each occurred.
- This structure makes it easy to accumulate counts and organize the relationship between k-mers and their context.

### 2. Handling Edge Cases
- Edge cases handled include:
    - Sequences shorter than k: These are skipped because they cannot produce valid k-mers.
    - K-mer at the very end of a sequence: If there's no next character, we explicitly record 'END' as the following character.
    - k == 1 or k == sequence length: Supported with consistent handling of the terminal case.
    - Mixed-case input: Automatically converts sequencing to uppercase.
- This ensures no information is lost and results are predictable across sequence lengths.

### 3. Preventing Overcounting and Missed Context
- To avoid losing or replicating data:
    - Sliding window logic is used to extract k-mers and their next characters.
    - Only one k-mer is recorded per position, and each has one "next" character.
    - Whitespace and lowercase letters are removed to ensure consistent parsing.
    - The last valid k-mer (if it's exactly at the end of the sequence) is followed by 'END' rather than being skipped or counted ambiguously.
    - The code checks for each sequence individually, avoiding cross-sequence leakage.
- These decisions sought to ensure accurate k-mer counts and consistent tracking of next-character context without redundancy.

### 4. Handling Multiple Contigs
- The script is designed to parse multiple sequences (or contigs) from a single FASTA file.
- Each contig is treated independently — k-mers are only extracted within each sequence, and never across sequence boundaries.
- This is achieved by detecting FASTA headers (lines starting with >), and splitting the input into individual sequences.
- By resetting the current sequence on each header, the script ensures no "bleed-over" of context between contigs.
------------
## Testing
Scripts starting with the word "test" can be run to test the functionality of the code and ensure it is running as expected.

Run the entire set of tests with:
```bash
pytest
```

Alternatively, tests can be run individually using:
```bash
pytest test_extract_kmers.py
pytest test_summarize_kmer.py
```
------------
## Example
Consider the following arguments using the summarize_kmer script:
```bash
python summarize_kmer.py input.fa 3 output.txt
```

Given this input sequence in input.fa:
```fa
>sequence1
AATGCA
>sequence2
TTACGA
>sequence3
CGTACGT
```
And while using k = 3, the script extracts all 3-mers from each sequence along with the character that follows them. If a 3-mer is the last possible one in a sequence (i.e. there's no next character), it uses "END" to mark the terminal k-mer.

Thus, with k = 3, the output, which would populate in output.txt, would be:
```vbnet
AAC:1, next G:1
AAT:1, next G:1
ACG:2, next A:1, next T:1
ATG:1, next C:1
CGA:1, next END:1
CGT:2, next A:1, next END:1
GCA:1, next END:1
GTA:1, next C:1
GTA:1, next C:1
TAC:2, next G:2
TGC:1, next A:1
TTA:1, next C:1
```