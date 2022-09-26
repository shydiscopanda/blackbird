from collections import defaultdict
from unittest import mock

from src.dt_classes import Record
from src.search import process_records
from tests.data.efetch_test_data import efetch_text_response

mock_records = defaultdict(set)


@mock.patch("src.search.RECORDS", mock_records)
def test_process_records():

    expected = {
        1993: {
            Record(
                pdate_year=1993,
                pmid='20301443',
                publisher_location='Seattle (WA)',
                publisher_name='University of Washington, Seattle'
            ),
            Record(
                pdate_year=1993,
                pmid='20301510',
                publisher_location='Seattle (WA)',
                publisher_name='University of Washington, Seattle'
            )},
        2001: {
            Record(
                pdate_year=2001,
                pmid='35696502',
                publisher_location='Rockville (MD)',
                publisher_name='Agency for Healthcare Research and Quality (US)'
            )
        }
    }

    process_records(efetch_text_response, 5, 10)

    assert mock_records == expected
