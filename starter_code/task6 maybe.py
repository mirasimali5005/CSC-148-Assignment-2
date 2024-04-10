import csv
from typing import List, Dict
from tm_trees import TMTree

DATA_FILE = 'cs1_papers.csv'
AUTHOR_IDX = 0
TITLE_IDX = 1
YEAR_IDX = 2
CATEGORY_IDX = 3
DOI_IDX = 4
CITATION_IDX = 5


class PaperTree(TMTree):
    """
    A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    _authors: The name(s) of the paper's authors.
    _doi: The digital object identifier of the paper.
    _citations: The number of citations of the paper.
    """

    _authors: str
    _doi: str
    _citations: int

    def __init__(self, name: str, subtrees: List['PaperTree'],
                 authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        self._authors = authors
        self._doi = doi
        self._citations = citations
        if all_papers:
            with open(DATA_FILE, 'r') as f:
                papers = [row for row in csv.reader(f)][1:]  # Skipping header
                papers_dict = self._build_nested_dict(papers, by_year)
                subtrees = self._build_tree_from_dict(papers_dict)
            super().__init__('CS1', subtrees, citations)
        else:
            super().__init__(name, subtrees, citations)

    def get_separator(self) -> str:
        return ','

    def get_suffix(self) -> str:
        if not self._subtrees:
            return ' (paper)'
        else:
            return ' (category)'

    def _build_nested_dict(self, data: List[List[str]], by_year: bool) -> Dict:
        nested_dict = {}
        for line in data:
            path = []
            if by_year:
                path.append(line[YEAR_IDX].strip())

            categories = line[CATEGORY_IDX].split(':')
            for category in categories:
                path.append(category.strip())

            current = nested_dict
            for category in path:
                if category not in current:
                    current[category] = {}
                current = current[category]

            if 'papers' not in current:
                current['papers'] = []

            paper_details = {
                'title': line[TITLE_IDX],
                'authors': line[AUTHOR_IDX],
                'doi': line[DOI_IDX],
                'citations': int(line[CITATION_IDX])
            }
            current['papers'].append(paper_details)

        return nested_dict

    def _build_tree_from_dict(self, nested_dict: Dict, path: str = '') -> List[
        'PaperTree']:
        trees = []
        for key in nested_dict:
            if key == 'papers':
                for paper in nested_dict[key]:
                    trees.append(PaperTree(paper['title'], [], paper['authors'],
                                           paper['doi'], paper['citations']))
            else:
                subtrees = self._build_tree_from_dict(nested_dict[key],
                                                      path + key + '/')
                tree_name = f"{path}{key}" if path else key
                trees.append(PaperTree(tree_name, subtrees))
        return trees


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_build_nested_dict'],
        'max-args': 8
    })
