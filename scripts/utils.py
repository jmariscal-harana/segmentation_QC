import os
import numpy as np

def find_patient_date_folders(path_DICOM_formatted):
    patient_folders =  sorted([fname for fname in os.listdir(path_DICOM_formatted) if (not fname.startswith('.') and os.path.isdir(os.path.join(path_DICOM_formatted, fname)))])
    
    patient_date_folders = []

    for patient_folder in patient_folders:
        patient_folder_full_path = os.path.join(path_DICOM_formatted, patient_folder)
        date_folders = sorted([fname for fname in os.listdir(patient_folder_full_path) if (not fname.startswith('.') and os.path.isdir(os.path.join(patient_folder_full_path, fname)))])

        for date_folder in date_folders:
            patient_date_folder = os.path.join(patient_folder, date_folder)
            patient_date_folders = np.append(patient_date_folders, patient_date_folder)
        
    return patient_date_folders
