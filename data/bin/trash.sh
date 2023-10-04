          if [ -f "YES_PASS_workflow2_.txt" ]; then
            bwa mem ${params.wholegenehg38_bed} ${reads_1} ${reads_2} | samtools view -S -b > "${name}.bam"
          fi

          if [ -f "Adapter_no_clear_.txt" ]; then
            trimmomatic PE -phred33 ${reads[0]} ${reads[1]} \
              "${reads[0].baseName}_trimmed.fastq" "${sample_name}_unpaired_1.fq" \
              "${reads[1].baseName}_trimmed.fastq" "${sample_name}_unpaired_2.fq" \
              ILLUMINACLIP:${adapter_dir_}:2:30:10 LEADING:5 TRAILING:5 SLIDINGWINDOW:4:30 MINLEN:70 AVGQUAL:25
            bwa mem ${params.wholegenehg38_bed} "${reads[0].baseName}_trimmed.fastq" "${reads[1].baseName}_trimmed.fastq" | samtools view -S -b > "${name}.bam"
          fi