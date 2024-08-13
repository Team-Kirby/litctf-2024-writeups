from collections import Counter

import requests

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def sort_by_closest_color(counter):
    """Sort colors by closest color in RGB space."""
    # Convert hex colors to RGB
    rgb_colors = [hex_to_rgb(color) for color in counter.keys()]
    sorted_colors = [rgb_colors.pop(0)]

    while rgb_colors:
        last_color = sorted_colors[-1]
        # Find the closest color by Euclidean distance
        closest_index = min(range(len(rgb_colors)), key=lambda i: distance.euclidean(last_color, rgb_colors[i]))
        closest_color = rgb_colors.pop(closest_index)
        sorted_colors.append(closest_color)

    # Convert sorted RGB colors back to hex
    sorted_hex_colors = ['#%02x%02x%02x' % color for color in sorted_colors]

    # Reconstruct the sorted list considering the original frequency
    result = []
    for hex_color in sorted_hex_colors:
        result.extend([hex_color] * counter[hex_color])

    return result


def display_color_image(color_array):
    """Display a 100x100 array of colors as an image."""
    # Convert hex to RGB and reshape to 100x100x3
    rgb_array = np.array([hex_to_rgb(color) for color in color_array]).reshape(100, 100, 3)

    # Normalize the RGB values to [0, 1] range for matplotlib
    rgb_array = rgb_array / 255.0

    # Display the image
    plt.imshow(rgb_array)
    plt.axis('off')  # Turn off the axis
    plt.show()


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def send_solution(solution):
    payload = {"data": solution}
    r = requests.post("http://litctf.org:31780/test", json=payload)
    return r.text


if __name__ == "__main__":
    with open("data.txt", "r") as f:
        data = eval(f.read())

    solution = []
    counter = Counter(data)

    arr = counter.most_common()[::-2] + counter.most_common()[1::2]
    last_color = hex_to_rgb(arr[0][0])
    for i in range(1, 99):
        a1 = hex_to_rgb(arr[i][0])
        a2 = hex_to_rgb(arr[-1-i][0])
        d1 = distance.euclidean(last_color, a1)
        d2 = distance.euclidean(last_color, a2)
        if d2 < d1:
            t = arr[i]
            arr[i] = arr[-i-1]
            arr[-i-1] = t

        last_color = hex_to_rgb(arr[i][0])
    i = 0
    for v, count in arr:
        r = min(i, 99)
        c = max(0, i - 99)
        all_pos = find(data, v)
        for j in range(count):
            pos = r + c * 100
            p = all_pos[j]
            if data[pos] != v:
                solution.append([pos, p])
                t = data[p]
                data[p] = data[pos]
                data[pos] = t
            r -= 1
            c += 1

        i += 1

    display_color_image(data)
    print(send_solution(solution))