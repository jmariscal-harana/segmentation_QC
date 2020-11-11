import os
import numpy as np
import pandas as pd

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

def add_csv_to_csv(source_csv, target_csv):
    # get all the data ffrom both csv
    df_source = pd.read_csv(source_csv, header=0)
    if os.path.isfile(target_csv):
        df_target = pd.read_csv(target_csv, header=0)
        # append data from source_csv to target_csv
        df_target = df_target.append(df_source, ignore_index=True)
    else:
        df_target = df_source

    # save target_csv
    pd.DataFrame(df_target).to_csv(target_csv, index = False)