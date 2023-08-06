from pathlib import Path
from dataclasses import dataclass
from sys import argv
from inspect import get_annotations

from pandas import DataFrame
from pandas import read_csv

@dataclass
class DataSet:
    access_levels:DataFrame = None
    groups:DataFrame = None
    projects:DataFrame = None
    branches:DataFrame = None
    merge_requests:DataFrame = None
    project_members:DataFrame = None
    group_members:DataFrame = None
    users:DataFrame = None
    ci_config_committers:DataFrame = None
    ci_config_includes:DataFrame = None

def datatypes():
    annotations = get_annotations(DataSet)
    return  [n for n in annotations if annotations[n] == DataFrame]

DATATYPES = datatypes()

class RawDataSet(DataSet):

    def __init__(self, output_path_str:str):
        output_path = Path(output_path_str).expanduser()
        for datatype in DATATYPES:
            path = output_path / f'{datatype}.csv'
            if path.exists():
                with open(path) as dtfile:
                    dtframe = read_csv(dtfile)
                    setattr(self, datatype, dtframe)

class AssembledDataSet(DataSet):

    def __init__(self, raw:RawDataSet):
        self.access_levels = \
                DataFrame(data = [[0,'No access'], [5,'Minimal access'],
                [10, 'Guest'], [20, 'Reporter'], [30, 'Developer'], [40, 'Maintainer'],
                [50, 'Owner']], columns = ['id', 'name']).set_index('id')
        if isinstance(raw.groups, DataFrame):
                self.groups = raw.groups.set_index('id')
        if isinstance(raw.projects, DataFrame):
                self.projects = raw.projects.set_index('id')
        if isinstance(raw.users, DataFrame):
                self.users = raw.users.set_index('id')
        self.branches = raw.branches.set_index('project_id').\
                join(self.projects[['name','path_with_namespace']].add_prefix('project_'))
        if isinstance(raw.merge_requests, DataFrame):
                self.merge_requests = raw.merge_requests.set_index('project_id').\
                        join(self.projects[['name','path_with_namespace']].add_prefix('project_'))
        if isinstance(raw.project_members, DataFrame):
                self.project_members = raw.project_members.\
                        join(self.projects[['name','path_with_namespace']].add_prefix('project_'), on='project_id').\
                        join(self.users[['username']].add_prefix('user_'), on='user_id').\
                        join(self.access_levels[['name']].add_prefix('access_level_'), on='access_level')
        if isinstance(raw.group_members, DataFrame):
                self.group_members = raw.group_members.\
                        join(self.groups[['path']].add_prefix('group_'), on='group_id').\
                        join(self.access_levels[['name']].add_prefix('access_level_'), on='access_level')
        if isinstance(raw.ci_config_committers, DataFrame):
                self.ci_config_committers = raw.ci_config_committers.\
                        join(self.projects[['name','path_with_namespace']].add_prefix('project_'), on='project_id' )
        if isinstance(raw.ci_config_includes, DataFrame):
                self.ci_config_includes = raw.ci_config_includes.\
                        join(self.projects[['name','path_with_namespace']].add_prefix('project_'), on='project_id' )
        
        for datatype in DATATYPES:
            df = getattr(self, datatype)
            if df is not None:
                df.index.name = 'id'

