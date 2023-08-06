import os
import shutil
from uuid import uuid4

from sys_helper import execute_cmd


def nifti2dicom(input_file, output_dir, accession_number=1):
    """
    Require nifti2dicom.
    sudo apt install nifti2dicom
    https://github.com/biolab-unige/nifti2dicom
    """
    cmd = f'nifti2dicom -i {input_file} -o {output_dir} -a {accession_number}'
    result = os.popen(cmd)
    return result.readlines()


def dicom2cavass(input_dir, output_file):
    execute_cmd(f'from_dicom {input_dir}/* {output_file}')


def nifti2cavass(input_file, output_file, dicom_accession_number=1):
    save_path = os.path.split(output_file)[0]
    tmp_dicom_dir = os.path.join(save_path, f'{uuid4()}')
    result = nifti2dicom(input_file, tmp_dicom_dir, dicom_accession_number)
    dicom2cavass(tmp_dicom_dir, output_file)
    shutil.rmtree(tmp_dicom_dir)
    return result


if __name__ == '__main__':
    r = nifti2cavass('/home/ubuntu/sda1.8T/Dataset/AMOS/AMOS22/imagesTr/amos_0086.nii.gz',
                 '/home/ubuntu/sdb1.8T/dj/amos_0086.IM0')
    print(r)
