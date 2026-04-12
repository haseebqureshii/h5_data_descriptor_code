import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def load_metadata_table(metadata_path):
    path = Path(metadata_path)
    suffix = path.suffix.lower()

    if suffix in [".xlsx", ".xls"]:
        try:
            return pd.read_excel(path)
        except ImportError as exc:
            raise ImportError(
                "Excel file detected but openpyxl is not installed. "
                "Run: pip install openpyxl"
            ) from exc
    return pd.read_csv(path)

def generate_dataset_dashboard(metadata_path):
    # 1. Load the metadata
    df = load_metadata_table(metadata_path)
    
    # Clean up DataSize (ensure it's numeric)
    df['DataSize'] = pd.to_numeric(df['DataSize'], errors='coerce').fillna(0)
    
    # Extract the "Source" name from the AMInsituDataID (e.g., 'source1/LMDP' -> 'source1')
    df['Source'] = df['AMInsituDataID'].apply(lambda x: str(x).split('/')[0])

    # Set up the plotting style
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))
    
    # --- CHART 1: Total Frames per Source ---
    source_counts = df.groupby('Source')['DataSize'].sum().sort_values(ascending=False)
    sns.barplot(
        x=source_counts.values,
        y=source_counts.index,
        hue=source_counts.index,
        legend=False,
        ax=axes[0],
        palette="viridis",
    )
    axes[0].set_title('Volume: Total Frames per Source', fontsize=16, fontweight='bold')
    axes[0].set_xlabel('Number of Frames', fontsize=12)
    axes[0].set_ylabel('Source ID', fontsize=12)
    
    # --- CHART 2: Data Distribution by Material ---
    material_counts = df.groupby('MaterialName')['DataSize'].sum().sort_values(ascending=False)
    # Using a pie chart for materials to see market share
    axes[1].pie(material_counts.values, labels=material_counts.index, autopct='%1.1f%%', 
                startangle=140, colors=sns.color_palette("pastel"))
    axes[1].set_title('Material Diversity (By Frame Count)', fontsize=16, fontweight='bold')

    # --- CHART 3: Sensor Type Variety ---
    sensor_counts = df.groupby('AMInsituDataSensorType')['DataSize'].sum().sort_values(ascending=False)
    sns.barplot(
        x=sensor_counts.values,
        y=sensor_counts.index,
        hue=sensor_counts.index,
        legend=False,
        ax=axes[2],
        palette="magma",
    )
    axes[2].set_title('Monitoring Conditions: Sensor Types', fontsize=16, fontweight='bold')
    axes[2].set_xlabel('Number of Frames', fontsize=12)
    axes[2].set_ylabel('Sensor Type', fontsize=12)

    plt.tight_layout()
    out_path = Path.cwd() / "dataset_inventory_dashboard.png"
    plt.savefig(out_path, dpi=150)
    print(f"Saved dashboard image to: {out_path}")
    plt.close()

    # --- PRINT SUMMARY TABLE ---
    print("\n--- DATASET SUMMARY TABLE ---")
    summary = df.groupby('Source').agg({
        'DataSize': 'sum',
        'MaterialName': 'first',
        'AMSystemType': 'first',
        'AMInsituDataSensorType': 'first'
    }).sort_values(by='DataSize', ascending=False)
    print(summary)
    return summary

import plotly.express as px
import plotly.graph_objects as go

def generate_topology_plots(summary_df):
    """
    Consumes the summary DataFrame (where Source is the index) and
    generates interactive topology visualizations.
    """
    # Ensure 'Source' is a column for Plotly paths
    viz_df = summary_df.reset_index()
    
    # Mapping metadata column names to shorter display names if necessary
    # (Assuming columns: DataSize, MaterialName, AMSystemType, AMInsituDataSensorType)
    
    # --- VISUALIZATION 1: TreeMap (Volume & Category) ---
    fig1 = px.treemap(
        viz_df, 
        path=[px.Constant("Melt-Pool-Kinetics"), 'MaterialName', 'AMSystemType', 'Source'], 
        values='DataSize',
        color='AMInsituDataSensorType',
        title='Dataset Composition: Volume by Material, System, and Sensor',
        color_discrete_sequence=px.colors.qualitative.Dark2,
        hover_data=['AMInsituDataSensorType']
    )
    fig1.update_traces(textinfo="label+value")
    treemap_out = Path.cwd() / "dataset_topology_treemap.html"
    fig1.write_html(treemap_out)
    print(f"Saved interactive treemap to: {treemap_out}")

    # --- VISUALIZATION 2: Parallel Categories (Flow of Logic) ---
    fig2 = go.Figure(
        data=[
            go.Parcats(
                dimensions=[
                    dict(label="Material", values=viz_df["MaterialName"]),
                    dict(label="AM System", values=viz_df["AMSystemType"]),
                    dict(label="Sensor", values=viz_df["AMInsituDataSensorType"]),
                ],
                counts=viz_df["DataSize"],
                line={"color": viz_df["DataSize"], "colorscale": "Viridis"},
            )
        ]
    )
    fig2.update_layout(title="Dataset Logic Flow: How Attributes Interconnect")
    parcats_out = Path.cwd() / "dataset_topology_parallel_categories.html"
    fig2.write_html(parcats_out)
    # Assuming fig1 (Treemap) and fig2 (Parallel) are your Plotly objects
    fig1.write_html("treemap.html", full_html=False, include_plotlyjs='cdn')
    fig2.write_html("parallel.html", full_html=False, include_plotlyjs='cdn')
    print(f"Saved interactive parallel categories plot to: {parcats_out}")

if __name__ == "__main__":
    summary_df = generate_dataset_dashboard(r"M:\Melt-Pool-Kinetics A multi-source melt pool compilation for vision-based analytics applications in additive manufacturing\Metadata Revised.xlsx")
    generate_topology_plots(summary_df)
