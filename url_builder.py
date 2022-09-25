
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
DATABASE = "pubmed"
DATE_TYPE = "pdat"


def term_sanitiser(raw_term):
    return raw_term.strip().replace(" ", "+")


def url_sanitiser(url):
    return url.replace('"', "%22").replace("#", "%23")


def get_query_url(term, y_from, y_to):
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


def get_fetch_url(query_key, chunk_size, pointer, web_env):
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

