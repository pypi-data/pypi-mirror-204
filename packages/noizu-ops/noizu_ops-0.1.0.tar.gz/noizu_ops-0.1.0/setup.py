from setuptools import setup, find_packages, Command
import os


class RunSystemInfo(Command):
    description = "Run init script: Gather System Details to Help AI Helper"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from setup import noizu_help_init
        si = noizu_help_init.system_info()
        noizu_help_init.update_config(si)

setup(
    name="noizu_ops",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        'noizu_ops': ['config/*.yml']
    },
    cmdclass={
     'run_system_info': RunSystemInfo,
    },
    install_requires=[
        "openai",
        "rich",
        "MarkupSafe",
        "pyyaml",
        "python-slugify",
        "psutil",
        "argcomplete"
    ],
    entry_points={
        "console_scripts": [
            "noizu-ops = noizu_ops.bin.noizu_ops:main",
        ],
        'argcomplete.completers': [
            'noizu-ops = noizu_ops.bin.noizu_ops:main'
        ]
    },
    author="Keith Brings",
    author_email="keith.brings@noizu.com",
    description="Interactive terminal assistant, log sessions, generate todo / step instructions, apply steps , query system status for troubleshooting., etc. (wip)",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
