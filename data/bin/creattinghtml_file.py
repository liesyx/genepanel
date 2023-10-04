#!/usr/bin/env python
import pandas as pd
import sys

name = sys.argv[1]
ketquaphantich = sys.argv[2]
phuluc = sys.argv[3]
ket_qua_sau_gop = sys.argv[4]
tenkhachang = sys.argv[5]
ngaynhanmau = sys.argv[6]
namsinh = sys.argv[7]
goitinh = sys.argv[8]
loaimau = sys.argv[9]
ngaytraketqua = sys.argv[10]
data_checktung_file = sys.argv[11]


# python creattinghtml_file.py S26 S26_data_bienthegaybenh.xlsx S26_data_final.xlsx S26__comparison_result.txt 1 2 3 4 5 6 S26__comparison1.txt
# Đọc dữ liệu từ tệp CSV
ket_qua_lap_rap = pd.read_csv(ket_qua_sau_gop, sep='\t')
ket_qua_lap_rap_html = ket_qua_lap_rap.to_html(index=False)

data_checktung_file_h = pd.read_csv(data_checktung_file, sep='\t')
ket_qua_lap_rap_tung_file_html = data_checktung_file_h.to_html(index=False)

ketquaphantich_1 = pd.read_excel(ketquaphantich)
ketquaphantich_html = ketquaphantich_1.to_html(index=False)

phuluc_1 = pd.read_excel(phuluc)
phuluc_html = phuluc_1.to_html(index=False)

# Chuỗi CSS
style_css_data = '''
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
    }

    header {
        background-color: #4CAF50;
        color: white;
        text-align: center;
        padding: 3px;
    }

    h1 {
        color: #333;
    }

    .container {
        max-width: 1200px;
        margin: 20px auto;
        padding: 50px;
        background-color: #fff;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
        border-radius: 5px;
    }

.dataframe {
    font-family: Arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

.dataframe th, .dataframe td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

.dataframe tr:nth-child(even) {
    background-color: #f2f2f2;
}

.dataframe th {
    background-color: #4CAF50;
    color: white;
}

</style>
'''

# Tạo chuỗi HTML
html_output = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>LOBI TEST</title>
    {style_css_data}
<body>
    <header>
        <h1>KẾT QUẢ PHÂN TÍCH</h1>
    </header>
<div class="container">
    <h2>Thông Tin Khách Hàng</h2>

        <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Họ và tên</th>
      <th>Năm sinh</th>
      <th>Giới Tính</th>
      <th>Ngày nhận mẫu</th>
      <th>Ngày trả kết quả</th>
      <th>Loại mẫu</th>
      <th>Mã phân tích</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{tenkhachang}</td>
      <td>{namsinh}</td>
      <td>{goitinh}</td>
      <td>{ngaynhanmau}</td>
      <td>{ngaytraketqua}</td>
      <td>dsDNA</td>
      <td>.</td>
    </tr>

  </tbody>
</table>
</div>

<div class="container">
    <h2>Kết Quả Phân Tích</h2>

        {ketquaphantich_html}

    <p>*Chú ý: phần kết quả phân tích chỉ báo cáo những biến dị đáng chú ý về mặt lâm sàng.</p>
    <p>phần phụ lục liệt kê những biến dị được tìm thấy trong phân tích này.</p>
    <br>
    <p>Kết quả được báo cáo dựa trên những hiểu biết và kiến thức khoa học tại thời điểm hiện tại về những gen đã được phân tích.</p>
</div>

<div class="container">
    <h2>Kết Quả Lắp Ráp</h2>

        {ket_qua_lap_rap_tung_file_html}

</div>


