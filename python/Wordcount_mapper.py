# Mapper code (Wordcount_mapper.py)
import sys
import string

for line in sys.stdin:
    line = line.strip()
    
    # Remove punctuation, including double quotes
    line = line.translate(str.maketrans("", "", string.punctuation))
    
    # Convert to lowercase
    line = line.lower()
    
    # Tokenize the line into words
    words = line.split()
    for word in words:
        # Emit key-value pairs (word, 1)
        print(f"{word}\t1")
