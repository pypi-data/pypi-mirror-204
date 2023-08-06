from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
from shutil import rmtree
from shutil import copy
from os import chdir
from sys import argv
from json import load
from os import environ
from getpass import getpass
from code import interact
from platform import python_version
import logging
import sys
import os

from platformdirs import user_data_dir
from platformdirs import user_documents_dir

from labcrawler.analysis import RawDataSet
from labcrawler.analysis import AssembledDataSet
from labcrawler.analysis import DATATYPES
from labcrawler.gitlab_ci_data_loader import GitLabCIDataLoader


APPNAME = "LabCrawler"
APPAUTHOR = "SteampunkWizard"

class LabCrawlerCLI:

    def __init__(self):
        self.set_logging()
        parser = ArgumentParser()
        parser.add_argument('command', choices=['init','melt','load','analyze'])
        namespace = parser.parse_args(argv[1:])
        getattr(self, namespace.command)()

    @staticmethod
    def set_logging():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @property
    def workspace(self):
        if not hasattr(self, '_workspace'):
            self._workspace = Path(user_data_dir(APPNAME, APPAUTHOR))
        return self._workspace

    @property
    def config_path(self):
        return self.workspace / 'labcrawler.json'

    def init(self):
        self.clear_dir("the LabCrawler workspace", self.workspace)
        self.init_meltano()
        self.init_config()
        self.init_plugins()
        print(f"Remember to edit the config file at\n  {self.config_path}")

    @staticmethod
    def clear_dir(prompt:str, dir:Path):
        if dir.exists():
            if dir.is_dir():
                if not len([f for f in dir.iterdir()]):
                    return
            print(dir)
            confirm = input(f"ABSOLUTELY CERTAIN you want to delete {prompt}? (type YES)? ")
            if confirm != 'YES':
                raise RuntimeError("User cancelled")
            if dir.is_file():
                dir.unlink()
            elif dir.is_dir():
                rmtree(dir)
        dir.mkdir(parents=True)

    def init_meltano(self):
        print(f"Initializing Meltano... ")
        run(['meltano','init',str(self.workspace)])
        print(f"Initialized Meltano.")

    def init_config(self):
        # Is this going to work after pipx install?
        templates = Path(__file__).parent / 'templates'
        copy(templates / 'meltano.yml', self.workspace / 'meltano.yml')
        with open(templates / 'labcrawler.json.template') as config_template_file:
            config_template = config_template_file.read()
        output_dir = Path(user_documents_dir()) / APPNAME
        with open(self.config_path, 'w') as config_file:
            config_file.write(config_template.format(output_dir=output_dir))

    def init_plugins(self):
        chdir(self.workspace)
        print("Installing Meltano plugins...")
        run(['meltano','install'])
        print("Installed Meltano plugins")

    @property
    def config(self):
        """When reading the config file, only read it once"""
        if not hasattr(self, '_config'):
            with open(self.config_path) as config_file:
                self._config = load(config_file)
        return self._config

    @staticmethod
    def grab_token():
        if not 'GITLAB_PRIVATE_TOKEN' in environ:         
            secret = getpass("GitLab Private Token: ").strip()
            if len(secret) != 26:
                raise RuntimeError("GitLab Private Token must contain 26 characters")
            environ['GITLAB_PRIVATE_TOKEN'] = secret


    def melt(self):
        """Load all the data via meltano"""
        if not self.workspace.exists():
            raise RuntimeError("Use the init command first")
        output_dir = self.config['output_dir']
        self.clear_dir("previous output", Path(output_dir))
        self.grab_token()
        environ['OUTPUT_DIR'] = output_dir
        environ['GITLAB_API_URL'] = self.config['api_url']
        environ['GITLAB_GROUPS'] = ' '.join(self.config['groups'])
        chdir(self.workspace)
        run(['meltano','run','tap-gitlab','target-csv'])
        print(f"Output is in {output_dir}")

    def load(self):
        """Load CI includes (and later blames), not covered by meltano"""
        # Cheap and easy cli argument: give me PROJECT_ID to limit scope
        self.grab_token()
        if 'PROJECT_ID' in os.environ:
            loader = GitLabCIDataLoader(self.config, \
                    project_id=os.environ['PROJECT_ID'])
        else:
            loader = GitLabCIDataLoader(self.config)
        loader.load_includes()
        loader.load_blames()

    def analyze(self):
        raw = RawDataSet(self.config['output_dir'])
        assembled = AssembledDataSet(raw)
        values = vars(assembled)
        banner = "\n".join([f"{len(values[t].index)} {t}" for t in values])
        banner = f"LabCrawler analysis\n{banner}\nPython {python_version()}"
        values['raw'] = raw
        interact(local=values, banner=banner)