#!/usr/bin/env python
import pandas as pd
import sys



name = sys.argv[1]
annotation = sys.argv[2]
data2_txt =sys.argv[3]

data_txt = annotation
data_1 = pd.read_csv(data_txt, delimiter='\t')
NM_data = pd.read_csv(data2_txt, delimiter='\t')
# Chọn  cột 
selected_columns = ['Gene.refGene', 'ExonicFunc.refGene', 'AAChange.refGene', 'avsnp150', 'Otherinfo13','CLNSIG','Func.refGene','Ref','Alt','Chr','Start']

# Tạo DataFrame mới 
new_data = data_1[selected_columns].copy()  
new_data.loc[:, 'ExtractedInfo'] = new_data['Otherinfo13'].str[:3]
new_data['ExonicFunc.refGene'] = new_data.apply(lambda row: row['Func.refGene'] if row['ExonicFunc.refGene'] == '.' else row['ExonicFunc.refGene'], axis=1)
new_data['Loại Biến Dị'] = new_data['ExonicFunc.refGene'].apply(lambda x: x[:-3] if 'SNV' in x else x)
new_data['thay_doi_aa'] = new_data['Chr'] + '.' + new_data['Start'].astype(str) + '.' + new_data['Ref'] + '>' + new_data['Alt']


def map_type(extracted_info):
    if extracted_info == '1/1':
        return 'Đồng hợp tử'
    elif extracted_info == '0/1':
        return 'Dị hợp tử'
    elif extracted_info == '1/2':
        return 'Dị hợp tử'
    else:
        return 'UNKNOWN'
    
def  map_type_3(CLNSIG):
    if 'Likely_pathogenic' in CLNSIG and 'pathogenic' in CLNSIG:
        return 'Gây bệnh/Có Thể gây Bệnh'
    elif 'pathogenic' in CLNSIG and not 'Likely_pathogenic' in CLNSIG:
        return 'Gây bệnh'
    elif 'Likely_pathogenic' in CLNSIG and not 'pathogenic' in CLNSIG:
        return 'Có thể gây bệnh'
    elif 'Likely_Benign' in CLNSIG and 'Benign' in CLNSIG:
        return 'Lành tính/Có thể lành tính'
    elif 'Likely_Benign' in CLNSIG and not 'Benign' in CLNSIG:
        return 'Có thể lành tính'
    elif 'Benign' in CLNSIG and not 'Likely_Benign' in CLNSIG:
        return 'lành tính'
    elif '.' in CLNSIG:
        return 'Không xác định'
    else:
        return 'Không xác định'

def update_nucleotide_change(row):
    if row['Thay đổi nucleotit'] == None:
        return row['thay_doi_aa']
    else:
        return row['Thay đổi nucleotit']
    
def thay_dau_cham(row):
    if row is None:
        return '.'
    else:
        return row
    
new_data['Hợp Tử'] = new_data['ExtractedInfo'].apply(map_type)
new_data['CLNSIG'] = new_data['CLNSIG'].apply(map_type_3)
new_data['LongestElement'] = new_data['AAChange.refGene'].str.split(',')
# Sử dụng .apply() để chọn phần tử dài nhất
new_data['LongestElement'] = new_data['LongestElement'].apply(lambda arr: max(arr, key=len))
new_data['LongestElement_array'] = new_data['LongestElement'].str.split(':')
new_data['Mã MN'] = new_data['LongestElement_array'].apply(lambda arr: arr[1] if len(arr) >= 2 else None).apply(thay_dau_cham)
new_data['exon'] = new_data['LongestElement_array'].apply(lambda arr: arr[2] if len(arr) >= 3 else None).apply(thay_dau_cham)
new_data['Thay đổi nucleotit'] = new_data['LongestElement_array'].apply(lambda arr: arr[3] if len(arr) >= 3 else None).apply(thay_dau_cham)
new_data['Thay đổi axit amin'] = new_data['LongestElement_array'].apply(lambda arr: arr[4] if len(arr) >= 4 else None).apply(thay_dau_cham)
new_data['Thay đổi nucleotit'] = new_data.apply(update_nucleotide_change, axis=1)

# ////////////////////////////////////////////////////////////////////////////////////////////
#xử lý mã MN
gene_to_NM = dict(zip(NM_data['gene'], NM_data['NM']))
new_data['Mã MN'] = new_data['Gene.refGene'].map(gene_to_NM)

# Ghi dữ liệu vào tệp Excel 
name_file=f"{name}_data.xlsx"
new_data.to_excel(name_file, index=False)


# ////////////////////////////////////////////////////////////////////////////////////////////
# xuất ra bảng mới
data_final_head = ['Gene.refGene', 'Mã MN','Thay đổi nucleotit','exon','Thay đổi axit amin', 'Loại Biến Dị', 'Hợp Tử', 'avsnp150','CLNSIG']
data_final = new_data[data_final_head].copy() 
data_final.rename(columns={'Gene.refGene': 'Gene'}, inplace=True)
data_final.rename(columns={'avsnp150': 'Mã biến dị'}, inplace=True)
data_final.rename(columns={'CLNSIG': 'Ý nghĩa lâm sàng'}, inplace=True)
data_final.rename(columns={'exon': 'Exon'}, inplace=True)
data_final.to_excel(f'{name}_data_final.xlsx', index=False)

# ////////////////////////////////////////////////////////////////////////////////////////////
# xuất bảng biến thể gây bệnh#
filtered_df = data_final[data_final['Ý nghĩa lâm sàng'].isin(['Có thể gây bệnh', 'Gây bệnh/Có Thể gây Bệnh','Gây bệnh'])]
filtered_df.to_excel(f'{name}_data_bienthegaybenh.xlsx', index=False)