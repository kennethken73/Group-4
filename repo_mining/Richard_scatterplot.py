import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def generate_scatter_plot(csv_file):
    # load the data from the CSV
    data = pd.read_csv(csv_file)
    
    # convert date to datetime format
    data["Date"] = pd.to_datetime(data["Date"])

    # find the project start date (earliest commit)
    project_start = data["Date"].min()

    # compute weeks since the project started
    data["Week"] = ((data["Date"] - project_start).dt.days // 7) + 1

    # assign a unique color to each author
    authors = data["Author"].unique()
    available_colors = list(mcolors.TABLEAU_COLORS.values())
    color_map = {author: available_colors[i % len(available_colors)] for i, author in enumerate(authors)}

    # ensure new authors get a color if missing in the color_map
    def get_color(author):
        if author not in color_map:
            color_map[author] = available_colors[len(color_map) % len(available_colors)]
        return color_map[author]

    # plot scatter points for each author
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

    plt.title("File Touches by Week and Author", fontsize=16)
    plt.xlabel("Week of the Year", fontsize=14)
    plt.ylabel("Filename", fontsize=14)
    plt.legend(title="Author", fontsize=10, loc="upper right", bbox_to_anchor=(1.2, 1))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":

    csv_file = "data/authors_file_touches.csv"
    generate_scatter_plot(csv_file)
