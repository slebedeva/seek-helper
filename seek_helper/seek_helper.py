from yellow_pages.project import Project

from experiments.investigation import Investigation
from experiments.study import Study
from experiments.assay import Assay

from assets.data_file import DataFile


class SeekHelper():
    def __init__(self, token: str, base_url: str, output_path: str):
        # Yellow Pages
        self.Project = Project(token, base_url, output_path)

        # Experiments
        self.Investigation = Investigation(token, base_url)
        self.Study = Study(token, base_url)
        self.Assay = Assay(token, base_url)

        # Assets
        self.DataFile = DataFile(token, base_url, output_path)
