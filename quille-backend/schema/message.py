from typing import TypedDict, List, Optional, Literal


class Inquire(TypedDict):
    question: str
    options: List[str]
    allows_input: bool
    input_label: str
    input_placeholder: str
    choices: List[str]
    input_value: str


class OutlineSubsection(TypedDict):
    title: str


class OutlineSection(TypedDict):
    title: str
    subsections: List[OutlineSubsection]


class Outline(TypedDict):
    sections: List[OutlineSection]


class NewDocument(TypedDict):
    name: str
    content: str


class WebSearchQuery(TypedDict):
    query: str


class WebSearch(TypedDict):
    queries: List[WebSearchQuery]


class WebSearchResult(TypedDict):
    query: str
    title: str
    url: str
    text: str


class WebSearchResults(TypedDict):
    results: List[WebSearchResult]


class Message(TypedDict):
    id: str
    date: str
    hidden: bool
    action: Optional[Literal['inquire', 'create-outline', 'create-document', 'search-web', 'web-search-results']]
    content: Optional[str]
    inquire: Optional[Inquire]
    outline: Optional[Outline]
    web_search_query: Optional[WebSearch]
    web_search_results: Optional[WebSearchResults]
    role: Literal['Assistant', 'User', 'Tool']
    status: Literal['Pending', 'InProgress', 'Completed', 'Failed']
    created_at: str
    updated_at: str
