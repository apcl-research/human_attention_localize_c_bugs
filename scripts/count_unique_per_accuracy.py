import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os
import math
import numpy as np 
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

def plot_histograms_from_csv(csv_file, output_dir):
    df = pd.read_csv(csv_file)

    # Only keep the rating columns (skip "Bug" and "Participant ID")
    rating_columns = df.columns[2:]

    for col in rating_columns:
        values = df[col]
        num_xs = sum(values == 'X')
        num_rounded = 0 

        # Dictionary to hold ratings and corresponding Bug+Participant IDs
        grouped_data = {i: [] for i in range(1, 6)}

        for idx, val in values.items():
            if val == 'X':
                continue
            try:
                val = float(val)

                if val == 0:
                    floored_val = 1
                    num_rounded += 1
                else:
                    floored = math.floor(val)
                    floored_val = max(1, min(5, floored))
                    if floored != val:
                        num_rounded += 1

                bug = str(df.loc[idx, 'Bug'])
                pid = str(df.loc[idx, 'Participant ID'])
                grouped_data[floored_val].append(f"{bug}+{pid}")
            except ValueError:
                continue

        # Prepare bar chart
        plt.figure(figsize=(3.71475, 2.29395))
        bins = [1, 2, 3, 4, 5]
        heights = [len(grouped_data[b]) for b in bins]
        bars = plt.bar(bins, heights, tick_label=bins)

        # Add labels inside each bar
        # for bar, b in zip(bars, bins):
        #     entries = grouped_data[b]
        #     if entries:
        #         label = '\n'.join(entries)
        #         plt.text(
        #             bar.get_x() + bar.get_width() / 2,
        #             bar.get_height() / 2,
        #             label,
        #             ha='center',
        #             va='center',
        #             fontsize=8,
        #             #rotation=90  # Vertical text to fit better
        #         )

        # Title
        title = col
        if num_xs > 0:
            title += f" ({num_xs} No Rating)"
        #plt.title(f'Histogram for {title}')
        xlabel= plt.xlabel(f'{num_xs} Tasks Not Rated\n {num_rounded} Rounded (floors .5→int, 0→1)', fontsize=14)
        xlabel.set_position((0.47, 0.50))  # move to the left 
        ylabel = plt.ylabel('Num Tasks', fontsize=14)
        ylabel.set_position((-0.3, 0.40))  # Lower than default
        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        plt.subplots_adjust(left=0.17, right=0.99, top=0.95, bottom=0.35)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        #plt.tight_layout()
        #plt.show()
        plt.savefig(os.path.join(output_dir, f"{col}_histogram.pdf"))

def count_unique_by_accuracy(csv_path):
    df = pd.read_csv(csv_path)

    # Group by Where_Accuracy and count unique Bug and Participant ID
    result = df.groupby('Where_Accuracy').agg({
        'Bug': pd.Series.nunique,
        'Participant ID': pd.Series.nunique
    }).reset_index()

    # Create the summary with two rows: one for unique participants and one for unique bugs
    summary = pd.DataFrame({
        'Where_Accuracy': result['Where_Accuracy'],
        'Unique_Participant_Count': result['Participant ID'],
        'Unique_Bug_Count': result['Bug']
    })

    # Restructure the DataFrame so that the columns start from Where_Accuracy and the rows are the counts
    summary = summary.set_index('Where_Accuracy').T

    return df, summary

def plot_stacked_histogram(df, group_col, count_col, title, output_path):
    # 1) Keep original floats, mark rows that need rounding
    df = df.copy()
    df['orig_acc'] = df['Where_Accuracy'].astype(float)
    df['Rounded'] = df['orig_acc'].apply(lambda x: True if x == 0 or not x.is_integer() else False)

    # 2) Map: 0→1, else floor down
    df['Where_Accuracy'] = df['orig_acc'].apply(lambda x: 1 if x == 0 else int(math.floor(x)))

    # 3) Define integer x-axis levels
    accuracy_levels = np.arange(1, 6)   # [1,2,3,4,5]
    step = 1
    bar_width = step * 0.8

    # 4) Sort participants naturally: p1, p2, …, p9, p10, p11
    def pid_key(pid):
        return int(''.join(filter(str.isdigit, pid)))
    participants = sorted(df[group_col].dropna().unique(), key=pid_key)

    # 5) Colors from a qualitative map
    cmap = plt.get_cmap('tab20')
    colors = cmap.colors[:len(participants)]

    # 6) Pivot counts and pivot rounded‐flags
    counts = (
        df
        .groupby(['Where_Accuracy', group_col])[count_col]
        .nunique()
        .unstack(fill_value=0)
        .reindex(accuracy_levels, fill_value=0)
    )
    rounds = (
        df[df['Rounded']]
        .groupby(['Where_Accuracy', group_col])['Rounded']
        .count()
        .unstack(fill_value=0)
        .reindex(accuracy_levels, fill_value=0)
    )

    # 7) Plot stacked bars and annotate asterisks where rounds>0
    fig, ax = plt.subplots(figsize=(5, 2.5))
    bottom = np.zeros(len(accuracy_levels))

    for idx, participant in enumerate(participants):
        vals = counts.get(participant, pd.Series(0, index=accuracy_levels)).values
        ax.bar(
            accuracy_levels,
            vals,
            bottom=bottom,
            width=bar_width,
            align='center',
            color=colors[idx],
            label=str(participant)
        )

        # annotate "*" for any rounded entries in this segment
        for i, x in enumerate(accuracy_levels):
            if participant in rounds.columns and rounds.at[x, participant] > 0:
                y = bottom[i] + vals[i] / 4
                ax.text(x, y, '*', ha='center', va='center', fontsize=12)

        bottom += vals

    # 8) Final styling
    #ax.set_title(title)
    ax.set_xlabel('Where_Accuracy (floors .5→int, 0→1)')
    ax.set_ylabel(f'Num Tasks')
    ax.set_xticks(accuracy_levels)
    ax.legend(title=group_col, bbox_to_anchor=(1.05, 1.04), loc='upper left', fontsize='small')
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

