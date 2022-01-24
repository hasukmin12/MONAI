
# https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/common_questions.md


from evaluator import evaluate_folder


# folder_with_gt = '/data/sukmin/nnUNet_raw_data_base/nnUNet_raw_data/Task139_Urinary/labelsTs'
folder_with_gt = '/data2/sukmin/monai_dataset/Task163_Ureter/labelsTs'
# folder_with_gt = '/data2/sukmin/nnUNet_raw_data_base/nnUNet_raw_data/Task172_Ureter/labelsTs'
# folder_with_gt = '/data/sukmin/nnUNet_raw_data_base/nnUNet_raw_data/Task150_Bladder/labelsTs'
# folder_with_gt = '/data/sukmin/_has_Bladder_red'

folder_with_pred = '/data2/sukmin/inf_2_GT_163_3'

labels = (0,1) # test 하고 싶은 라벨 입

evaluate_folder(folder_with_gt, folder_with_pred, labels)


