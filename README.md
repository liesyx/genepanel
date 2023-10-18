
<h1 align="center">
  <br>
<!--   <a href="http://www.amitmerchant.com/electron-markdownify"><img src="https://raw.githubusercontent.com/amitmerchant1990/electron-markdownify/master/app/img/markdownify.png" alt="Markdownify" width="200"></a> -->
  <br>
  Gene Panel
  <br>
</h1>

<h4 align="center">A web for GenePanel build with core of <a href="https://www.nextflow.io/" target="_blank">Nextflow</a>.</h4>

<!--
<p align="center">
  <a href="https://badge.fury.io/js/electron-markdownify">
    <img src="https://badge.fury.io/js/electron-markdownify.svg"
         alt="Gitter">
  </a>
  <a href="https://gitter.im/amitmerchant1990/electron-markdownify"><img src="https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg"></a>
  <a href="https://saythanks.io/to/bullredeyes@gmail.com">
      <img src="https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg">
  </a>
  <a href="https://www.paypal.me/AmitMerchant">
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">
  </a>
</p>
-->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#Main-Workflow">Main Workflow</a> •
  <a href="#credits">Credits</a> •

</p>


<img src="https://github.com/liesyx/Gene-Panel/assets/63604038/c3907611-2147-47c0-b86a-be1a5dccfb63" alt="Alt text" title="Main Web site">



## Key Features
* Save the result preview as PDF
* Cross platform
  - Linux ready.
  - docker ready

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Java](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html) 

```bash

# Install nextflow
$ mkdir genepanel
$ cd genepnel
$ curl -s https://get.nextflow.io | bash
$ ./nextflow run hello


# Clone this repository dowload annovar database (location gene panel)
$ git clone https://github.com/liesyx/Gene-Panel.git
$ export PATH=/data/annovar/annovar:$PATH
$ perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb avsnp150 -buildver hg38 data/annovar/annovar/humandb
$ perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb gnomad312_genome -buildver hg38 data/annovar/annovar/humandb
$ perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb cosmic70 -buildver hg38 data/annovar/annovar/humandb
$ perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb refGene -buildver hg38 data/annovar/annovar/humandb
$ perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb cytoBand -buildver hg38 data/annovar/annovar/humandb
$ perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb clinvar_20221231 -buildver hg38 data/annovar/annovar/humandb
$ perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb intervar_20180118 -buildver hg38 data/annovar/annovar/humandb
$ perl data/annovar/annovar/annotate_variation.pl -webfrom annovar -downdb hrcr1 -buildver hg38 data/annovar/annovar/humandb


# build docker imgaes 
$ docker build -t genepanel:latest .

# Run the app (high recomment) (the location of fastqc.nf file )
$ ./nextflow run fastqc.nf -with-docker gene

# website for developer
$ uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```
## Parameter
```bash
# Parameter
# -resume
# -NM_data_
# -bed_file
# -ten_du_an 
# -goitinh
# -ngaynhanmau
# -tenkhachang
# -adapter_dir
```
## Main Workflow
<img src="https://github.com/liesyx/Gene-Panel/assets/63604038/51808164-ff59-4245-b588-ca320fcd67a4" alt="Alt text" title="Main Web site">

## Credits

This software uses the following open source packages:

- [Nextflow](https://www.nextflow.io/)
- [fastapi](https://fastapi.tiangolo.com/)



## Support

<a href="https://www.buymeacoffee.com/liesy" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


