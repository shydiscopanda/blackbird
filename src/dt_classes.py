from dataclasses import dataclass


@dataclass
class Record:
    """
    Holds information for each search result
    """
    pdate_year: int = 0
    pmid: str = None
    publisher_location: str = None
    publisher_name: str = None

    def __hash__(self):
        return hash(self.pmid)


@dataclass
class Flags:
    """
    Bool flags used for flow control in
    """
    pubdate: bool = False
    publisher: bool = False
