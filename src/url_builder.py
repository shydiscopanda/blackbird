
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
DATABASE = "pubmed"
DATE_TYPE = "pdat"


def term_sanitiser(raw_term: str) -> str:
    return raw_term.strip().replace(" ", "+")


def url_sanitiser(url: str) -> str:
    return url.replace('"', "%22").replace("#", "%23")


def get_query_url(term: str, y_from: int, y_to: int) -> str:
    """
    Create a suitable query string for esearch endpoint
    """
    url = BASE_URL + "esearch.fcgi?"
    params = [
        f"db={DATABASE}",
        f"term={term_sanitiser(term)}",
        f"datetype={DATE_TYPE}",
        f"mindate={y_from}",
        f"maxdate={y_to}",
        "usehistory=y",
        "retmode=json"
    ]
    return url_sanitiser(url + "&".join(params))


def get_fetch_url(query_key: str, chunk_size: int, pointer:  int, web_env: int) -> str:
    """
    Create a suitable query string for efetch endpoint
    """
    url = BASE_URL + "efetch.fcgi?"
    params = [
        f"db={DATABASE}",
        f"query_key={query_key}",
        f"retmax={chunk_size}",
        f"retstart={pointer}",
        "retmode=xml",
        f"WebEnv={web_env}"
    ]
    return url_sanitiser(url + "&".join(params))

