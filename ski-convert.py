import argparse
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, transform
from datetime import datetime
import json

def add_alpha_channel_to_jpg(image):
    if image.shape[2] == 4:
        print("The image already has an alpha channel (RGBA).")
        return image
    
    alpha_channel = np.ones((image.shape[0], image.shape[1], 1), dtype=np.uint8) * 255
    return np.concatenate([image, alpha_channel], axis=2)

def thin_plate_spline_transform(image, src_points, dst_points):
    tps = transform.ThinPlateSplineTransform()
    tps.estimate(dst_points, src_points)

    h, w = image.shape[:2]

    if image.shape[2] == 3:
        image = add_alpha_channel_to_jpg(image)

    warped_image = transform.warp(image, tps, output_shape=(h, w), mode='constant', cval=0)

    output_image = np.zeros((h, w, 4), dtype=np.uint8)
    output_image[..., :3] = (warped_image[..., :3] * 255).astype(np.uint8)
    output_image[..., 3] = (warped_image[..., 3] > 0).astype(np.uint8) * 255
    return output_image

def load_points_from_json(file_path):
    with open(file_path, 'r') as f:
        points = json.load(f)
    return np.array(points)

def main(image_path, index):
    image = io.imread(f"{image_path}")
    src_points = load_points_from_json(f"points/origin-{index}.json")
    dst_points = load_points_from_json(f"points/target-{index}.json")

    warped_image = thin_plate_spline_transform(image, src_points, dst_points)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.png"
    io.imsave(filename, warped_image)

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(image)
    ax[0].set_title('Original Image')
    ax[0].axis('off')
    
    ax[1].imshow(warped_image)
    ax[1].set_title('Warped Image')
    ax[1].axis('off')

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an image with Thin Plate Spline transformation.')
    parser.add_argument('--image_path', type=str, required=True, help='Path to the input image.')
    parser.add_argument('--index', type=int, required=True, help='Path to the input image.')

    args = parser.parse_args()
    main(args.image_path, args.index)
