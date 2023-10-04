# FROM continuumio/miniconda3
# RUN apt-get update && apt-get install -y openjdk-17-jdk wget unzip python

# RUN wget https://github.com/broadinstitute/gatk/releases/download/4.1.4.1/gatk-4.1.4.1.zip \  
#      && unzip gatk-4.1.4.1.zip && rm gatk-4.1.4.1.zip
# ENV PATH=/gatk-4.1.4.1:$PATH
# ENV PATH=/data/annovar/annovar/table_annovar.pl:$PATH       

# # Cập nhật conda
# RUN conda update conda -y

# # Tạo môi trường conda
# RUN conda create -n genepanel
# ENV PATH /opt/conda/envs/genepanel/bin:$PATH

# # Cài đặt tools
# RUN conda install -c bioconda bwa -y
# RUN conda install -c bioconda samtools -y 
# RUN apt-get install -y libssl1.0.0
# RUN conda install -c bioconda bcftools -y
# RUN conda install -c bioconda trimmomatic -y
# RUN conda install -c bioconda nextflow -y
# RUN conda install -c bioconda fastqc -y
# RUN conda install -c conda-forge nano -y
# RUN pip install fastapi[all] jinja2 uvicorn



# RUN mkdir /app 
# WORKDIR /app
# COPY . .
# EXPOSE 8888


# # Thiết lập môi trường mặc định khi chạy container
# # ["/bin/bash"] 
# #uvicorn main:app --host 0.0.0.0 --port 8888 --reload
# RUN echo '#!/bin/bash' > run.sh && \
#     echo 'conda run -n genepanel ' >> run.sh && \
#     # echo 'uvicorn main:app --host 0.0.0.0 --port 8000 --reload' >> run.sh && \
#     chmod +x run.sh

# CMD ["./run.sh"]

# # uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# #docker rmi --force docker_genepanel 
# # docker exec -it 4a5e2eb58cb6 /bin/bashc7c755ffd59b     47ac56941f27

# #docker run -it --rm -v /home/dungnguyen/genepanel/test:/app/data2 docker_genepanel
# # docker run -it -v /home/dungnguyen/genepanel/data:/app/data gene
# # docker run --rm -v /home/dungnguyen/genepanel/data:/app/data docker_genepanel
# # docker run -it --rm -v /home/dungnguyen/genepanel/test:/app/data docker_genepanel bash -c "nextflow fastqc.nf --reads $baseDir/data/reads/*_R{1,2}.fastq"
# # docker run -it --rm -v /home/dungnguyen/genepanel/data:/app/data docker_genepanel bash -c "nextflow fastqc.nf --reads $pwd/data/reads/*_R{1,2}.fastq"
# # docker rm $(docker ps -a -q) #xoa toan bo file docker none

	
# # docker exec -it 3a2608e78994 /bin/bash vào container đang chạy
# # docker run -it -v /home/dungnguyen/genepanel:/genepanel docker_genepanel_main uvicorn main:app --host 0.0.0.0 --port 8888 --reload
# # docker run -it -v /home/dungnguyen/genepanel:/genepanel genepanel:0.5 /bin/bash -c "cd /genepanel | ls"
# # docker run -it -v /home/dungnguyen/genepanel/data:/data -v /home/dungnguyen/genepanel/data:/data fbda33098912 nextflow fastqc.nf
# Use a base image with Conda and other dependencies
FROM continuumio/miniconda3

# Update the system and install essential packages
RUN apt-get update && apt-get install -y openjdk-17-jdk wget unzip

# Install GATK
RUN wget https://github.com/broadinstitute/gatk/releases/download/4.1.4.1/gatk-4.1.4.1.zip \
     && unzip gatk-4.1.4.1.zip && rm gatk-4.1.4.1.zip
ENV PATH=/gatk-4.1.4.1:$PATH

# Install ANNOVAR (assuming it's downloaded and placed in /data/annovar)
ENV PATH=/data/annovar:$PATH

# Update Conda
RUN conda update conda -y

# Create a Conda environment
RUN conda create -n genepanel
ENV PATH /opt/conda/envs/genepanel/bin:$PATH

# Install bioinformatics tools and other dependencies
RUN conda install -c bioconda bwa samtools bcftools trimmomatic nextflow fastqc -y
RUN conda install -c conda-forge nano -y

# Install Python dependencies using pip
RUN pip install fastapi[all] jinja2 uvicorn

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Copy your pipeline files into the container
COPY . .

# Expose a port if needed
# EXPOSE 8888

# Create a run script to activate the Conda environment and run your command
RUN echo '#!/bin/bash' > run.sh && \
    echo 'conda activate genepanel' >> run.sh && \
    chmod +x run.sh

# Set the default command to run your script
CMD ["./run.sh"]
