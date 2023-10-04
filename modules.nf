// Module FASTQC
process FASTQC {
  publishDir "${params.outdir}/$id_file", mode: 'copy'
  tag "FASTQC on ${id_file}"
    cpus 15
  input:
    tuple val(id_file), path(reads)
  output:
    val(id_file)
    path "fastqc_${id_file}_logs"
  script:
    """
    mkdir fastqc_${id_file}_logs
    fastqc -o fastqc_${id_file}_logs -f fastq -q ${reads}
    """
}

// Module FASTQC cho các tập tin cặp
process FASTQC_trimnomatic {  
  publishDir "${params.outdir}/$id_file", mode: 'copy'
  tag "FASTQC on ${id_file}"
    cpus 15
  input:
    val(id_file)
    path(reads1)
    path(reads2)
  output:
    val(id_file)
    path "fastqc_${id_file}_logs_trimmed"
  script:
    """
    mkdir fastqc_${id_file}_logs_trimmed
    fastqc -o fastqc_${id_file}_logs_trimmed -f fastq -q ${reads1} ${reads2}
    """
}

// Module Trimmomatic
process trimmomatic {
  publishDir "${params.outdir}/${sample_name}", mode: 'copy'
  input:
    tuple val(sample_name), path(reads)
  output:
    val(sample_name)
    path "${reads[0].baseName}_trimmed.fastq"
    path "${reads[1].baseName}_trimmed.fastq"
  script:
    """
    trimmomatic PE -phred33 ${reads[0]} ${reads[1]} \
    ${reads[0].baseName}_trimmed.fastq ${sample_name}_unpaired_1.fq \
    ${reads[1].baseName}_trimmed.fastq ${sample_name}_unpaired_2.fq \
    LEADING:5 TRAILING:5 SLIDINGWINDOW:4:30 MINLEN:70 AVGQUAL:25
    """
}

// Module Trimmomatic với cắt adapter
process trimmomatic_adapter_cut {
  publishDir "${params.outdir}/${sample_name}", mode: 'copy'
  input:
    tuple val(sample_name), path(reads)
  output:
    val(sample_name)
    path "${reads[0].baseName}_trimmed.fastq"
    path "${reads[1].baseName}_trimmed.fastq"
  script:
    """
    trimmomatic PE -phred33 ${reads[0]} ${reads[1]} \
    ${reads[0].baseName}_trimmed.fastq ${sample_name}_unpaired_1.fq \
    ${reads[1].baseName}_trimmed.fastq ${sample_name}_unpaired_2.fq \
    ILLUMINACLIP:${params.adapter}:2:30:10 LEADING:5 TRAILING:5 SLIDINGWINDOW:4:30 MINLEN:70 AVGQUAL:25 
    """
}

// Module FASTQC_check_final
process FASTQC_check_final {
  publishDir "${params.outdir}/$name/check", mode: 'copy'
  publishDir "${params.outdir}/check", pattern: "*_result.txt"
  tag "FASTQC on ${name}"
    cpus 15
  input:
    // fastqc_output
    val(name)
    path(folder_fastqc)
    // fastqc_trimnomatic_out
    val(name1)
    path(folder_trimnomatic)
    // bash file
  output:
    path("*_.txt")
  script:
    """
    pwd=\$(pwd)
    cd $projectDir/${params.outdir}/${name}
    bash  $projectDir/data/bin/bash.sh ${params.outdir}
    python $projectDir/data/bin/fastqc_check.py ${name}
    mv *.txt \$pwd
    """
}


// Module bwa_map
process bwa_map {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  tag "BWA on $name"

  input:
    // trimnomatic
    val(name)
    path(reads_1)
    path(reads_2)
    // adapter
    path(adapter_dir_)

  // when:
    // check_txt.name == "YES_PASS_workflow2_.txt" || check_txt.name == "Adapter_no_clear_.txt"
  output:
    tuple val(name), path("${name}.bam")
  script:
    """
    bwa mem ${params.wholegenehg38_bed} ${reads_1} ${reads_2} | samtools view -S -b > "${name}.bam"
    """
}

// Module bamfile_sort
process bamfile_sort {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  tag "variant_calling on $reads"
  input:
    tuple val(name), path(reads)
  output:
    tuple val(name), path("sorted_${name}.bam")
  script:
    """

    samtools sort ${reads} -o sorted_${name}.bam
    """
}

// Module variant_calling_freebayes
process variant_calling_freebayes {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  tag "variant_calling on $bam"

  input:
    tuple val(name), path(bam)
  output:
    val(name)
    path "${name}_output.vcf"
  script:
    """
    freebayes -f ${params.wholegenehg38_bed} ${bam} > ${name}_output.vcf
    """
}

// Module Extract_SNPs_INDELS
process extract_SNPs_INDELS {
  tag "$vcf_file.baseName"
  publishDir "${params.outdir}/${name}", mode: 'copy'
  input:
    path genome
    path genome_fai
    path genome_dict
    val(name)
    path vcf_file
  output:
    val(name)
    path "${vcf_file.baseName}_raw_snps.vcf"
    path "${vcf_file.baseName}_raw_indels.vcf"
  script:
    """
     gatk SelectVariants -R ${genome} -V ${vcf_file} --select-type SNP -O ${vcf_file.baseName}_raw_snps.vcf
    gatk SelectVariants -R ${genome} -V ${vcf_file} --select-type INDEL -O ${vcf_file.baseName}_raw_indels.vcf
    """
}

