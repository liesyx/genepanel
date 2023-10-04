#!/usr/bin/env python
import vcfpy
import sys

name = sys.argv[1]
snp_file = sys.argv[2]
indel_file = sys.argv[3]
bed_file = sys.argv[4]
# bed_file_path= sys.argv[4]
# name = "S26"
# snp_file = "/home/dungnguyen/genepanel/results/clean_snp_indels/S26_output_raw_snps_filtered_.vcf"
# indel_file = "/home/dungnguyen/genepanel/results/clean_snp_indels/S26_output_raw_indels_filtered_.vcf"
bed_file_path = bed_file
# extract data form bed file
def filter_vcf_by_bed(vcf_file, bed_ranges):
    filtered_records = []

    output_vcf = vcfpy.Reader.from_path(vcf_file)

    for record in output_vcf:
        pos = record.POS
        if any(start <= pos <= end for (_, start, end) in bed_ranges):
            filtered_records.append(record)

    return filtered_records

# extract data 
def write_vcf(records, output_file, header):
    with open(output_file, 'w') as outfile:
        writer = vcfpy.Writer(outfile, header)
        for record in records:
            writer.write_record(record)

bed_ranges = []
with open(bed_file_path, "r") as bed_file:
    for line in bed_file:
        parts = line.strip().split("\t")
        chrom, start, end, _, _ = parts
        bed_ranges.append((chrom, int(start), int(end)))
# lọc 
snp_filtered_records = filter_vcf_by_bed(snp_file, bed_ranges)
indel_filtered_records = filter_vcf_by_bed(indel_file, bed_ranges)
output_vcf = vcfpy.Reader.from_path(snp_file)  # Or use indel_file, both should have the same header
snp_output = f"{name}_snp_bed_filter.vcf"
indel_output = f"{name}_indel_bed_filter.vcf"
write_vcf(snp_filtered_records, snp_output, output_vcf.header)
write_vcf(indel_filtered_records, indel_output, output_vcf.header)

# gộp file
merged_file = f"{name}_bed_file_filter.vcf"
with open(merged_file, 'w') as outfile:
    with open(snp_output) as snp_file:
        for line in snp_file:
            if line.startswith('#'):
                outfile.write(line)
    
    with open(indel_output) as indel_file:
        for line in indel_file:
            if not line.startswith('#'):
                outfile.write(line)
    
    with open(snp_output) as indel_file:
        lines = indel_file.readlines()
        for line in lines:
            if not line.startswith('#'):
                outfile.write(line)
    
    # Kiểm tra xem tất cả các dòng trong tệp bắt đầu bằng '#'
    all_lines_start_with_hash = all(line.startswith('#') for line in lines)
    
    if all_lines_start_with_hash:
        # Nếu tất cả bắt đầu bằng '#', tạo ra tệp no_anovar.txt
        with open('no_anovar.txt', 'w') as no_anovar_file:
            no_anovar_file.writelines(lines)
    else:
        # Nếu không, tạo ra tệp yes_anovar.txt
        with open('yes_anovar.txt', 'w') as yes_anovar_file:
            yes_anovar_file.writelines(lines)
    
    # if all_lines_start_with_hash:
    #     # Nếu tất cả bắt đầu bằng '#', tạo ra tệp no_anovar.txt
    #     with open("no_anovar.txt", "w") as no_anovar_file:
    #         no_anovar_file.writelines(["no\n"] + lines) # Thêm "no" vào đầu tệp
    # else:
    #     # Nếu không, tạo ra tệp yes_anovar.txt
    #     with open("yes_anovar.txt", "w") as yes_anovar_file:
    #         yes_anovar_file.writelines(["yes\n"] + lines) # Thêm "yes" vào đầu tệp