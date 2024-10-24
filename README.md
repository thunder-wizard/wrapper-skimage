# wrapper-skimage
Image Wrap Tool using Thin Plate Spline Transform

# Usage
## Get warpping image
- Copy the design image with clipping rightly like sample.
python .\ski-convert.py --image_path [image_path] --index [template_index]
python .\ski-convert.py --image_path .\input\input-1.png --index 1  

## Get src-dst data
python .\coordinate.py [input_image_path] [target_image_path] [index_tag]
python .\coordinate.py .\input\input-1.png .\template\template-1.jpg 1

-Left click to add point, the adding order will be matched for det and src...

# Warning!!!
- The number of src and dst points must be the same.
- Match the image and template index correctly.
- When you use coordinate.py you cant add a new point in 10px from existed points.