import os
from collections import defaultdict
from io import StringIO
from math import ceil
from re import findall
from time import perf_counter
from typing import Tuple
from xml.etree.ElementTree import iterparse

import requests as requests

from src.dt_classes import Flags, Record
from src.url_builder import get_fetch_url, get_query_url

RECORDS: Record = None


def is_local() -> None:
    """
    Is the code running locally
    :return:
    """
    return os.environ.get('LOCAL')


def process_records(xml_response: str, api_call: int, calls: int) -> None:
    """
    Process and load the incoming records
    :param xml_response: data from efetch endpoint
    :param api_call: number of the current api call in list (for debugging logs)
    :param calls: number of calls to make in total (for debugging logs)
    :return:
    """
    record, flags = None, None

    for event, elem in iterparse(StringIO(xml_response), events=["start", "end"]):
        tag = elem.tag

        if event == 'start':
            # INIT
            if tag in ["PubmedArticle", "PubmedBookArticle"]:
                record = Record()
                flags = Flags()

            # CONTROL FLAGS
            if tag in ["ArticleDate", "PubDate"]:
                flags.pubdate = True
            if tag in ["Publisher"]:
                flags.publisher = True

        # event == end
        else:
            # DATA PROCESSING
            if flags.pubdate and tag in ["Year", "MedlineDate"]:
                new_year = int(elem.text.strip()) if tag == "Year" else int(findall(r'\d{4}', elem.text)[0])
                curr_date = record.pdate_year
                record.pdate_year = new_year if curr_date == 0 or new_year < curr_date else curr_date

            if tag == "PMID":
                record.pmid = elem.text.strip()

            if flags.publisher and tag in ["PublisherLocation", "PublisherName"]:
                if tag == "PublisherName":
                    record.publisher_name = elem.text.strip()
                else:
                    record.publisher_location = elem.text.strip()


            # CONTROL FLAGS
            if tag in ["ArticleDate", "PubDate"]:
                flags.pubdate = False
            if tag in ["Publisher"]:
                flags.publisher = False

            # LOAD RECORDS
            if tag in ["PubmedArticle", "PubmedBookArticle"]:
                RECORDS[record.pdate_year].add(record)
                elem.clear()

    print(f"Processing {api_call + 1}/{calls} : Current number of processed records: {sum([len(x) for x in RECORDS.values()])}")


def run_query(query_term: str, year_from: int, year_to: int) -> Tuple[int, int, str, str,  int]:
    """
    Call the NCBI esearch endpoint to load remote server with
    :param query_term: term to use in query
    :param year_from: year to start query
    :param year_to: year to end query
    :return:
    """

    t1 = perf_counter()
    resp = requests.get(get_query_url(query_term, year_from, year_to))
    t2 = perf_counter()
    print(f"Making esearch query took : {t2 - t1}s")

    results = resp.json()["esearchresult"]

    count = int(results["count"])
    chunk_size = 5000
    query_key = results['querykey']
    web_env: str = results['webenv']
    calls: int = ceil(count/chunk_size)

    if is_local():
        run_fetch(str(chunk_size), query_key, web_env, str(calls))
    else:
        return count, chunk_size, query_key, web_env, calls


def run_fetch(chunk_size: str, query_key: str, web_env: str, calls: str) -> defaultdict[set[Record]]:
    """
    Call the NCBI efetch endpoint to collect query data
    All parameters come in as string as pulled from query string
    :param chunk_size: number of responses to request
    :param query_key:  part 1/2 of key for location on the Entrez history server
    :param web_env: part 2/2 of key for location on the Entrez history server
    :param calls: number of api calls being made
    :return: The full set of processed records
    """
    global RECORDS
    start = 0
    chunk_size = int(chunk_size)
    calls = int(calls)
    RECORDS = defaultdict(set)

    for i in range(calls):
        pointer = start + (chunk_size * i)

        t1 = perf_counter()
        resp = requests.get(get_fetch_url(query_key, chunk_size, pointer, web_env))
        t2 = perf_counter()
        print(f"Making this efetch request took : {t2 - t1}s")

        t3 = perf_counter()
        process_records(resp.text, i, calls)
        t4 = perf_counter()
        print(f"Processing data efetch data took : {t4 - t3}s")

    return RECORDS


if __name__ == "__main__":
    os.environ['LOCAL'] = "true"
    run_query("heart failure", 2000, 2010)