// Module filter_variant
process filter_variant {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  input:
    path genome
    path genome_fai
    path genome_dict
    val(name)
    path raw_snps_vcf
    path raw_indels_vcf
  output:
    val(name)
    path "${raw_indels_vcf.baseName}_filtered.vcf"
    path "${raw_snps_vcf.baseName}_filtered.vcf"
  script:
    """

    gatk VariantFiltration \
      -R ${genome} \
      -V ${raw_snps_vcf} \
      -O ${raw_snps_vcf.baseName}_filtered.vcf \
      --filter-expression "AF < 0.2" --filter-name "AF5" \
      --filter-expression "DP < 100" --filter-name "DP10" \
      --filter-expression "QUAL < 25" --filter-name "QUAL25"

    gatk VariantFiltration \
      -R ${genome} \
      -V ${raw_indels_vcf} \
      -O ${raw_indels_vcf.baseName}_filtered.vcf \
      --filter-expression "AF < 0.2" --filter-name "AF5" \
      --filter-expression "DP < 100" --filter-name "DP10" \
      --filter-expression "QUAL < 30" --filter-name "QUAL30"
    """
}

// Module clean_snp_indels
process clean_snp_indels {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  input:
    val(name)
    path indels_filtered
    path snps_filtered
  output:
    val(name)
    path "${indels_filtered.baseName}_.vcf"
    path "${snps_filtered.baseName}_.vcf"
  script:
    """
    
    gatk SelectVariants \
      -V ${indels_filtered} \
      --exclude-filtered \
      -O ${indels_filtered.baseName}_.vcf

    gatk SelectVariants \
      -V ${snps_filtered} \
      --exclude-filtered \
      -O ${snps_filtered.baseName}_.vcf
    """
}

// Module bed_file
process bed_file {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  input:
    val(name)
    path(indel_file)
    path(snp_file)
  output:
    val(name)
    path "${name}_bed_file_filter.vcf"
    path("*_anovar.txt")
  script:
    """
    python $projectDir/data/bin/bed.py ${name} ${snp_file} ${indel_file} ${params.bed_file}
    """
}

// Module annovar_annotation
process annovar_annotation {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  input:
    val(name)
    path(vcf_file)
    path(check_anovar_txt)
  when:
    check_anovar_txt.name == "yes_anovar.txt" 
  output:
    val(name)
    path "${name}.hg38_multianno.txt"
  script:
    """
    $projectDir/data/annovar/annovar/table_annovar.pl ${vcf_file} ${params.humandb} \
    -buildver hg38 -out ${name} \
    -remove -protocol refGene,cytoBand,avsnp150,gnomad312_genome,cosmic70,clinvar_20221231,hrcr1 \
    -operation g,r,f,f,f,f,f \
    -nastring . -vcfinput -polish
    """
}
// perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb avsnp150 -buildver hg38 data/annovar/annovar/humandb
// perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb gnomad312_genome -buildver hg38 data/annovar/annovar/humandb
// perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb cosmic70 -buildver hg38 data/annovar/annovar/humandb

// refGene,
// cytoBand,

// // avsnp150
// // gnomad312_genome
// // cosmic70

// clinvar_20221231
// hrcr1

// Module Extract_data
process extract_data {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  input:
    val(name)
    path(annotation)
    path(MN_data)
  output:
    val(name)
    path "${name}_data.xlsx"
    path "${name}_data_final.xlsx"
    path "${name}_data_bienthegaybenh.xlsx"
  script:
    """
    python $baseDir/data/bin/extract_data.py ${name} ${annotation} ${MN_data}
    """
}

// Module FASTQC_check_final_all
process fASTQC_check_final_all {
  publishDir "${params.outdir}/$name/check", mode: 'copy'
    publishDir "${params.outdir}/check", pattern: "${name}_*"

  tag "FASTQC on ${name}"
  input:
    val(name)
    path(_data)
    path(_data_final)
    path(_data_bienthegaybenh)
  output:
    val(name)
    path(_data)
    path(_data_final)
    path(_data_bienthegaybenh)
    path("${name}_comparison1.txt")
    path("${name}_comparison_result.txt")
  script:
    """
    
    pwd=\$(pwd)
    cd $projectDir/${params.outdir}
    bash  $projectDir/data/bin/bash.sh ${name}
    python $projectDir/data/bin/fastqc_check.py ${name}
    mv ${name}*.txt \$pwd
    """
}

// Module html_file
process html_file {
  publishDir "${params.outdir}/${name}", mode: 'copy'
  publishDir "${params.outdir}/HTML_file", mode: 'copy'
  input:
    val(name)
    path(_data)
    path(_data_final)
    path(_data_bienthegaybenh)
    path(check_tung_file)
    path(data_bangtong)
  output:
    path "${name}_ketqua.html"
    path "ketqua_lap_rap.html"
  script:
    """
    python $baseDir/data/bin/creattinghtml_file.py \
      "${name}" \
      "${_data_bienthegaybenh}" \
      "${_data_final}" \
      "${data_bangtong}" \
      "${params.tenkhachang}" \
      "${params.ngaynhanmau}" \
      "${params.namsinh}" \
      "${params.goitinh}" \
      "${params.loaimau}" \
      "${params.ngaytraketqua}" \
      "${check_tung_file}"
    """
}
