import h5py
import matplotlib.pyplot as plt
import numpy as np
import os

def browse_h5_source(file_path, target_source=None, frames_to_show=5):
    """
    A more robust browser for the 48GB Melt-Pool-Kinetics dataset.
    If target_source is None, it lists all available paths.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with h5py.File(file_path, 'r') as h5f:
        # 1. Map all datasets in the file
        dataset_paths = []
        h5f.visititems(lambda name, obj: dataset_paths.append(name) if isinstance(obj, h5py.Dataset) else None)

        if target_source is None:
            print("--- Available Datasets (First 100) ---")
            for path in dataset_paths[:100]:
                shape = h5f[path].shape
                print(f"Path: {path} | Shape: {shape}")
            print("\nUsage: Call browse_h5_source(file_path, target_source='source10/NIST4X')")
            return

        # 2. Visualize a specific source
        # Find the actual dataset path that contains the target_source string
        actual_path = next((p for p in dataset_paths if target_source in p), None)
        
        if not actual_path:
            print(f"Could not find source matching: {target_source}")
            return

        data = h5f[actual_path]
        print(f"\n--- Visualizing: {actual_path} ---")
        print(f"Total Frames available: {data.shape[0] if len(data.shape)>2 else 1}")

        # Determine how to plot based on shape (Rank 2 or 3)
        plt.figure(figsize=(20, 4))
        if len(data.shape) == 3: # (Frames, Height, Width)
            total_frames = data.shape[0]
            indices = np.linspace(0, total_frames - 1, frames_to_show, dtype=int)
            
            for i, idx in enumerate(indices):
                plt.subplot(1, frames_to_show, i + 1)
                plt.imshow(data[idx, :, :], cmap='magma')
                plt.title(f"Frame {idx}")
                plt.axis('off')
        
        elif len(data.shape) == 2: # Single Image
            plt.imshow(data[:, :], cmap='magma')
            plt.title("Single Frame Dataset")
            plt.axis('off')

        plt.suptitle(f"Source: {actual_path}")
        plt.tight_layout()
        plt.show()

        # 3. Print Metadata (Attributes)
        if data.attrs:
            print("\nMetadata Attributes:")
            for k, v in data.attrs.items():
                print(f"  {k}: {v}")

if __name__ == "__main__":
    browse_h5_source(r'M:\Melt-Pool-Kinetics A multi-source melt pool compilation for vision-based analytics applications in additive manufacturing\Final_DatasetV3.h5')


# Example Usage (Run this in a cell):
# browse_h5_source(H5_PATH, target_source='source18/223W_33mms')