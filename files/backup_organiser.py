#!/usr/bin/python

CURRENT_BACKUPS_PARAMETER_NAME = "current"
MAXIMUM_BACKUPS_PARAMETER_NAME = "max"

DEFAULT_MAXIMUM_BACKUPS = 10



class Configuration:
    """
    TODO
    """
    def __init__(self, current_backup_names, maximum_number_of_backups):
        self.current_backup_names = current_backup_names
        self.maximum_number_of_backups = maximum_number_of_backups


class Result:
    """
    TODO
    """
    def __init__(self, new_backup_name, latest_backup, to_delete):
        self.new_backup_name = new_backup_name
        self.latest_backup = latest_backup
        self.to_delete = to_delete


def _process(configuration):
    """
    TODO
    :param configuration: TODO
    :type configuration: Configuration
    :return: TODO
    :rtype: Result
    """
    current_backup_dates = _parse_dates(configuration.current_backup_names)
    new_backup_name = _generate_new_backup_name(current_backup_dates)
    #configuration.maximum_number_of_backups


def _parse_dates(backup_names):
    """
    TODO
    :param backup_names: TODO
    :type backup_names: List[str]
    :return: TODO
    :rtype: Dict[datetime, str]
    """
    return {}


def _generate_new_backup_name(current_backup_dates):
    """
    TODO
    :param current_backup_dates:
    :type current_backup_dates: Dict[datetime, str]
    :return: TODO
    :rtype: str
    """
    return ""


# def check_dependencies():
#     """
#     Checks that the required dependencies have been imported.
#     :exception ImportError: if it is detected that any of the required dependencies have not been iported
#     """
#     if not python_consul_installed:
#         raise ImportError("python-consul required for this module. "
#                           "See: http://python-consul.readthedocs.org/en/latest/#installation")
#
#     if not pyhcl_installed:
#         raise ImportError("pyhcl required for this module. "
#                           "See: https://pypi.python.org/pypi/pyhcl")


def main():
    """
    Main method.
    """

    # try:
    #     check_dependencies()
    # except ImportError as e:
    #     module.fail_json(msg=str(e))

    configuration = Configuration(
        current_backup_names=module.params.get(CURRENT_BACKUPS_PARAMETER_NAME),
        maximum_number_of_backups=module.params.get(MAXIMUM_BACKUPS_PARAMETER_NAME)
    )

    return_values = dict(changed=output.changed, token=output.token, operation=output.operation)
    module.exit_json(**return_values)


if __name__ == "__main__":
    main()
