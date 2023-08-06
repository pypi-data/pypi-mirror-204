from unittest import TestCase

from labcrawler.gitlab_ci_config import GitLabCIConfig


class TestGitLabCIConfig(TestCase):

    def test_nothing(self):
        self.assertEqual(3,3)

    def test_yaml(self):
        c = GitLabCIConfig("""
        include: foo
        """)
        self.assertEqual(c.yaml, {'include':'foo'})

    def test_include_str(self):
        c = GitLabCIConfig("""
        include: foo
        """)
        self.assertEqual(c.locals, {'foo'})

    def test_include_list(self):
        c = GitLabCIConfig("""
        include:
          - goo
          - hoo
        """)
        self.assertEqual(c.locals, {'goo','hoo'})

    def test_include_list_local(self):
        c = GitLabCIConfig("""
        include:
          - local: goo
          - hoo
        """)
        self.assertEqual(c.locals, {'goo','hoo'})

    def test_include_list_remote(self):
        c = GitLabCIConfig("""
        include:
          - remote: goo
          - hoo
        """)
        self.assertEqual(c.locals, {'hoo'})

    def test_exclude_url(self):
        c = GitLabCIConfig("""
          include:
            - 'https://abc'
            - 'def'
          """)
        self.assertEqual(c.locals, {'def'})
    
    def test_complex_example(self):
        c = GitLabCIConfig("""
          include:
            - 'https://gitlab.com/awesome-project/raw/main/.before-script-template.yml'
            - '/templates/.after-script-template.yml'
            - template: Auto-DevOps.gitlab-ci.yml
            - project: 'my-group/my-project'
              ref: main
              file: '/templates/.gitlab-ci-template.yml'
          """)
        self.assertEqual(c.locals, {'/templates/.after-script-template.yml'})
        