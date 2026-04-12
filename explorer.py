import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from pathlib import Path

def explore_melt_pool_h5(file_path, num_samples=3):
    """
    Explores the structure of the Melt-Pool-Kinetics HDF5 file 
    and visualizes sample images.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"Error: File not found at {file_path}")
        return
    if not file_path.is_file():
        print(f"Error: Expected an .h5 file, got a directory: {file_path}")
        return

    with h5py.File(file_path, 'r') as h5f:
        print(f"--- Exploring HDF5: {file_path.name} ---")
        
        # 1. Recursive function to print the internal tree structure
        def print_structure(name, obj):
            indent = "  " * name.count('/')
            if isinstance(obj, h5py.Dataset):
                print(f"{indent}Dataset: {name} | Shape: {obj.shape} | Type: {obj.dtype}")
            else:
                print(f"{indent}Group: {name}")

        print("\nInternal Structure (First 20 items):")
        # We limit the print so it doesn't scroll forever if there are thousands of groups
        count = 0
        for name in h5f:
            if count > 20: break
            print_structure(name, h5f[name])
            if isinstance(h5f[name], h5py.Group):
                for sub_name in h5f[name]:
                    print_structure(f"{name}/{sub_name}", h5f[name][sub_name])
            count += 1

        # 2. Visualizing Samples
        # Note: We assume the images are stored in datasets. 
        # We'll search for the first available dataset with 2D or 3D shape.
        print("\n--- Visualizing Samples ---")
        datasets = []
        h5f.visititems(lambda name, obj: datasets.append(name) if isinstance(obj, h5py.Dataset) else None)

        if not datasets:
            print("No datasets found in the file.")
            return

        plt.figure(figsize=(15, 5))
        for i in range(min(num_samples, len(datasets))):
            ds_name = datasets[i]
            data = h5f[ds_name]
            
            # Melt pool data is often (Frames, Height, Width) or (Height, Width)
            # We take the first frame if it's a sequence
            if len(data.shape) == 3:
                img = data[0, :, :]
            elif len(data.shape) == 2:
                img = data[:, :]
            else:
                continue

            plt.subplot(1, num_samples, i+1)
            plt.imshow(img, cmap='hot')
            plt.title(f"Source: {ds_name.split('/')[0]}\nShape: {img.shape}")
            plt.axis('off')
            
            # Print attributes if they exist (Power, Speed, etc.)
            if data.attrs:
                print(f"\nMetadata for {ds_name}:")
                for attr_name, attr_val in data.attrs.items():
                    print(f"  {attr_name}: {attr_val}")

        plt.tight_layout()
        out_path = Path.cwd() / "h5_preview_samples.png"
        plt.savefig(out_path, dpi=150)
        print(f"\nSaved sample preview image to: {out_path}")
        plt.close()

if __name__ == "__main__":
    explore_melt_pool_h5(r"M:\Melt-Pool-Kinetics A multi-source melt pool compilation for vision-based analytics applications in additive manufacturing\Final_DatasetV3.h5")

# Update this path to where your 48GB file is stored (e.g., in Drive or Local)
# H5_PATH = "/content/drive/MyDrive/Melt-Pool-Kinetics.h5"
# explore_melt_pool_h5(H5_PATH)
