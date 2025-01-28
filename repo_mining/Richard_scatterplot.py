import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def generate_scatter_plot(csv_file):
    # Load the data from the CSV
    data = pd.read_csv(csv_file)
    
    # Convert dates to weeks
    data["Week"] = pd.to_datetime(data["Date"]).dt.isocalendar().week

    # Assign a unique color to each author
    authors = data["Author"].unique()
    available_colors = list(mcolors.TABLEAU_COLORS.values())
    color_map = {author: available_colors[i % len(available_colors)] for i, author in enumerate(authors)}

    # Ensure new authors get a color if missing in the color_map
    def get_color(author):
        if author not in color_map:
            color_map[author] = available_colors[len(color_map) % len(available_colors)]
        return color_map[author]

    # Plot scatter points for each author
    plt.figure(figsize=(12, 8))
    for author, group in data.groupby("Author"):
        plt.scatter(
            group["Week"],
            group["Filename"],
            label=author,
            color=get_color(author),
            alpha=0.6,
            edgecolors="w",
            s=100,
        )

    # Configure plot labels and legend
    plt.title("File Touches by Week and Author", fontsize=16)
    plt.xlabel("Week of the Year", fontsize=14)
    plt.ylabel("Filename", fontsize=14)
    plt.legend(title="Author", fontsize=10, loc="upper right", bbox_to_anchor=(1.2, 1))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    # Replace with the path to your CSV file
    csv_file = "data/authors_file_touches.csv"
    generate_scatter_plot(csv_file)
