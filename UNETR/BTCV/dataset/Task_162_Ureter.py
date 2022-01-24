import shutil
import os
import json


def maybe_mkdir_p(directory):
    directory = os.path.abspath(directory)
    splits = directory.split("/")[1:]
    for i in range(0, len(splits)):
        if not os.path.isdir(os.path.join("/", *splits[:i+1])):
            try:
                os.mkdir(os.path.join("/", *splits[:i+1]))
            except FileExistsError:
                # this can sometimes happen when two jobs try to create the same directory at the same time,
                # especially on network drives.
                print("WARNING: Folder %s already existed and does not need to be created" % directory)


def save_json(obj, file, indent=4, sort_keys=True):
    with open(file, 'w') as f:
        json.dump(obj, f, sort_keys=sort_keys, indent=indent)


def subdirs(folder, join=True, prefix=None, suffix=None, sort=True):
    if join:
        l = os.path.join
    else:
        l = lambda x, y: y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isdir(os.path.join(folder, i))
            and (prefix is None or i.startswith(prefix))
            and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res





if __name__ == "__main__":
    """
    This is the Ureter dataset from sukmin Ha
    """

    # base = "/data5/sukmin/_has_Task123_Ureter"
    base = "/data/sukmin/_has_Task162_Ureter"

    task_id = 162
    task_name = "Ureter"
    foldername = "Task%03.0d_%s" % (task_id, task_name)

    data_path = '/data/sukmin/monai_dataset'
    maybe_mkdir_p(data_path)

    out_base = os.path.join(data_path, foldername)


    imagestr = os.path.join(out_base, "imagesTr")
    imagests = os.path.join(out_base, "imagesTs")
    labelstr = os.path.join(out_base, "labelsTr")
    labelsts = os.path.join(out_base, "labelsTs")

    maybe_mkdir_p(imagestr)
    maybe_mkdir_p(imagests)
    maybe_mkdir_p(labelstr)
    maybe_mkdir_p(labelsts)

    train_patient_names = []
    val_patient_names = []
    test_patient_names = []
    all_cases = subdirs(base, join=False)

    train_patients = all_cases[:192]
    val_patients = all_cases[192:240]
    test_patients = all_cases[240:]


    for p in train_patients:
        curr = os.path.join(base, p)
        label_file = os.path.join(curr, "segmentation.nii.gz")
        image_file = os.path.join(curr, "imaging.nii.gz")
        shutil.copy(image_file, os.path.join(imagestr, p + ".nii.gz"))
        shutil.copy(label_file, os.path.join(labelstr, p + ".nii.gz"))
        train_patient_names.append(p)

    for p in val_patients:
        curr = os.path.join(base, p)
        label_file = os.path.join(curr, "segmentation.nii.gz")
        image_file = os.path.join(curr, "imaging.nii.gz")
        shutil.copy(image_file, os.path.join(imagestr, p + ".nii.gz"))
        shutil.copy(label_file, os.path.join(labelstr, p + ".nii.gz"))
        val_patient_names.append(p)

    for p in test_patients:
        curr = os.path.join(base, p)
        image_file = os.path.join(curr, "imaging.nii.gz")
        shutil.copy(image_file, os.path.join(imagests, p + ".nii.gz"))
        test_patient_names.append(p)

    # 나중에 test inference를 위해 폴더는 만들어놓
    for p in test_patients:
        curr = os.path.join(base, p)
        label_file = os.path.join(curr, "segmentation.nii.gz")
        shutil.copy(label_file, os.path.join(labelsts, p + ".nii.gz"))





    json_dict = {}
    json_dict['description'] = "Ureter segmentation"
    json_dict['labels'] = {
        "0": "background",
        "1": "Ureter"
    }
    json_dict['licence'] = "yt"
    json_dict['modality'] = {
        "0": "CT",
    }
    json_dict['name'] = "Ureter"
    json_dict['numTest'] = len(test_patient_names)
    json_dict['numTraining'] = len(train_patient_names) + len(val_patient_names)
    json_dict['reference'] = "Hanyang University"
    json_dict['release'] = "0.0"
    json_dict['tensorImageSize'] = "4D"
    # json_dict['tensorImageSize'] = "3D"
    json_dict['test'] = ["./imagesTs/%s.nii.gz" % i.split("/")[-1] for i in test_patient_names]
    json_dict['training'] = [{'image': "./imagesTr/%s.nii.gz" % i.split("/")[-1], "label": "./labelsTr/%s.nii.gz" % i.split("/")[-1]} for i in
                             train_patient_names]

    json_dict['validation'] = [{'image': "./imagesTr/%s.nii.gz" % i.split("/")[-1], "label": "./labelsTr/%s.nii.gz" % i.split("/")[-1]} for i in
                               val_patient_names]

    save_json(json_dict, os.path.join(out_base, "dataset.json"))