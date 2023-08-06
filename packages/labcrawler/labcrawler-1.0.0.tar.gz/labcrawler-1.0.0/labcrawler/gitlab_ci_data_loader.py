from os import environ
from pathlib import Path
from csv import DictWriter
import logging

from labcrawler.project_data_file import ProjectDataFile
from labcrawler.gitlab_repository_files_extractor import \
        GitLabRepositoryFilesExtractor
from labcrawler.gitlab_ci_config import GitLabCIConfig


class GitLabCIDataLoader:
    """Load includes (and later blames) from GitLab CI configs"""

    def __init__(self, config:GitLabCIConfig, project_id:int=None):
        self.config = config
        self.project_file = ProjectDataFile(self.config)
        if project_id:
            self.project_ids = [int(project_id)]    
        else:
            self.project_ids = [p['id'] for p in self.project_file.projects_data]
        self.extractor = GitLabRepositoryFilesExtractor( \
                gitlab_private_token = environ['GITLAB_PRIVATE_TOKEN'], \
                gitlab_api_url = config['api_url'] )

    def load_includes(self):
        """Load the includes (and accidentally full CI config content)"""
        contents = []  # For a future feature where we write the contents
        includes = []
        for project_id in self.project_ids:
            project_data = self.project_file.get_project_data(project_id)
            ci_config_file_content = self.extractor.extract_file_content( \
                    project_id = project_data['id'], \
                    branch = project_data['default_branch'], \
                    repo_path = project_data['ci_config_path'] or '.gitlab-ci.yml' )
            contents.append(ci_config_file_content)
            ci_config = GitLabCIConfig(ci_config_file_content)
            if ci_config.locals:
                for localfile in ci_config.locals:
                    includes.append({'project_id': project_data['id'], \
                            'local_include': localfile})
        self.write_csv(includes, 'ci_config_includes', \
                ['project_id','local_include'])

    def load_blames(self):
        """Find committer information for main CI config file"""
        committers = []
        for project_id in self.project_ids:
            project_data = self.project_file.get_project_data(project_id)
            project_committers = self.extractor.extract_blamed_committers( \
                    project_id = project_data['id'], \
                    branch = project_data['default_branch'], \
                    repo_path = project_data['ci_config_path'] or '.gitlab-ci.yml' )
            committers.extend(project_committers)
        self.write_csv(committers, 'ci_config_committers', \
                ['project_id','committer_name','committer_email'])

    def write_csv(self, rows:list, filename:str, fieldnames:list):
        path = Path(self.config['output_dir']) / (filename + '.csv')
        with open(path, 'w') as outfile:
            writer = DictWriter(outfile, fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
            logging.info(f"Wrote {len(rows)} rows to {str(path.absolute())}")
