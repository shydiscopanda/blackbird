from src.url_builder import get_fetch_url, get_query_url, term_sanitiser, url_sanitiser


def test_term_sanitiser():
    assert term_sanitiser("test gap is replaced") == "test+gap+is+replaced"
    assert term_sanitiser(" whitespace stripped ") == "whitespace+stripped"


def test_url_sanitiser():
    assert url_sanitiser("test+#42+hashtag+replaced") == "test+%2342+hashtag+replaced"
    assert url_sanitiser('"double"+quotes+replaced') == "%22double%22+quotes+replaced"


def test_get_query_url():
    url = get_query_url("search term", 2000, 2020)
    expected = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=search+term&datetype=pdat&mindate=2000&maxdate=2020&usehistory=y&retmode=json"
    assert url == expected


def test_get_fetch_url():
    url = get_fetch_url(1, 5000, 0, "MCID_632ffedd483b6c34f6286913")
    expected = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key=1&retmax=5000&retstart=0&retmode=xml&WebEnv=MCID_632ffedd483b6c34f6286913"
    assert url == expected
