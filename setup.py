from setuptools import setup

setup(
    name='aws-utils',
    version='1.0.0',
    description='AWS Utils',
    url='https://github.com/xz278/aws-utils.git',
    author='Xian Zhang',
    author_email='zhang.xian.0414@outlook.com',
    packages=['aws_utils'],
    zip_safe=False,
    install_requires=['boto3', 'pandas'],
    include_package_data=False,
    # scripts=['bin/syncredash'],
    # entry_points = {
    #     'console_scripts': ['syncredash=report_redash.command_line:main'],
    # }
)
