from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
import shutil
from subprocess import run, PIPE
import subprocess
import os
import datetime
import zipfile
import uuid


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/log", response_class=HTMLResponse)
async def read_trangchu(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/", response_class=HTMLResponse)
async def read_log(request: Request):
    return templates.TemplateResponse("loging.html", {"request": request})



@app.get("/test", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("notation.html", {"request": request})

def secure_filename(filename):
    # Loại bỏ các ký tự không hợp lệ và thay thế chúng bằng "_"
    cleaned_filename = ''.join(c if c.isalnum() or c in (' ', '.', '-') else '_' for c in filename)
    return cleaned_filename

global global_author
global global_tenduan
global global_current_time
def delete_empty_directories(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
@app.post("/run-nextflow/")
async def run_nextflow(
    request: Request,
    author: str = Form(...),
    namsinh: str = Form(...),
    goitinh: str = Form(...),
    tenduan: str = Form(...), 

    reads: list[UploadFile] = Form(...),
    maMN: UploadFile = Form(...),
    BED: UploadFile = Form(...),
    Adapter: UploadFile = Form(...),

):
    ####xoá khoảng trắng tránh lỗi
    author = author.replace(" ", "_")
    namsinh = namsinh.replace(" ", "_")
    goitinh = goitinh.replace(" ", "_")
    tenduan = tenduan.replace(" ", "_")
    current_time = datetime.datetime.now()
    current_time_nhanmau=current_time.strftime("%Y-%m-%d")
    current_time=current_time.strftime("%Y-%m-%d_%H-%M-%S")
    
    global global_author
    global_author = author
    global global_tenduan
    global_tenduan = tenduan
    global global_current_time
    global_current_time = current_time
    # Kiểm tra tính hợp lệ của dữ liệu đầu vào
    for file in reads:
        if not file.filename.endswith(('.fastq', '.fq')):
            # return {"error": "Tệp không hợp lệ, hãy chọn tệp .fq hoặc .fastq"}
            return templates.TemplateResponse(
            "notation.html",
            {"request": request, "output_dir": "Tệp không hợp lệ, hãy chọn tệp .fq hoặc .fastq"},
    )
    
    # Tạo thư mục tạm thời để lưu trữ các tệp đọc
    output_directory_1 = os.path.join("uploads", author, secure_filename(tenduan))
    output_directory = os.path.join(output_directory_1, secure_filename(current_time))

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory, exist_ok=True)

    for file in reads:
            file_path = os.path.join(output_directory, secure_filename(file.filename))
            if os.path.exists(file_path):
                continue
            with open(file_path, "wb") as dest_file:
                shutil.copyfileobj(file.file, dest_file)

    adapter_dir = os.path.join(output_directory, 'adapter')
    maMN_dir = os.path.join(output_directory, 'maMN')
    BED_dir = os.path.join(output_directory, 'BED')

    os.makedirs(adapter_dir, exist_ok=True)
    os.makedirs(maMN_dir, exist_ok=True)
    os.makedirs(BED_dir, exist_ok=True)

    # Copy files to directories
    if Adapter:
        Adapter_path = os.path.join(adapter_dir, secure_filename(Adapter.filename))
        if not os.path.exists(Adapter_path):
            with open(Adapter_path, "wb") as dest_file:
                shutil.copyfileobj(Adapter.file, dest_file)

    if maMN:
        maMN_path = os.path.join(maMN_dir, secure_filename(maMN.filename))
        if not os.path.exists(maMN_path):
            with open(maMN_path, "wb") as dest_file:
                shutil.copyfileobj(maMN.file, dest_file)

    if BED:
        BED_path = os.path.join(BED_dir, secure_filename(BED.filename))
        if not os.path.exists(BED_path):
            with open(BED_path, "wb") as dest_file:
                shutil.copyfileobj(BED.file, dest_file)


    # Chuẩn bị lệnh nextflow
    command = ['nextflow', 'run', 'fastqc.nf ']
    # Thêm các tham số 
    # command.extend(['-resume'])
    command.extend(['--tenkhachang', str(author)])
    command.extend(['--namsinh', str(namsinh)])
    command.extend(['--goitinh', str(goitinh)])
    command.extend(['--ten_du_an',str(tenduan)])
    command.extend(['--ngaynhanmau',str(current_time_nhanmau)])
    command.extend(['--ngaytraketqua',str(current_time_nhanmau)])
    #lấy biến thời gian
    command.extend(['--times', str(current_time)])
    link_read = f"{output_directory}/*{{1,2}}.f*"
    command.extend(['--reads', str(link_read)])
    ####xoá thư mục trống
    delete_empty_directories(os.getcwd())
    ### thêm điều kiện command
    if os.path.exists(os.path.join(maMN_dir, secure_filename(maMN.filename))) and os.path.exists(os.path.join(BED_dir, secure_filename(BED.filename))):
        command.extend(['--NM_data', maMN_dir, '--bed_file', BED_dir])

    if os.path.exists(os.path.join(adapter_dir, secure_filename(Adapter.filename))):
        command.extend(['--adapter_dir', adapter_dir])
    try:
        result = run(command, stdout=PIPE, stderr=PIPE, text=True)
    except subprocess.CalledProcessError as e:
        error_message = f"Lỗi khi thực thi command: {e}"
        return templates.TemplateResponse(
            "notation.html",
            {"request": request, "output_dir": error_message},
        )
    except Exception as e:
        error_message = f"Lỗi khác: {e}"
        return templates.TemplateResponse(
            "notation.html",
            {"request": request, "output_dir": error_message},
        )
    # result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

    # tạo zip file 
    global global_zip_file_path
    directory_to_zip = f"ketqua/{author}/{tenduan}/{current_time}"
    zip_file_name = f"ketqua_{author}_{tenduan}.zip"
    zip_file_path = os.path.join(directory_to_zip, zip_file_name)


    global_zip_file_path = zip_file_path
    #//////////////////////////////////////////////
    # Get the result directory
    output_PRINT = result.stdout
    command_string = ' '.join(command)
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "output_dir": output_PRINT, "output_PRINT": result,"command_string": command_string},
    )
    

@app.get("/download-s22")
async def download_s22():
    # Đường dẫn đến tệp S22.bam
    file_path = "/home/dungnguyen/genepanel/results/Bwa_map/S22.bam"
    return FileResponse(file_path, headers={"Content-Disposition": "attachment; filename=S22.bam"})

@app.get("/create_and_download_zip")
async def create_and_download_zip():
    # Đường dẫn đến thư mục cần đóng gói (sử dụng đường dẫn tương đối)
    global global_zip_file_path
    author = global_author
    tenduan = global_tenduan
    current_time =global_current_time
    directory_to_zip = f"ketqua/{author}/{tenduan}/{current_time}"
    zip_file_name = f"ketqua_{author}_{tenduan}.zip"
    zip_file_path = os.path.join(directory_to_zip, zip_file_name)

    if os.path.exists(zip_file_path):
        global_zip_file_path = zip_file_path
        return FileResponse(global_zip_file_path, filename=zip_file_name)

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_to_zip))
    global_zip_file_path = zip_file_path
    return FileResponse(global_zip_file_path, filename=zip_file_name)

@app.post("/dangnhap/")
async def dangnhap_taikhoan(
    request: Request,
    password: str = Form(...),
    email: str = Form(...),
):
    if password == "1" and email == "admin@gmail.com":
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "output_dir": ""},
        )

    return templates.TemplateResponse(
        "notation.html",
        {"request": request, "output_dir": "Tài Khoản Mật Khẩu Không chính xác"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
