#!/usr/bin/python

DEFAULT_MAXIMUM_BACKUPS = 10
DEFAULT_BACKUP_NAME_SUFFIX = ""

CURRENT_BACKUPS_PARAMETER_NAME = "current"
MAXIMUM_BACKUPS_PARAMETER_NAME = "max"



def main():
    configuration = Configuration(
        current_backup_names=module.params.get(CURRENT_BACKUPS_PARAMETER_NAME),
        maximum_number_of_backups=module.params.get(MAXIMUM_BACKUPS_PARAMETER_NAME)
    )

    return_values = dict(changed=output.changed, token=output.token, operation=output.operation)
    module.exit_json(**return_values)


if __name__ == "__main__":
    # TODO
    pass