def plot_histogram_subplots(df, group_col, count_col, title_prefix, output_path):
    groups = df[group_col].unique()
    accuracy_levels = sorted(df['Where_Accuracy'].dropna().unique())
    num_groups = len(groups)
    cols = 3
    rows = math.ceil(num_groups / cols)

    # Precompute consistent y-axis limit
    all_counts = []
    for group in groups:
        group_df = df[df[group_col] == group]
        counts = group_df.groupby('Where_Accuracy')[count_col].nunique()
        all_counts.extend(counts.values)

    y_max = max(all_counts) if all_counts else 1

    fig, axs = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4), squeeze=False)

    for idx, group in enumerate(groups):
        row, col = divmod(idx, cols)
        ax = axs[row][col]

        group_df = df[df[group_col] == group]
        counts = group_df.groupby('Where_Accuracy')[count_col].nunique()
        counts = counts.reindex(accuracy_levels, fill_value=0).reset_index()
        counts.columns = ['Where_Accuracy', count_col]

        ax.bar(counts['Where_Accuracy'], counts[count_col], color='skyblue')
        ax.set_title(f'{title_prefix}: {group}')
        ax.set_xlabel('Where_Accuracy')
        ax.set_ylabel(f'Num Unique {count_col}s')
        ax.set_ylim(0, y_max + 1)
        ax.set_xticks(accuracy_levels)
        ax.tick_params(axis='x', rotation=45)

    # Remove unused subplots
    for i in range(num_groups, rows * cols):
        row, col = divmod(i, cols)
        fig.delaxes(axs[row][col])

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_line_graph(df, group_col, count_col, title, output_path):
    groups = df[group_col].unique()
    accuracy_levels = sorted(df['Where_Accuracy'].dropna().unique())

    plt.figure(figsize=(10, 6))
    for group in groups:
        group_df = df[df[group_col] == group]
        counts = group_df.groupby('Where_Accuracy')[count_col].nunique()
        counts = counts.reindex(accuracy_levels, fill_value=0).reset_index()
        counts.columns = ['Where_Accuracy', count_col]

        plt.plot(counts['Where_Accuracy'], counts[count_col], label=group, marker='o')

    plt.title(f'{title}: Unique {count_col}s per Where_Accuracy')
    plt.xlabel('Where_Accuracy')
    plt.ylabel(f'Num Unique {count_col}s')
    plt.xticks(accuracy_levels, rotation=45)
    plt.legend(title=group_col, fontsize='small', loc='upper right')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Analyze Where_Accuracy by Bug and Participant.')
    parser.add_argument('csv_path', type=str, help='Path to the input CSV file')
    parser.add_argument('--output_dir', type=str, default='output_charts', help='Directory to save plots and data')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    plot_histograms_from_csv(args.csv_path, args.output_dir) 

    df, summary = count_unique_by_accuracy(args.csv_path)

    # Save summary dataframe to CSV
    summary_path = os.path.join(args.output_dir, 'where_accuracy_summary.csv')
    summary.to_csv(summary_path)
    print(f"Saved summary CSV to {summary_path}")

    # Generate Bug-based charts
    print("Creating bug-based plots...")
    plot_histogram_subplots(
        df, group_col='Bug', count_col='Participant ID',
        title_prefix='Bug',
        output_path=os.path.join(args.output_dir, 'bug_histograms_subplot.png')
    )
    plot_line_graph(
        df, group_col='Bug', count_col='Participant ID',
        title='Participants per Where_Accuracy by Bug',
        output_path=os.path.join(args.output_dir, 'bug_accuracy_line_plot.png')
    )

    # Generate Participant-based charts
    print("Creating participant-based plots...")
    plot_histogram_subplots(
        df, group_col='Participant ID', count_col='Bug',
        title_prefix='Participant',
        output_path=os.path.join(args.output_dir, 'participant_histograms_subplot.png')
    )
    plot_line_graph(
        df, group_col='Participant ID', count_col='Bug',
        title='Bugs per Where_Accuracy by Participant',
        output_path=os.path.join(args.output_dir, 'participant_accuracy_line_plot.png')
    )
     # Pivot tables for additional CSVs
    bug_pivot = df.groupby(['Bug', 'Where_Accuracy'])['Participant ID'].nunique().unstack(fill_value=0)
    bug_pivot.to_csv(os.path.join(args.output_dir, 'bug_accuracy_counts.csv'))
    print("Saved bug pivot table to bug_accuracy_counts.csv")

    participant_pivot = df.groupby(['Participant ID', 'Where_Accuracy'])['Bug'].nunique().unstack(fill_value=0)
    participant_pivot.to_csv(os.path.join(args.output_dir, 'participant_accuracy_counts.csv'))
    print("Saved participant pivot table to participant_accuracy_counts.csv")
    plot_stacked_histogram(
        df, group_col='Participant ID', count_col='Bug',
        title='Stacked Bar Chart of Bugs per Where_Accuracy by Participant',
        output_path=os.path.join(args.output_dir, 'participant_stacked_bar.pdf')
    )

    print(f"\nAll charts and summary CSVs saved in: {args.output_dir}")


if __name__ == '__main__':
    main()
