#!/usr/bin/env python
import pandas as pd
import sys
import os
import re
name = sys.argv[1]

def parse_lines(lines):
    total_seqs = {}
    comparison_table = []

    for line in lines[:]:
        columns = line.strip().split()

        file_name = columns[0]
        total_seq = int(columns[2])
        total_seqs[file_name] = total_seq

    for line in lines[:]:

        columns = line.strip().split()
        file_name = columns[0]
        # print(file_name)
        if "trimmed" in file_name:
            original_file = re.sub(r'_trimmed', r'', file_name)
            original_total_seq = total_seqs[original_file]
            trimmed_total_seq = int(columns[2])
            reads_count = int(columns[1])
            adapter = columns[3]
            trimmed_count = original_total_seq - trimmed_total_seq
            trimmed_per = round((trimmed_total_seq / original_total_seq) * 100, 3)
            if trimmed_per >= 50 and reads_count > 70 and adapter == "[OK]" and original_total_seq >1000:
                status = "PASS"
            else:
                status = "NOT PASS"
            comparison_table.append((original_file, original_total_seq, trimmed_total_seq, trimmed_count, trimmed_per, reads_count, adapter, status))

    return comparison_table

def save_result(result, output_file_path):
    with open(output_file_path, 'w') as output_file:
        output_file.write("Original_File\tTotal_Seq\tTrimmed_Seq\tTrimmed_Count\tTrimmed_per\tTrimmed_reads\tAdapter\tSTATUS\n")
        for item in result:
            output_file.write('\t'.join(map(str, item)) + '\n')
    
    # Kiểm tra các điều kiện và ghi các tệp kết quả phụ
    statuses = [item[7] for item in result]
    
    if all(status == "PASS" for status in statuses):
        with open("YES_PASS_workflow2_.txt", "w") as pass_file:
            pass_file.write("PASS workflow 2.")
    if all(status == "NOT PASS" for status in statuses):
        if any("[OK]" not in item[6] for item in result) or any("[OK]" in item[6] for item in result):
            with open("NO_PASS_.txt", "w") as pass_file:
                pass_file.write("File của bạn không đủ chất lượng.")
    if any("[OK]" not in item[6] for item in result) and all(status == "NOT PASS" for status in statuses):
        with open("Adapter_no_clear_.txt", "w") as adapter_noclear_file:
            adapter_noclear_file.write("File còn Adapter.")


if __name__ == "__main__":
    with open(f'{name}_output_clear.txt', 'r') as file:
        lines = file.readlines()

    comparison_table = parse_lines(lines)
    comparison_table.sort(key=lambda x: x[0])
    output_file_path_1 = f"{name}_comparison_result.txt"
    save_result(comparison_table, output_file_path_1)

    output_file_path = f"{name}_comparison1.txt"
    with open(output_file_path, "w") as output_file:
        # Mở tệp văn bản để đọc và ghi
        input_file_path = f"{name}_comparison_result.txt"
        with open(input_file_path, "r") as input_file:
            first_line = input_file.readline()  # Đọc dòng đầu tiên
            output_file.write(first_line)  # Ghi dòng đầu tiên vào tệp mới

            for line in input_file:
                # Nếu dòng không bắt đầu bằng {name}, thì ghi vào tệp mới
                if line.startswith(name):
                    output_file.write(line)
