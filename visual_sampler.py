import h5py
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_visual_atlas(file_path, cols=4):
    """
    Generates a bird's-eye view of the entire HDF5 dataset by plotting 
    one representative frame from every source detected in the file.
    
    Args:
        file_path (str): Path to the Final_DatasetV3.h5 file.
        cols (int): Number of columns in the visualization grid.
    """
    if not os.path.exists(file_path):
        print(f"Error: H5 file not found at {file_path}")
        return

    with h5py.File(file_path, 'r') as h5f:
        # Get all top-level sources (source1, source2, etc.)
        sources = sorted(list(h5f.keys()), key=lambda x: int(x.replace('source', '')) if 'source' in x else 0)
        num_sources = len(sources)
        rows = int(np.ceil(num_sources / cols))

        print(f"Detected {num_sources} sources. Generating Visual Atlas...")

        plt.figure(figsize=(20, 5 * rows))
        plt.suptitle(f"Melt-Pool-Kinetics Visual Atlas ({num_sources} Sources)", fontsize=22, fontweight='bold', y=1.02)

        for i, source_name in enumerate(sources):
            ax = plt.subplot(rows, cols, i + 1)
            
            # Internal search for the first valid image dataset in this source group
            img_path = None
            def find_first_image(name, obj):
                nonlocal img_path
                if img_path is None and isinstance(obj, h5py.Dataset):
                    # Check for 2D or 3D arrays (H, W) or (Frames, H, W)
                    if len(obj.shape) >= 2 and obj.shape[-1] > 1 and obj.shape[-2] > 1:
                        img_path = name

            h5f[source_name].visititems(find_first_image)

            if img_path:
                full_key = f"{source_name}/{img_path}"
                ds = h5f[full_key]
                
                # Logic to grab the first frame regardless of rank
                try:
                    if len(ds.shape) == 4: # RGB Video (F, H, W, C)
                        sample_img = ds[0, :, :, :]
                    elif len(ds.shape) == 3: # Mono Video (F, H, W)
                        sample_img = ds[0, :, :]
                    else: # Static Image (H, W)
                        sample_img = ds[:, :]

                    # Plotting logic
                    plt.imshow(sample_img, cmap='magma' if len(sample_img.shape) == 2 else None)
                    plt.title(f"{source_name}\nRes: {sample_img.shape}", fontsize=14, fontweight='bold')
                    
                    # Add labels for sensor type if available in attributes
                    if 'AMInsituDataSensorType' in ds.attrs:
                        plt.xlabel(f"Sensor: {ds.attrs['AMInsituDataSensorType']}", fontsize=10)
                except Exception as e:
                    plt.text(0.5, 0.5, "Corrupt/Incompatible", ha='center')
            else:
                plt.text(0.5, 0.5, "No Image Data", ha='center', color='red')
                plt.title(f"{source_name} (Empty)")

            plt.axis('off')

        plt.tight_layout()
        # Save a high-res version to the project folder for reference
        plt.savefig("h5_visual_atlas.png", dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    # You can update this path to your actual H5 location
    H5_PATH = "../Final_DatasetV3.h5" 
    generate_visual_atlas(H5_PATH)