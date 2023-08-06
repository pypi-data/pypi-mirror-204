# DeepSea 

This work presents a versatile and trainable deep-learning-based software, termed DeepSea, that allows for both segmentation and tracking of single cells in sequences of phase-contrast live microscopy images.


### Datasets

To download our datasets go to https://deepseas.org/datasets/ or:

* Link to [Original annotated dataset](https://drive.google.com/drive/folders/13RhhBAetSWkjySyhJcDqj_FaO09hxkhO?usp=sharing)

* Link to [dataset example for cell segmentation](https://drive.google.com/drive/folders/1gJIkwUQEtut4JCCoUXUcKUWp2gVYxQ9P?usp=sharing)

* Link to [dataset example for cell tracking](https://drive.google.com/drive/folders/17n0Ex8NQS-REB5ZAMlntVnYBnSmZJtLR?usp=sharing)


### Usage
* #### Example of single cell image segmentation

```
from deepsea.test_single_image_segmentation import apply_img_segmentation
import cv2
import os

output_dir='test_results/'
img = cv2.imread("segmentation_dataset/test/images/A11_z016_c001.png",0)
label_img,binary_mask,overlay_img,img=apply_img_segmentation(img)
cv2.imwrite(os.path.join(output_dir, 'label_img.png'), label_img)
cv2.imwrite(os.path.join(output_dir, 'binary_mask.png'), binary_mask)
cv2.imwrite(os.path.join(output_dir, 'overlay_img.png'), overlay_img)
cv2.imwrite(os.path.join(output_dir, 'original_img_resized.png'), img)

```
* #### Example of tracking the single set of cell image sequences

```
from deepsea.test_single_set_tracking import apply_cell_tracking
import cv2
import os

single_image_set_dir="tracking_dataset/test/set_13_MESC/images/"
output_dir='test_results/'
img_list=[]
for img_name in sorted(os.listdir(single_image_set_dir)):
    img_list.append(cv2.imread(os.path.join(single_image_set_dir,img_name),0))

cell_labels,cell_centroids,tracked_imgs=apply_cell_tracking(img_list)
if tracked_imgs:
    for id, img in enumerate(tracked_imgs):
        cv2.imwrite(os.path.join(output_dir, 'img_{:04d}.png'.format(id)), img)
```

### DeepSea GUI Software
Our DeepSea software is available on https://deepseas.org/software/ 
with examples and instructions. DeepSea software is a user-friendly and automated software designed
to enable researchers to 1) load and explore their phase-contrast cell images in a 
high-contrast display, 2) detect and localize cell bodies using the pre-trained DeepSea 
segmentation model, 3) track and label cell lineages across the frame sequences using the pre-trained 
DeepSea tracking model, 4) manually correct the DeepSea models' outputs using user-friendly editing 
options, 5) train a new model with a new cell type dataset if needed, 6) save the results and cell label 
and feature reports on the local system. It employs our latest trained DeepSea models in the segmentation and tracking processes.
It employs our last trained DeepSea models in the segmentation and tracking processes.

### Useful Information
If you have any questions, contact us at abzargar@ucsc.edu.

