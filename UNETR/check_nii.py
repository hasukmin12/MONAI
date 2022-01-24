import os

import nibabel as nib

# 1. Proxy 불러오기

# proxy = nib.load('/data2/sukmin/monai_dataset/Task163_Ureter/labelsTs/case_00240.nii.gz')
proxy = nib.load('/data2/sukmin/inf_2_GT_163/case_00240.nii.gz')
# proxy = nib.load('/home/has/Datasets/CT_annotated_Kidney_3D/imaging/img_case_000.nii.gz')
# proxy = nib.load('./case_000.nii.gz')

# 2. Header 불러오기
header = proxy.header

# 3. 원하는 Header 불러오기 (내용이 문자열일 경우 숫자로 표현됨)
header_size = header['sizeof_hdr']

# 2. 전체 Image Array 불러오기
arr = proxy.get_fdata()

# 3. 원하는 Image Array 영역만 불러오기
sub_arr = proxy.dataobj[..., 0:5]


# print(arr.shape)
#
# arr = arr.transpose((1,2,0))

print(arr.shape)
print(arr.max())