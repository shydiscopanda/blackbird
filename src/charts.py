
from matplotlib.figure import Figure

from src.dt_classes import Record


def create_bar_chart(records: dict[set[Record]]) -> Figure:
    """
    Creates a basic bar chart
    :param records: Set of Records processed from efetch endpoint
    :return: bar chart
    """
    fig = Figure(figsize=(20, 5))
    axis = fig.add_subplot(1, 1, 1)
    axis.set_ylabel("Count")
    axis.set_xlabel("Year")
    year_list = list(records.keys())
    counts = [len(v) for _, v in records.items()]
    axis.bar(year_list, counts, tick_label=year_list, label="COST")
    return fig
