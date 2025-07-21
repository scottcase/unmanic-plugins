#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unmanic-plugins.plugin.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     31 Aug 2021, (12:11 PM)

    Copyright:
        Copyright (C) 2021 Josh Sunnex

        This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
        Public License as published by the Free Software Foundation, version 3.

        This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
        implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
        for more details.

        You should have received a copy of the GNU General Public License along with this program.
        If not, see <https://www.gnu.org/licenses/>.

"""
import filecmp
import logging
import os
import shutil
from configparser import NoSectionError, NoOptionError

from unmanic.libs.directoryinfo import UnmanicDirectoryInfo
from unmanic.libs.unplugins.settings import PluginSettings

# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.reject_files_larger_than_original")


# TODO: Write config options in description
class Settings(PluginSettings):
    settings = {
        'fail_task_if_file_detected_larger':                 False,
        'if_end_result_file_is_still_larger_mark_as_ignore': False,
    }
    form_settings = {
        "fail_task_if_file_detected_larger":                 {
            "label": "Mark the task as failed",
        },
        "if_end_result_file_is_still_larger_mark_as_ignore": {
            "label": "Ignore files in future scans if end result is larger than source (regardless of task history)",
        },
    }


def file_marked_as_failed(settings, path):
    """Read directory info to check if file was previously marked as failed"""
    if settings.get_setting('if_end_result_file_is_still_larger_mark_as_ignore'):
        directory_info = UnmanicDirectoryInfo(os.path.dirname(path))

        try:
            previously_failed = directory_info.get('reject_files_larger_than_original', os.path.basename(path))
        except NoSectionError as e:
            previously_failed = ''
        except NoOptionError as e:
            previously_failed = ''
        except Exception as e:
            logger.debug("Unknown exception {}.".format(e))
            previously_failed = ''

        if previously_failed:
            # This stream already has been attempted and failed
            return True

    # Default to...
    return False


def write_file_marked_as_failed(path):
    """Write entry to directory infor to mark this file as failed"""
    directory_info = UnmanicDirectoryInfo(os.path.dirname(path))
    directory_info.set('reject_files_larger_than_original', os.path.basename(path), 'Ignoring')
    directory_info.save()
    logger.debug("Ignore on next scan written for '{}'.".format(path))


def on_library_management_file_test(data):
    """
    Runner function - enables additional actions during the library management file tests.

    The 'data' object argument includes:
        path                            - String containing the full path to the file being tested.
        issues                          - List of currently found issues for not processing the file.
        add_file_to_pending_tasks       - Boolean, is the file currently marked to be added to the queue for processing.

    :param data:
    :return:

    """
    # Get the path to the file
    abspath = data.get('path')

    # Configure settings object
    settings = Settings(library_id=data.get('library_id'))


    if file_marked_as_failed(settings, abspath):
        # Ensure this file is not added to the pending tasks
        data['add_file_to_pending_tasks'] = False
        data['issues'].append({
                    'id':      'Ignore files by Marked As Ignoring1',
                    'message': "File '{}' should ignored because it is marked as Ignoring.".format(abspath),
                })
    else:
        data['add_file_to_pending_tasks'] = False
        data['issues'].append({
                    'id':      'Ignore files by Marked As Ignoring2',
                    'message': "File '{}' should ignored because it is marked as Ignoring.".format(abspath),
        })
