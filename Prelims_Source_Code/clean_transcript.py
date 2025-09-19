import re
from pathlib import Path

input_path = Path("transcribed.txt")
output_path = Path("cleaned_transcript.txt")

# allow lowercase letters, spaces, and full stops
keep_re = re.compile(r'[^a-z. ]+')

def clean_transcript_text(text: str) -> str:
    s = text.lower()
    s = keep_re.sub(' ', s)   # remove everything except a-z, space, and .
    s = re.sub(r'\s+', ' ', s).strip()  # collapse spaces
    return s

with open(input_path, 'r', encoding='utf-8') as fin, \
     open(output_path, 'w', encoding='utf-8') as fout:
    for line in fin:
        if line.strip() == '':
            fout.write('\n')
            continue

        if ':' in line:
            filename_part, rest = line.split(':', 1)
            cleaned = clean_transcript_text(rest)
            fout.write(f"{filename_part}:{' ' if cleaned else ''}{cleaned}\n")
        else:
            cleaned = clean_transcript_text(line)
            fout.write(f"{cleaned}\n")

print(f"Cleaned file written to: {output_path}")