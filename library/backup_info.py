#!/usr/bin/python
import json
import subprocess

import sys
from ansible.module_utils.basic import AnsibleModule

DEFAULT_MAXIMUM_BACKUPS = 10
DEFAULT_BACKUP_NAME_SUFFIX = ""

INFO_SCRIPT_LOCATION_PARAMETER_NAME = "script"
CURRENT_BACKUPS_PARAMETER_NAME = "current"
MAXIMUM_BACKUPS_PARAMETER_NAME = "max"
BACKUP_NAME_SUFFIX_PARAMETER_NAME = "suffix"
PYTHON_EXECUTABLE_PARAMETER_NAME = "python"

_MAX_NUMBER_OF_BACKUPS_LONG_CLI_PARAMETER = "backups"
_BACKUP_NAME_SUFFIX_LONG_CLI_PARAMETER = "suffix"

_TO_DELETE_JSON_PARAMETER = "delete"
_LATEST_BACKUP_NAME_JSON_PARAMETER = "latest"
_NEW_BACKUP_NAME_JSON_PARAMETER = "new"


_ARGUMENT_SPEC = {
    INFO_SCRIPT_LOCATION_PARAMETER_NAME: dict(required=True, type="str"),
    CURRENT_BACKUPS_PARAMETER_NAME: dict(default=[], type="list"),
    MAXIMUM_BACKUPS_PARAMETER_NAME: dict(default=DEFAULT_MAXIMUM_BACKUPS, type="int"),
    BACKUP_NAME_SUFFIX_PARAMETER_NAME: dict(default=DEFAULT_BACKUP_NAME_SUFFIX, type="str"),
    PYTHON_EXECUTABLE_PARAMETER_NAME: dict(default=sys.executable, type="str")
}


def main():
    module = AnsibleModule(_ARGUMENT_SPEC, supports_check_mode=False)

    script_location = module.params.get(INFO_SCRIPT_LOCATION_PARAMETER_NAME)
    current_backups = module.params.get(CURRENT_BACKUPS_PARAMETER_NAME)
    maximum_number_of_backups = module.params.get(MAXIMUM_BACKUPS_PARAMETER_NAME)
    backup_name_suffix = module.params.get(BACKUP_NAME_SUFFIX_PARAMETER_NAME)
    python_executable = module.params.get(PYTHON_EXECUTABLE_PARAMETER_NAME)

    arguments = [python_executable, script_location,
                 "--%s" % _MAX_NUMBER_OF_BACKUPS_LONG_CLI_PARAMETER, str(maximum_number_of_backups),
                 "--%s" % _BACKUP_NAME_SUFFIX_LONG_CLI_PARAMETER, backup_name_suffix] \
                + current_backups

    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        module.fail_json(msg=stderr, arguments=arguments)

    information = json.loads(stdout)

    return_values = dict(changed=False, new=information[_NEW_BACKUP_NAME_JSON_PARAMETER],
                         latest=information[_LATEST_BACKUP_NAME_JSON_PARAMETER],
                         delete=information[_TO_DELETE_JSON_PARAMETER])
    module.exit_json(**return_values)


if __name__ == "__main__":
    main()
