from bids import BIDSLayout, BIDSValidator
import os
import nibabel as nib
import datalad.api as dl
import matplotlib.pyplot as plt
from math import ceil
from nilearn.plotting import view_img, plot_glass_brain, plot_anat, plot_epi, plot_roi
from nltools.data import Brain_Data

data_dir = './data/Localizer'
layout = BIDSLayout(data_dir, derivatives=True)
ds = dl.Dataset(data_dir)

# download file from dataset by path
def get_file(path):
  ds.get(path)

# print the first 10 files
def show_first_ten_files():
  first_ten_files = layout.get()[:10]
  print(first_ten_files)

# print the first 10 subject ids
def show_first_ten_sub_ids():
  first_ten_sub_ids = layout.get(target='subject', return_type='id', scope='derivatives')[:10]
  print(first_ten_sub_ids)

# print the file names for the raw bold functional nifti images for the first 10 subjects
def show_first_ten_raw_bold_nifti():
  raw_bold_nifti_files = layout.get(target='subject', scope='raw', suffix='bold', return_type='file')[:10]
  print(raw_bold_nifti_files)

# print a list of tasks included in the dataset 
def show_tasks():
  task = layout.get_task()
  print(task)

# print all of the files associated with a task
# e.g. task = 'localizer'
def show_files_by_task(task):
  task_files = layout.get(task=task, suffix='bold', scope='raw')[:10]
  print(task_files)

# print the filename for the first participant’s functional run
def show_first_participant_filename_by_task(task):
  first_run_file = layout.get(task=task)[0].filename
  print(first_run_file)

# print a dataframe of the layout
def show_layout_as_dataframe():
  dataframe = layout.to_df()
  print(dataframe)

# grab subject S01’s T1 image
def get_S01_T1_img():
  S01_T1_path = layout.get(subject='S01', scope='derivatives', suffix='T1w', return_type='file', extension='nii.gz')[1]
  get_file(S01_T1_path)
  img = nib.load(S01_T1_path)
  print(img.shape)
  return img

def get_horizontal_slice(img, start_slice=50, step=0):
  img_slice = img.get_fdata()[:,:,start_slice+step]
  return img_slice

def get_coronal_slice(img, start_slice=50, step=0):
  img_slice = img.get_fdata()[:,start_slice+step,:]
  return img_slice

def get_sagittal_slice(img, start_slice=50, step=0):
  img_slice = img.get_fdata()[start_slice+step,:,:]
  return img_slice

def get_slice(img, orientation, start_slice=50, step=0):
  if orientation == 'horizontal':
    return get_horizontal_slice(img, start_slice, step)
  if orientation == 'sagittal':
    return get_sagittal_slice(img, start_slice, step)
  if orientation == 'coronal':
    return get_coronal_slice(img, start_slice, step)

# plot fmri by slice
def plot_slice(img_slice):
  fig, ax = plt.subplots()
  ax.imshow(img_slice)

def plot_S01_T1_slice(orientation):
  plot_slice(get_slice(get_S01_T1_img(), orientation))

def plot_slices(slices):
  num_slices = len(slices)
  fig, axs = plt.subplots(ceil(num_slices / 3) , 3)
  for idx, ax in enumerate(axs.flat):
    if idx < num_slices:
      img_slice = slices[idx]
      ax.imshow(img_slice)

def plot_S01_T1_slices(num_slices, orientation):
  img = get_S01_T1_img()
  slices = [get_slice(img, orientation, 40, step) for step in range(0,num_slices)]
  plot_slices(slices)

# show_first_ten_files()
# show_first_ten_sub_ids()
# show_first_ten_raw_bold_nifti()
# show_tasks()
# show_files_by_task('localizer')
# show_first_participant_filename_by_task('localizer')
# show_layout_as_dataframe()

# plot_S01_T1_slice('sagittal')
# plot_S01_T1_slices(9, 'horizontal')
# plot_S01_T1_slices(9, 'sagittal')
# plot_S01_T1_slices(9, 'coronal')

# plot_anat(get_S01_T1_img())
# plot_anat(get_S01_T1_img(), draw_cross=False, display_mode='z')
# plot_glass_brain(get_S01_T1_img())

# amygdala_mask = Brain_Data('https://neurovault.org/media/images/1290/FSL_BAmyg_thr0.nii.gz').to_nifti()
# plot_roi(amygdala_mask, get_S01_T1_img())
# plot_glass_brain(amygdala_mask)

plt.show()