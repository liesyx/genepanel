import os
import re

# Get the current directory
pwd = os.getcwd()

# Find HTML files
html_files = []
for root, dirs, files in os.walk(pwd):
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

# Process HTML files
output_lines = []
for html_file in html_files:
    with open(html_file, "r") as f:
        content = f.read()
        
        # Extract total_seq
        total_seq_match = re.search(r'<td>Total Sequences<\/td>.*<td>Sequences flagged as poor quality<\/td>', content, re.DOTALL)
        if total_seq_match:
            total_seq_match = re.search(r'<td>Total Sequences<\/td><td>([0-9-]+)<\/td>', total_seq_match.group(0))
            if total_seq_match:
                total_seq = total_seq_match.group(1)
            else:
                total_seq = ""
        else:
            total_seq = ""

        # Extract max_seq
        max_seq_match = re.search(r'<td>Sequence length<\/td>.*<td>%GC<\/td>', content, re.DOTALL)
        if max_seq_match:
            max_seq_match = re.findall(r'<td>Sequence length<\/td><td>([0-9-]+)<\/td>', max_seq_match.group(0))
            if max_seq_match:
                max_seq = max(max_seq_match, key=lambda x: int(x))
            else:
                max_seq = ""
        else:
            max_seq = ""

        # Extract name_seq
        name_seq_match = re.search(r'<td>Filename<\/td>.*<td>File type<\/td>', content, re.DOTALL)
        if name_seq_match:
            name_seq_match = re.search(r'<td>Filename<\/td><td>(.*?)<\/td>', name_seq_match.group(0))
            if name_seq_match:
                name_seq = name_seq_match.group(1)
            else:
                name_seq = ""
        else:
            name_seq = ""

        # Extract adapter_seq
        adapter_seq_match = re.search(r'alt="([^"]*)"/>Adapter', content)
        if adapter_seq_match:
            adapter_seq = adapter_seq_match.group(1)
        else:
            adapter_seq = ""

        # Append the result to the output_lines
        output_lines.append(f"{name_seq}  {max_seq} {total_seq} {adapter_seq}")

# Write the results to output.txt
with open("output.txt", "w") as f:
    f.write("\n".join(output_lines))

# Remove duplicate lines using AWK
os.system("awk '!seen[$0]++' output.txt > output_awk.txt")

# Remove lines containing "R2" using sed
os.system("sed '/R2/d' output_awk.txt > output_awk_remove_lap.txt")
