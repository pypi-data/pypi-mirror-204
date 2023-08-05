#!/usr/bin/env python3
# =============================================================================
# @file    setup.py
# @brief   Installation setup file
# @created 2022-12-08
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/iga
#
# Note: the full configuration metadata is maintained in setup.cfg, not here.
# This file exists to hook in setup.cfg and requirements.txt, so that the
# requirements don't have to be repeated and so that "python3 setup.py" works.
# =============================================================================

from setuptools import setup


def requirements(file):
    from os import path
    required = []
    requirements_file = path.join(path.abspath(path.dirname(__file__)), file)
    if path.exists(requirements_file):
        with open(requirements_file, encoding='utf-8') as f:
            required = [ln for ln in filter(str.strip, f.read().splitlines())
                        if not ln.startswith('#')]
        if any(item.startswith(('-', '.', '/')) for item in required):
            # The requirements.txt uses pip features. Try to use pip's parser.
            try:
                from pip._internal.req import parse_requirements
                from pip._internal.network.session import PipSession
                parsed = parse_requirements(requirements_file, PipSession())
                required = [item.requirement for item in parsed]
            except ImportError:
                # No pip, or not the expected version. Give up & return as-is.
                pass
    return required


setup(
    setup_requires=['wheel'],
    install_requires=requirements('requirements.txt'),
)
