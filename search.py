from collections import defaultdict
from dataclasses import dataclass
from io import StringIO
from math import ceil
from re import findall
from xml.etree.ElementTree import iterparse

import requests as requests

from url_builder import get_fetch_url, get_query_url


@dataclass
class Record:
    pdate_year: int = 0
    pmid: str = None

    def __hash__(self):
        return hash(self.pmid)


@dataclass
class Flags:
    pubdate: bool = False


RECORDS = None


def process_records(xml_response, loop, loops):

    record, flags = None, None

    for event, elem in iterparse(StringIO(xml_response), events=["start", "end"]):
        label = elem.tag

        if event == 'start':
            if label in ["PubmedArticle", "PubmedBookArticle"]:
                record = Record()
                flags = Flags()

            if label in ["ArticleDate", "PubDate"]:
                flags.pubdate = True

        else:
            if flags.pubdate and label in ["Year", "MedlineDate"]:
                new_year = int(elem.text.strip()) if label == "Year" else int(findall(r'\d{4}', elem.text)[0])
                curr_date = record.pdate_year
                record.pdate_year = new_year if curr_date == 0 or new_year < curr_date else curr_date

            if label == "PMID":
                record.pmid = elem.text.strip()

            if label in ["ArticleDate", "PubDate"]:
                flags.pubdate = False

            if label in ["PubmedArticle", "PubmedBookArticle"]:
                RECORDS[record.pdate_year].add(record)
                elem.clear()

    print(f"Processing {loop + 1}/{loops} : Current number of processed records: {sum([len(x) for x in RECORDS.values()])}")


def run_query(query_term, year_from, year_to):

    resp = requests.get(get_query_url(query_term, year_from, year_to))

    results = resp.json()["esearchresult"]

    count = int(results["count"])
    chunk_size = 5000
    query_key = results['querykey']
    web_env = results['webenv']
    loops = ceil(count/chunk_size)

    return count, chunk_size, query_key, web_env, loops


def run_fetch(chunk_size, query_key, web_env, loops):
    global RECORDS
    start = 0
    RECORDS = defaultdict(set)

    for i in range(int(loops)):
        pointer = start + (int(chunk_size) * i)

        resp = requests.get(get_fetch_url(query_key, chunk_size, pointer, web_env))

        process_records(resp.text, i, loops)

    return RECORDS


if __name__ == "__main__":
    run_query("cat", 2000, 2001)
