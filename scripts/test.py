# Utils
import os, random, shutil
import numpy as np
import pandas as pd
from datetime import datetime
from utils import find_patient_date_folders

# click2label
# %matplotlib inline
from click2label import ClickLabel

def clinician_init(name, surname):
    clinician_ID = name + '_' + surname
    date_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    return clinician_ID, date_time

# def git_clone(path_root, path_repo):
#     git clone https://github.com/jmariscal-harana/segmentation_QC

# Paths
path_root = '/Users/jorge/PostDoc/Scripts/'
path_repo = os.path.join(path_root, 'segmentation_QC/')
path_images = os.path.join(path_repo, 'images')
path_images_temp = os.path.join(path_repo, 'images_temp')
path_input = os.path.join(path_repo, 'input')
path_output = os.path.join(path_repo, 'output')
path_scripts = os.path.join(path_repo, 'scripts')

# Initialisation
initialisation_bool = False

# Mount Google Drive
#

# Paths
path_root = '/Users/jorge/PostDoc/Scripts/'
path_repo = os.path.join(path_root, 'segmentation_QC/')
path_images = os.path.join(path_repo, 'images')
path_images_temp = os.path.join(path_repo, 'images_temp')
path_input = os.path.join(path_repo, 'input')
path_output = os.path.join(path_repo, 'output')
path_scripts = os.path.join(path_repo, 'scripts')

# Initialisation
initialisation_bool = False

# Mount Google Drive
#

# Get a list of studies which are left to analyse

# 1. find IDs+series names in seg_QC_list.csv
seg_QC_list_csv = os.path.join(path_input, 'seg_QC_list.csv')
df_list = pd.read_csv(seg_QC_list_csv)
study_IDs = df_list['Study ID'].astype(str).to_numpy()
study_series_names = df_list['Series name'].astype(str).to_numpy()
folders_list = np.unique(study_IDs + os.path.sep + study_series_names)

# 1. find IDs+series names in images/
folders_images = find_patient_date_folders(path_images)

# Find all  
folders_coincide = list(set(folders_images).intersection(folders_list)) # Studies which appear in seg_QC_list.csv and images/

# Error handling
if len(folders_list) == 0:
    raise Exception('{} is empty!'.format(seg_QC_list_csv))
elif len(folders_images) == 0:
    raise Exception('{} is empty!'.format(path_images))
elif len(folders_coincide) == 0:
    raise Exception('None of the folders in {} and {} coincide!'.format(seg_QC_list_csv, path_images))

study_available = []
study_missing = []
study_missing_csv = os.path.join(path_output, 'study_missing.csv')

# 2. For each folder, check that all image_names in seg_QC_list.csv can be found in images/ID/series_name/
for loc, folder_coincide in enumerate(folders_coincide):
    # 1. find all filenames within csv
    # print(folder_coincide)
    image_names_csv = [image_name for study_ID, series_name, image_name in zip(df_list['Study ID'], df_list['Series name'], df_list['Image name']) if (study_ID + os.path.sep + series_name) == folder_coincide]
    # print(sorted(image_names_csv))

    # 1. find all filenames within folder
    folder_image = os.path.join(path_images, folder_coincide)
    folder_image_names = [f for f in os.listdir(folder_image) if os.path.isfile(os.path.join(folder_image,f)) and f.endswith('.jpg')]
    # print(sorted(folder_image_names))

    # 2. find images missing from folder
    images_missing = list(set(image_names_csv).difference(folder_image_names))
    # print(images_missing)

    if len(images_missing) > 0:
        # print ('Some images are missing from {}\n'.format(folder_coincide))
        study_missing = np.append(study_missing, folder_coincide)
        pd.DataFrame(study_missing).to_csv(study_missing_csv, header=['Folder name'], index = False) # Update study_missing.csv
        continue
    else:
        study_available = np.append(study_available, folder_coincide)

study_available = list(study_available)

# print(study_available)

# 3. compare study_available to those in seg_QC_complete.csv and keep the difference
study_complete_csv = os.path.join(path_output, 'seg_QC_complete.csv')

if os.path.isfile(study_complete_csv):
    df_complete = pd.read_csv(study_complete_csv)
    # print(df_complete)
    study_complete = np.unique(df_complete['Study ID'].astype(str).to_numpy()+os.path.sep+df_complete['Series name'].astype(str).to_numpy())
    # print(study_complete)
    study_available = list(set(study_available).difference(study_complete))
    # print(study_available)

# Randomise it
random.shuffle(study_available)
# print(study_available)
# Now you have a random list with all Study IDs

# 1. Copy 1 study at a time from images into images_temp/
source_folder = os.path.join(path_images, study_available[0])
destination_folder = os.path.join(path_images_temp, study_available[0])

if os.path.exists(destination_folder) and os.path.isdir(destination_folder):
#     print('Folder {} exists. Removing.'.format(destination_folder))
    shutil.rmtree(destination_folder)
# print('Copying {} to {}.'.format(source_folder, destination_folder))
_ = shutil.copytree(source_folder, destination_folder)
# TODO: check that images are not too big (~250x250), otherwise resahpe, as this slows down the GUI

# 2. Show all the images
#     under each image you can click reject/revise
cl = ClickLabel(result_path='output/df_temp.csv', # file to save the results to 
                label_options=['REVISE', 'REJECT'], # two labels for left & right click)
                color_options=['green', 'red'], # colors corresponding to the two labels
                fontsize=10) # size of display text

cl.labelling_grid(  data_folder=destination_folder,  # folder containing the images to label
                    rows=5, # rows in each labelling grid
                    columns=4) # columns in each labelling grid

cl.labelling_grid(  data_folder=destination_folder,  # folder containing the images to label
                    rows=5, # rows in each labelling grid
                    columns=4) # columns in each labelling grid

print('end')