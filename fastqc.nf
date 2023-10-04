#!/usr/bin/env nextflow

// Enable DSL2
nextflow.enable.dsl = 2

// Định nghĩa các tham số 
params.times = "20"
params.baseDir = '.'
params.wholegenehg38_bed = "$baseDir/data/hg38/hg38.fa"
params.genome_fai = "$baseDir/data/hg38/hg38.fa.fai"
params.genome_dict = "$baseDir/data/hg38/hg38.dict"
params.humandb = "$baseDir/data/annovar/annovar/humandb/"
params.tenkhachang = "dung"
params.author = params.tenkhachang
params.ngaynhanmau = "1/9/2023"
params.namsinh = "7/3/2002"
params.goitinh = "Nam"
params.loaimau = "dsDNA"
params.ngaytraketqua = "1/9/2023"
params.ten_du_an = "PMAB_Liesy_sang_itc"
params.reads = "$baseDir/data/test_read/*{1,2}.f*"
params.outdir = "ketqua/${params.author}/${params.ten_du_an}/${params.times}"
params.NM_data_ = "$baseDir/data/NM_DATA/NM_data.txt"
params.bed_file = "$baseDir/data/panelbed/Atila_hotspot_cancer_panel_bed_file.bed"
params.data_check = "$baseDir/$params.outdir/workflow1_check/data.txt"
params.adapter_dir = "$baseDir/data/NM_DATA/NM_data.txt"
params.nextflow_dir = "/home/dungnguyen/genepanel"

log.info """\
   GENE Panel ---------   P I P E L I N E    
   ===================================
   reads        : ${params.reads}
   BED file     : ${params.bed_file}
   Author       : ${params.author}
"""
.stripIndent()

// Include các module
include {
    FASTQC
    trimmomatic
    trimmomatic_adapter_cut
    FASTQC_trimnomatic
    FASTQC_check_final
    bwa_map
    bamfile_sort
    variant_calling_freebayes
    extract_SNPs_INDELS
    filter_variant
    clean_snp_indels
    bed_file
    annovar_annotation
    extract_data
    html_file
    fASTQC_check_final_all
} from "./modules.nf"

// Workflow
workflow {
    read_pairs_ch = Channel.fromFilePairs(params.reads)
    
    // Workflow 1: Kiểm tra và kiểm soát chất lượng
    FASTQC(read_pairs_ch)
    trimmomatic(read_pairs_ch)
    FASTQC_trimnomatic(trimmomatic.out)
    // FASTQC_check_final(FASTQC.out, FASTQC_trimnomatic.out)
    // FASTQC_check_final_python(FASTQC_check_final.out)

    // Workflow 2: Xử lý adapter và thực hiện công việc bình thường
    bwa_map(trimmomatic.out, params.adapter_dir)
    bamfile_sort(bwa_map.out)
    variant_calling_freebayes(bamfile_sort.out)
    extract_SNPs_INDELS(params.wholegenehg38_bed, params.genome_fai, params.genome_dict, variant_calling_freebayes.out)
    filter_variant(params.wholegenehg38_bed, params.genome_fai, params.genome_dict, extract_SNPs_INDELS.out)
    clean_snp_indels(filter_variant.out)
    bed_file(clean_snp_indels.out)
    annovar_annotation(bed_file.out)
    extract_data(annovar_annotation.out, params.NM_data_)
    fASTQC_check_final_all(extract_data.out)
    html_file(fASTQC_check_final_all.out)


}
workflow.onComplete { 
	log.info ( workflow.success ? "\nDone!" : "404 .. something went wrong" )
}
