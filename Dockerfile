
FROM continuumio/miniconda3
RUN apt-get update && apt-get install -y openjdk-17-jdk wget unzip python

RUN wget https://github.com/broadinstitute/gatk/releases/download/4.1.4.1/gatk-4.1.4.1.zip \  
     && unzip gatk-4.1.4.1.zip && rm gatk-4.1.4.1.zip
ENV PATH=/gatk-4.1.4.1:$PATH
ENV PATH=/data/annovar/annovar/table_annovar.pl:$PATH       

# Cập nhật conda
RUN conda update conda 

# Tạo môi trường conda
RUN conda create -n genepanel
ENV PATH /opt/conda/envs/genepanel/bin:$PATH
# Cài đặt tools
RUN apt-get install -y bwa samtools
RUN pip install vcfpy
RUN pip install pandas
RUN conda install -c bioconda bwa 
RUN conda install -c bioconda freebayes
RUN conda install -c bioconda bcftools 
RUN conda install -c bioconda trimmomatic 
RUN conda install -c bioconda nextflow 
RUN conda install -c bioconda fastqc 
RUN conda install -c conda-forge nano 
RUN pip install fastapi[all] jinja2 uvicorn
RUN conda install -c anaconda pandas
RUN conda install -c anaconda openpyxl
RUN apt-get update 
RUN conda update --all

#Khai bao thu muc lam viec
RUN mkdir /app 
WORKDIR /app
COPY . .
EXPOSE 8888


# Thiết lập môi trường mặc định khi chạy container
# ["/bin/bash"] 
#uvicorn main:app --host 0.0.0.0 --port 8888 --reload
RUN echo '#!/bin/bash' > run.sh && \
    echo 'conda run -n genepanel ' >> run.sh && \
    # echo 'uvicorn main:app --host 0.0.0.0 --port 8000 --reload' >> run.sh && \
    chmod +x run.sh

CMD ["./run.sh"]

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
#docker rmi --force docker_genepanel 
# docker exec -it 4a5e2eb58cb6 /bin/bashc7c755ffd59b     47ac56941f27


# docker run -v /home/dungnguyen/genepanel/data/annovar/annovar/humandb:/app/data/annovar/annovar/humandb -it gene_panel nextflow run fastqc.nf

# docker run -it --rm -v /home/dungnguyen/genepanel/data:/app/data docker_genepanel bash -c "nextflow fastqc.nf --reads $pwd/data/reads/*_R{1,2}.fastq"
# docker rm $(docker ps -a -q) #xoa toan bo file docker none

	
# docker exec -it 3a2608e78994 /bin/bash vào container đang chạy
# docker run -it -v /home/dungnguyen/genepanel:/genepanel docker_genepanel_main uvicorn main:app --host 0.0.0.0 --port 8888 --reload
# docker run -it -v /home/dungnguyen/genepanel:/genepanel genepanel:0.5 /bin/bash -c "cd /genepanel | ls"
# docker run -it -v /home/dungnguyen/genepanel/data:/data -v /home/dungnguyen/genepanel/data:/data fbda33098912 nextflow fastqc.nf

