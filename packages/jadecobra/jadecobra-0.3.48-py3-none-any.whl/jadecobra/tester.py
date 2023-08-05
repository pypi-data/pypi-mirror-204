import unittest
import os
import sys

from . import toolkit

def create_scaffolding():
    for command in (
        'npm install -g npm aws-cdk',
        'cdk init app --language python',
        'python -m pip install -U pip',
        'python -m pip install -r requirements.txt',
    ):
        os.system(command)

def remove_unwanted_files(project_name):
    os.remove('requirements-dev.txt')
    os.rmdir('tests/unit')
    os.rmdir(project_name)

def run_tests():
    os.system('sniffer')

def update_requirements():
    with open('requirements.txt', 'a') as file:
        file.write('jadecobra\n')
        if sys.platform.startswith('linux'):
            file.write('pyinotify')
        elif sys.platform.startswith('win32'):
            file.write('pywin32')
        elif sys.platform.startswith('darwin'):
            file.write('macfsevents')

def create_test_file(project_name):
    toolkit.write_file(
        filepath='tests/__init__.py',
        data=f'''import jadecobra.tester

class Test{project_name}(jadecobra.tester.TestCase):

    def test_failure(self):
        self.assertFalse(True)'''
    )

def create_scent():
    toolkit.write_file(
        filepath='scent.py',
        data="""import sniffer.api
import subprocess
watch_paths = ['tests/', 'src/']

@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run(
        'python -m unittest -f tests/*.*',
        shell=True
    ).returncode == 0:
        return True"""
    )

def create_app(project_name):
    toolkit.write_file(
        filepath='app.py',
        data=f'''import aws_cdk
import jadecobra.toolkit
import os
import {project_name}

app = aws_cdk.App()
{project_name}.Stack(
    app, {project_name},
    env=aws_cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)

jadecobra.toolkit.time_it(
    function=app.synth,
    description='cdk ls for {project_name}'
)
        '''
    )

def create_tdd_project(project_name):
    return

def get_project_name(project_name):
    return os.path.split(os.getcwd())[-1]

def create_tdd_cdk_project(project_name=None):
    if not project_name:
        project_name = get_project_name(project_name)
    create_scaffolding()
    update_requirements()
    create_app(project_name)
    create_test_file(project_name)
    create_scent()
    remove_unwanted_files(project_name)
    run_tests()


class TestCase(unittest.TestCase):

    maxDiff = None

    def create_cdk_templates(self):
        '''Create CloudFormation using CDK with presets'''
        result = toolkit.run_in_shell(
            (
                'cdk ls '
                '--no-version-reporting '
                '--no-path-metadata '
                '--no-asset-metadata'
            )
        )
        self.assertEqual(result.returncode, 0)

    def assert_cdk_templates_equal(self, stack_name):
        '''Check if stack_name in cdk.out folder and tests/fixtures are the same'''
        self.assertEqual(
            toolkit.read_json(f"cdk.out/{stack_name}"),
            toolkit.read_json(f"tests/fixtures/{stack_name}")
        )

    def assert_attributes_equal(self, thing=None, attributes=None):
        '''Check that the given attributes match the attributes of thing'''
        self.assertEqual(
            sorted(dir(thing)), sorted(attributes)
        )