import argparse
import pandas as pd
import matplotlib.pyplot as plt
import adjustText
import numpy as np
import seaborn as sns
import datetime
import logging
import os 
from natsort import natsorted
from collections import Counter
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from collections import defaultdict

def plot_csv_data(csv_file, official_bug_names_csv, x_col, y_col, label_col, title=None, xlabel=None, ylabel=None, dir=None):
    input_dir = os.path.dirname(os.path.abspath(csv_file))
    output_dir = os.path.join(input_dir, f'{dir}')
    os.makedirs(output_dir, exist_ok=True)

    # Configure logging to suppress adjustText output
    logging.getLogger("adjustText").setLevel(logging.ERROR)
    
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    official_bug_names_df = pd.read_csv(official_bug_names_csv, header=None)  # No header row assumed
    official_bug_names = dict(zip(official_bug_names_df[0], official_bug_names_df[1]))  # Convert two columns into key-value pairs

    # Map x values to official bug names
    #x_labels = [official_bug_names.get(str(val), str(val)) for val in official_bug_names]  # Default to the original value if not found
    #x_labels = [f"{official_bug_names.get(str(val), str(val))} ({val})" for val in df[x_col].unique()]
    x_labels = [f"{val}" for val in df[x_col].unique()]

    # Check if the specified columns exist
    if x_col not in df.columns or y_col not in df.columns or label_col not in df.columns:
        print("Error: One or more specified columns not found in the CSV file.")
        print("Available columns:", df.columns.tolist())
        return
    
    ## Extract data
    x = df[x_col]
    y = df[y_col].astype(float)
    labels = df[label_col]

    # Group all data points by (x, y)
    xy_to_indices = defaultdict(list)
    for i, (xi, yi) in enumerate(zip(x, y)):
        xy_to_indices[(xi, yi)].append(i)

    # Set up the plot
    plt.figure(figsize=(5, 3))
    unique_labels = natsorted(labels.unique())
    palette = dict(zip(unique_labels, sns.color_palette("tab20", len(unique_labels))))

    legend_handles = []

    # Draw each group of overlapping points as concentric circles
    for (xi, yi), indices in xy_to_indices.items():
        # Sort indices so that colors appear in a consistent order (e.g., by label)
        sorted_indices = sorted(indices, key=lambda i: unique_labels.index(labels.iloc[i]))
        n = len(sorted_indices)
        
        for rank, i in enumerate(sorted_indices):
            label = labels.iloc[i]
            color = palette[label]
            size = 50 * (1 - 0.8 * (rank / (n - 1))) if n > 1 else 50  # smaller size for later circles
            plt.scatter(xi, yi, s=size, color=color, alpha=0.9)

    # One legend entry per label (uniform size)
    for label in unique_labels:
        legend_handles.append(Line2D([0], [0], marker='o', color='w',
                                    markerfacecolor=palette[label], markersize=8,
                                    label=label))

    plt.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5), title=label_col)
    '''
    scatter = plt.scatter(x, y, c=palette)
    
   # Annotate points with labels without overlapping
    
    texts = []
    for i, label in enumerate(labels):
        texts.append(plt.text(x[i], y[i], label, fontsize=12, color=palette[i]))
    
    #adjustText.adjust_text(texts, expand_points=(1.2, 1.5), expand_text=(1.2, 1.5), force_points=(0.3, 0.5), force_text=(0.3, 0.5), arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
    '''
    # Set axis labels and title
    plt.xlabel(xlabel if xlabel else x_col)
    plt.ylabel(ylabel if ylabel else y_col)
    #plt.title(title if title else f"Scatter Plot of {y_col} vs {x_col}")
    
    # Set new x-axis labels in the scatter plot
    plt.xticks(ticks=np.arange(len(x_labels)), labels=x_labels, rotation=25, ha="right")

    # Use tight layout to adjust labels and prevent clipping
    plt.tight_layout()

    # Save the scatter plot with a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_title = f"{title.replace(" ", "_")}_scatter" if title else f"scatter_plot"
    scatter_filename = f"{filename_title}_{timestamp}.svg"
    plt.savefig(os.path.join(output_dir, scatter_filename), dpi=300, bbox_inches='tight')
    scatter_filename = f"{filename_title}_{timestamp}.png"
    plt.savefig(os.path.join(output_dir, scatter_filename), dpi=300, bbox_inches='tight')
    scatter_filename = f"{filename_title}_{timestamp}.pdf"
    plt.savefig(os.path.join(output_dir, scatter_filename), dpi=300, bbox_inches='tight')
    print(f"Scatter plot saved as {scatter_filename}")
    
    # Show the scatter plot
    plt.show()
    
    # Create the box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x, y=y, color='lightblue')
    
    # Set axis labels and title
    plt.xlabel(xlabel if xlabel else x_col)
    plt.ylabel(ylabel if ylabel else y_col)
    plt.title(title if title else f"Box Plot of {y_col} by {x_col}")
    
    # Set new x-axis labels in the scatter plot
    plt.xticks(ticks=np.arange(len(x_labels)), labels=x_labels, rotation=45, ha="right")

    # Use tight layout to adjust labels and prevent clipping
    plt.tight_layout()

    # Save the box plot with a timestamped filename
    filename_title = f"{title.replace(" ", "_")}_box" if title else f"box_plot"
    boxplot_filename = f"{filename_title}_{timestamp}.svg"
    plt.savefig(os.path.join(output_dir, boxplot_filename), dpi=300, bbox_inches='tight')
    boxplot_filename = f"{filename_title}_{timestamp}.png"
    plt.savefig(os.path.join(output_dir, boxplot_filename), dpi=300, bbox_inches='tight')
    print(f"Box plot saved as {boxplot_filename}")
    
    # Show the box plot
    plt.show()

def main():
    # TODO: change name of directory created for saving 
    parser = argparse.ArgumentParser(description="Plot data from a CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument('official_bug_names_csv', type=str, help='Path to the CSV file containing official bug names mapping.')
    parser.add_argument("x_col", help="Column name for x-axis")
    parser.add_argument("y_col", help="Column name for y-axis")
    parser.add_argument("label_col", help="Column name for data point labels")
    parser.add_argument("--title", help="Title for the plot", default=None)
    parser.add_argument("--xlabel", help="Label for the x-axis", default=None)
    parser.add_argument("--ylabel", help="Label for the y-axis", default=None)
    parser.add_argument("--dir", help="Directory name", default="uniq_methods")
    
    args = parser.parse_args()
    
    plot_csv_data(args.csv_file, args.official_bug_names_csv, args.x_col, args.y_col, args.label_col, args.title, args.xlabel, args.ylabel, args.dir)

if __name__ == "__main__":
    main()
