import logging

import semantic_version

from changes import util, attributes


log = logging.getLogger(__name__)


def strip_long_arguments(arguments, long_keys):
    long_arguments = util.extract(arguments, long_keys)
    return dict([
        (key[2:], value) for key, value in long_arguments.items()
    ])


def extract_version_arguments():
    return strip_long_arguments(['--major', '--minor', '--patch'])


def increment(version, major=False, minor=False, patch=True):
    """
    Increment a semantic version

    :param version: str of the version to increment
    :param major: bool specifying major level version increment
    :param minor: bool specifying minor level version increment
    :param patch: bool specifying patch level version increment
    :return: str of the incremented version
    """
    version = semantic_version.Version(version)
    if major:
        version.major += 1
        version.minor = 0
        version.patch = 0
    elif minor:
        version.minor += 1
        version.patch = 0
    elif patch:
        version.patch += 1

    return str(version)


def get_new_version(app_name, current_version,
                    major=False, minor=False, patch=True):

    guess_new_version = increment(
        current_version,
        major=major,
        minor=minor,
        patch=patch
    )

    new_version = raw_input(
        'What is the release version for "%s" '
        '[Default: %s]: ' % (
            app_name, guess_new_version
        )
    )
    if not new_version:
        new_version = guess_new_version
    return new_version.strip()


def current_version(app_name):
    return attributes.extract_attribute(app_name, '__version__')