<div class="container">
    <h2>Phương Pháp Phân Tích</h2>
    <!-- Thêm nội dung cho phương pháp phân tích nếu cần -->
    <p>Dữ liệu đọc trình tự từ MiSeq (Illumina, USA) được áp dụng quy trình phát hiện biến dị di truyền LB GenPan được phát triển bởi LOBI VietNam. Phân tích này phát hiện đồng thời các biến dị di truyền điểm, thêm, mất, và các đoạn nhỏ. Tính chất gây bệnh của biến dị được phân loại theo tiêu chuẩn và hướng dẫn của ACMG và AMP.</p>

    <h3>Giới hạn của phân tích</h3>
    <p>Phân tích này không phát hiện được một số biến đổi về chất lượng bản sao, bao gồm biến đổi về số lượng những đoạn lớn của những gen dị hợp tử. Phân tích này cũng không phát hiện được một số đột biến đặc biệt như là đột biến tái tở hợp phức tạp, đột biến về cấu trúc (nghĩa là mất, nhân và đảo đoạn lớn), thêm đoạn dị hợp tử lớn (nghĩa là thêm đoạn gây ra bởi Alu), cũng như những biến dị nằm ngoài vùng nhắm đích.</p>

    <h3>Kết quả phân tích</h3>
    <p>Kết quả của phân tích này chỉ phục vụ cho mục đích tham khảo, và không được giải thích, theo bất cứ các thức nào là tư vấn y tế của Chuyên Gia về Sức Khỏe.</p>

    <!-- Danh sách các gen được phân tích có thể thêm ở đây -->

    <ul>
        <li>Phiếu trả kết quả này đặc hiệu cho mẫu và các gen được phân tích, nên không thể dùng cho mục đích khác.</li>
        <li>Những dữ liệu trong phiếu trả kết quả này được tạo ra theo quy trình phân tích chuẩn và chỉ được dùng cho mục đích tham khảo lâm sàng.</li>
        <li>Biến dị được định danh theo hướng dẫn của HGVS (<a href="http://varnomen.hgvs.org/">http://varnomen.hgvs.org/</a>).</li>
        <li>Sự hiện diện của biến dị gây bệnh ở những gen được khuyến cáo bởi các hiệp hội ung thư chỉ ra nguy cơ mắc bệnh ung thư di truyền của người mang đột biến cao hơn quần thể.</li>
        <li>Nếu không phát hiện biến dị gây bệnh trên những gen được khuyến cáo nghĩa là nguy cơ mắc bệnh ung thư di truyền của người được phân tích là thấp, nhưng không loại trừ hoàn toàn.</li>
        <li>Kết quả này không loại trừ nguy cơ ung thư do những đột biến không thể được phát hiện bằng phương pháp phân tích này hoặc được gây ra bởi những yếu tố không di truyền như là môi trường, lối sống.</li>
        <li>Nếu những biến dị chưa xác định ý nghĩa lâm sàng được phát hiện thì ảnh hưởng của chúng đến việc mắc bệnh ung thư di truyền là không chắc chắn và cần được xác định thêm bởi những nghiên cứu lâm sàng.</li>
        <li>Các biến đổi di truyền được phân tích dựa trên những hiểu biết và kiến thức thực tại của Y học. Tuy nhiên, với sự cập nhật và phát triển không ngừng của Y học, các biến đổi có thể được đánh giá lại tầm quan trọng trong lâm sàng.</li>
    </ul>
</div>

<div class="container">
    <h2>Phụ Lục</h2>
    <p>Danh sách các biến dị được phát hiện trong phân tích này</p>
    <div>

            {phuluc_html}

        <p>Ý nghĩa lâm sàng của biến dị được phân loại theo hệ thống 5 bậc theo hướng dẫn của ACMG và AMP, bao gồm: Gây bệnh (pathogenic), Có Thể gây bệnh (like pathogenic), Không xác định (uncertain significance), Có thể lành tính(likely benign) và lành tính (benign).</p>
    </div>
</div>

</body>
</html>
'''
html_check_tung_file = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>LOBI TEST</title>
    {style_css_data}
<body>
    <header>
        <h1>KẾT QUẢ PHÂN TÍCH</h1>
    </header>
<div class="container">
    <h2>Thông Tin Khách Hàng</h2>

        <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Họ và tên</th>
      <th>Năm sinh</th>
      <th>Giới Tính</th>
      <th>Ngày nhận mẫu</th>
      <th>Ngày trả kết quả</th>
      <th>Loại mẫu</th>
      <th>Mã phân tích</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{tenkhachang}</td>
      <td>{namsinh}</td>
      <td>{goitinh}</td>
      <td>{ngaynhanmau}</td>
      <td>{ngaytraketqua}</td>
      <td>dsDNA</td>
      <td>.</td>
    </tr>

  </tbody>
</table>
</div>

<div class="container">
    <h2>Kết Quả Lắp Ráp Tổng</h2>
        {ket_qua_lap_rap_html}
</div>


</body>
</html>
'''


# Lưu chuỗi HTML vào tệp HTML
with open(f'{name}_ketqua.html', 'w') as file:
    file.write(html_output)

with open('ketqua_lap_rap.html', 'w') as file:
    file.write(html_check_tung_file)
