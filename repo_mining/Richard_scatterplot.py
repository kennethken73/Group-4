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

    # assign a unique number to each filename
    unique_files = sorted(data["Filename"].unique())  # Sort to maintain consistency
    file_to_number = {file: idx for idx, file in enumerate(unique_files, start=1)}
    data["FileNumber"] = data["Filename"].map(file_to_number)

    # assign a unique color to each author
    authors = data["Author"].unique()
    available_colors = list(mcolors.TABLEAU_COLORS.values())
    color_map = {author: available_colors[i % len(available_colors)] for i, author in enumerate(authors)}

    # ensure new authors get a color if missing in the color_map
    def get_color(author):
        if author not in color_map:
            color_map[author] = available_colors[len(color_map) % len(available_colors)]
        return color_map[author]

    # plot activity for each filename
    plt.figure(figsize=(12, 8))
    for author, group in data.groupby("Author"):
        plt.scatter(
            group["FileNumber"],
            group["Week"],
            label=author,
            color=get_color(author),
            alpha=0.6,
            edgecolors="w",
            s=100,
        )

    plt.title("File Modification Activity Over Time", fontsize=16)
    plt.xlabel("File Number", fontsize=14)
    plt.ylabel("Weeks Since Project Start", fontsize=14)
    plt.xticks(ticks=range(1, len(unique_files) + 1, max(1, len(unique_files) // 10)))
    plt.gca().invert_yaxis()
    plt.legend(title="Author", fontsize=10, loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=1)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":

    csv_file = "data/authors_file_touches.csv"
    generate_scatter_plot(csv_file)
