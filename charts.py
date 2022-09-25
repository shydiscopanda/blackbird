
from matplotlib.figure import Figure

from search import Record


def create_bar_chart(records):
    fig = Figure(figsize=(20, 5))
    axis = fig.add_subplot(1, 1, 1)
    axis.set_ylabel("Count")
    axis.set_xlabel("Year")
    year_list = list(records.keys())
    counts = [len(v) for _, v in records.items()]
    axis.bar(year_list, counts, tick_label=year_list, label="COST")
    return fig


if __name__ == "__main__":
    create_bar_chart({
        2001: {Record(pdate_year=2001, pmid='18968352'), Record(pdate_year=2001, pmid='18968180'), Record(pdate_year=2001, pmid='18763098'), Record(pdate_year=2001, pmid='18968382')},
        2002: {Record(pdate_year=2002, pmid='18924732')}
    })
