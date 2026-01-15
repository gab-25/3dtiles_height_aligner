import argparse
import json

from pyproj import Transformer


def align_tileset_to_ground(input_path, output_path, manual_height=None):
    with open(input_path, 'r') as f:
        tileset = json.load(f)

    try:
        bounding_box = tileset['root']['boundingVolume']['box']
        x_ecef = bounding_box[0]
        y_ecef = bounding_box[1]
        z_ecef = bounding_box[2]
        print(f"Coordinates read from file: X={x_ecef}, Y={y_ecef}, Z={z_ecef}")
    except (KeyError, IndexError):
        print("Error: Could not find coordinates in root.boundingVolume.box format")
        return

    to_geodetic = Transformer.from_crs("EPSG:4978", "EPSG:4326")

    to_ecef = Transformer.from_crs("EPSG:4326", "EPSG:4978")

    lat, lon, alt_attuale = to_geodetic.transform(x_ecef, y_ecef, z_ecef)
    print(f"Detected position: Lat {lat:.5f}, Lon {lon:.5f}")

    if manual_height is not None:
        target_height = manual_height
        print(f"Using manual target height: {target_height} meters")
    else:
        target_height = alt_attuale
        print(f"Current detected height: {alt_attuale:.2f} meters")

    x_target, y_target, z_target = to_ecef.transform(lat, lon, target_height)
    dx = x_target - x_ecef
    dy = y_target - y_ecef
    dz = z_target - z_ecef

    transform_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        dx, dy, dz, 1.0
    ]

    tileset['root']['transform'] = transform_matrix

    with open(output_path, 'w') as f:
        json.dump(tileset, f, indent=2)

    print("-" * 30)
    print(f"SUCCESS: New file saved as '{output_path}'")
    print(f"The model has been lowered by {target_height:.2f} meters to touch the ground.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Align 3D tileset to ground level')
    parser.add_argument('path', type=str, help='Path to the input tileset.json file')
    parser.add_argument('--height', type=float, help='Manual target height (bypasses automatic ground alignment)',
                        default=None)
    args = parser.parse_args()

    input_path = args.path
    output_path = input_path.replace('.json', '_aligned.json')

    align_tileset_to_ground(input_path, output_path, args.height)
