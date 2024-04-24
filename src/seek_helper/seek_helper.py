from seek_helper.yellow_pages.project import Project

from seek_helper.experiments.investigation import Investigation
from seek_helper.experiments.study import Study
from seek_helper.experiments.assay import Assay

from seek_helper.assets.data_file import DataFile


class SeekHelper():
    def __init__(self, token: str, base_url: str, output_path: str, input_path: str):
        # Yellow Pages
        self.Project = Project(
            token, base_url, output_path, input_path, DataFile(token, base_url, output_path))

        # Experiments
        self.Investigation = Investigation(token, base_url)
        self.Study = Study(token, base_url)
        self.Assay = Assay(token, base_url)

        # Assets
        self.DataFile = DataFile(token, base_url, output_path)
