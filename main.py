from collections import defaultdict
import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage import color

# since there may be some differences, we'll also have a list of colors
def get_colors_dict(raw_colors, colors_list=None): 
    colors_dict = defaultdict(lambda: 0)
    raw_colors.sort()

    curr_color = 0
    delta = np.std(np.diff(raw_colors)) * 2
    prev = raw_colors[0]
    for c in raw_colors:
        if c - prev < delta:
            # appliable here, but will create mistakes when number of colors is not the same
            if colors_list:
                colors_dict[colors_list[curr_color]] += 1
            else:
                colors_dict[prev] += 1 
        else:
            if colors_list:
                curr_color += 1
                colors_dict[colors_list[curr_color]] += 1
            else:
                colors_dict[c] += 1
            prev = c
    return colors_dict


def print_dict(dict):
    for key, value in dict.items():
        print(f'{key}: {value}')


im = plt.imread('balls_and_rects.png')
hsv = color.rgb2hsv(im)[:, :, 0]
bin_im = im.copy()
bin_im = bin_im.mean(2)
bin_im[bin_im > 0] = 1
lb = label(bin_im)
props = regionprops(lb)
colors = []
rects = []
circles = []
for p in props:
    cy, cx = p.centroid    
    color = hsv[int(cy), int(cx)]
    colors.append(color)

    if p.extent == 1:
        rects.append(color)
    else: 
        circles.append(color)

colors_dict = get_colors_dict(colors)
colors_list = list(colors_dict.keys())
rects_dict = get_colors_dict(rects, colors_list)
circles_dict = get_colors_dict(circles, colors_list)

print("All:")
print_dict(colors_dict)
print("\nR:")
print_dict(rects_dict)
print("\nC:")
print_dict(circles_dict)