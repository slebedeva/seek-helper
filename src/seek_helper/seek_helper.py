from seek_helper.yellow_pages.institution import Institution
from seek_helper.yellow_pages.people import People
from seek_helper.yellow_pages.programme import Programme
from seek_helper.yellow_pages.project import Project

from seek_helper.experiments.investigation import Investigation
from seek_helper.experiments.study import Study
from seek_helper.experiments.assay import Assay

from seek_helper.assets.data_file import DataFile


class SeekHelper():
    def __init__(self, token: str, base_url: str, output_path: str, input_path: str, experimental_features: bool = False):
        # Yellow Pages
        self.Institution = Institution(token, base_url)
        self.People = People(token, base_url)
        self.Programme = Programme(token, base_url)
        self.Project = Project(
            token, base_url, input_path, DataFile(token, base_url, output_path, input_path, experimental_features))

        # Experiments
        self.Investigation = Investigation(token, base_url)
        self.Study = Study(token, base_url)
        self.Assay = Assay(
            token, base_url, input_path, DataFile(token, base_url, output_path, input_path, experimental_features))

        # Assets
        self.DataFile = DataFile(token, base_url, output_path, input_path, experimental_features)
