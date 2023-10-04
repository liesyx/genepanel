  name=$1
  outdir=$2
  nextflow_dir=$3
  
  
  pwd=$(pwd)

  cd   $nextflow_dir/${outdir}/$name
  bash  $nextflow_dir/data/bin/bash.sh 
  python $nextflow_dir/data/bin/fastqc_check.py ${name}
