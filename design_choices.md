# Design Choices
This document outlines the design decisions and implementation details behind the `summarize_kmer.py` script, with a focus on data structures, edge cases, and correctness.

## Data Structures
The script uses a **nested dictionary** structure to store k-mers and the characters that follow them. This design allows for efficient lookups, updates, and clear organization of both the frequency and context of each k-mer.

#### Main Structure Overview
Each k-mer is stored as a key in a dictionary. Its value is another dictionary that tracks:

- `count`: How many times the k-mer appears in the entire input.
- `next`: A dictionary of characters that immediately follow this k-mer, along with their respective counts.

#### Example Structure
```python
{
    'ACG': {
        'count': 3,
        'next': {
            'T': 2,
            'END': 1
        }
    },
    'GTA': {
        'count': 1,
        'next': {
            'C': 1
        }
    }
}
```
In this example:
- 'ACG' appears 3 times in total.
    - It's followed by 'T' twice.
    - Once, it appears at the end of a sequence and is followed by 'END'.
- 'GTA' appears once and is followed by 'C'.

#### Nested Dictionaries
A nested dictionary offers greater efficiency, reliability, and extensibility.
 - **Efficiency:** Access and update operations are constant time (O(1)) for each k-mer and next character.
 - **Readability:** Separating total count and next-character context makes the structure easier to reason about.
 - **Extensibility:** If future needs arise (e.g., storing position info or probabilities), additional keys can be added without breaking the structure.

#### Alternative Considerations (and Why They Weren’t Used)
- **Flat list of tuples:** (kmer, next_char) would require multiple passes for counting and grouping, increasing time complexity.
- **Defaultdict chaining:** Although collections.defaultdict could simplify the structure, explicit dictionaries were chosen for clarity and control over how values are initialized and updated.
- **Counters or pandas:** Counters are good for flat frequency counts but less suited for hierarchical context like next characters. Pandas is overkill here given the simplicity and size of the data being tracked. 
The nested dictionary strikes a balance between performance, simplicity, and flexibility.

## Handling Edge Cases
The script is designed to handle several edge cases that could arise:
**Sequences shorter than `k`**
These are skipped entirely, as no valid k-mers can be extracted

**Terminal k-mers**
If a k-mer is at the end of a sequence with no character following it, the next character is recorded as `"END"`

**Sequences exactly equal to `k`**
A single k-mer is extracted and paired with the special `"END"` marker to indicate no following character.

**Empty sequences**
These are ignored automatically during processing--no k-mers are extracted, and no errors are raised.

**Single-nucleotide k-mers (`k=1`)**
Handed like any other k value.  Each nucleotide is paried with the next one, and the last nucleotide is followed by `"END"`.

**Multiple contigs in a file**
Each contig is treated independently--no k-mers are extracted across contig boundaries

**FASTA headers**
Lines starting with `>` are used to identify new contigs and are not included in processing

## Avoiding Overcounting or Missing Context
The script uses a **sliding window approach** to move through each sequence and extract `(k-mer, next char)` pairs. Specific strategies to ensure accurate counting include:

- **One k-mer per valid position:** No overlapping counts or repeated indexing errors.
- **Terminal k-mers are not ignored:** If a k-mer ends the sequence, 'END' is recorded instead of skipping it.
- **Each sequence is processed independently:** Prevents contamination of context between contigs in a multi-sequence file.
- **Whitespace and lowercase letters are removed:** Ensures consistent parsing.

These combined measures ensure that:
- Every k-mer is counted exactly once per appearance.
- Context is preserved with high fidelity.
- The results can be reliably used for downstream analysis (e.g., prediction models, motif discovery, compression).