import json
import re
from argparse import ArgumentParser

import arrow
import sys
from hgijson import JsonPropertyMapping, MappingJSONEncoderClassBuilder

DEFAULT_MAXIMUM_BACKUPS = 10
DEFAULT_BACKUP_NAME_SUFFIX = ""

_CURRENT_BACKUPS_POSITIONAL_CLI_PARAMETER = "current-backups"
_MAX_NUMBER_OF_BACKUPS_LONG_CLI_PARAMETER = "backups"
_BACKUP_NAME_SUFFIX_LONG_CLI_PARAMETER = "suffix"


class Configuration:
    """
    Configuration to be used by the organiser.
    """
    def __init__(self, current_backup_names, maximum_number_of_backups, backup_name_suffix):
        self.current_backup_names = current_backup_names
        self.maximum_number_of_backups = maximum_number_of_backups
        self.backup_name_suffix = backup_name_suffix


class Result:
    """
    Result of this organiser.
    """
    def __init__(self, new_backup_name, latest_backup, to_delete):
        self.new_backup_name = new_backup_name
        self.latest_backup = latest_backup
        self.to_delete = to_delete


result_mapping_schema = [
    JsonPropertyMapping("new", "new_backup_name"),
    JsonPropertyMapping("latest", "latest_backup"),
    JsonPropertyMapping("delete", "to_delete")
]
ResultJSONEncoder = MappingJSONEncoderClassBuilder(Result, result_mapping_schema).build()


def process(configuration):
    """
    Process backup results for the given configuration.
    :param configuration: configuration to process
    :type configuration: Configuration
    :return: results based on the given configuration
    :rtype: Result
    """
    new_backup_name = _generate_backup_name(backup_name_suffix=configuration.backup_name_suffix)

    dated_backup_name_map = _create_date_name_map(configuration.current_backup_names, configuration.backup_name_suffix)
    sorted_backup_dates = sorted(dated_backup_name_map.keys())
    to_delete = [dated_backup_name_map[x] for x in
                 (sorted_backup_dates[:-configuration.maximum_number_of_backups]
                  if configuration.maximum_number_of_backups > 0 else dated_backup_name_map.keys())]
    latest_backup = dated_backup_name_map[sorted_backup_dates[-1]] if len(dated_backup_name_map) > 0 else None

    return Result(new_backup_name=new_backup_name, latest_backup=latest_backup, to_delete=to_delete)


def main(cli_args):
    """
    Main method.
    :param cli_args: arguments specified on the CLI
    :type cli_args: List[Any]
    """
    configuration = _get_cli_configuration(cli_args)
    output = process(configuration)

    print(json.dumps(output, cls=ResultJSONEncoder))


def _get_cli_configuration(cli_args):
    """
    Gets the CLI configuration from the given CLI arguments.
    :param cli_args: arguments specified on the CLI
    :type cli_args: List[Any]
    :return: configuration implied by the given CLI arguments
    :rtype: Configuration
    """
    parser = ArgumentParser()
    parser.add_argument(_CURRENT_BACKUPS_POSITIONAL_CLI_PARAMETER, metavar="current-backup", default=[], nargs="*",
                        type=str, help="name of current backup")
    parser.add_argument("--%s" % _MAX_NUMBER_OF_BACKUPS_LONG_CLI_PARAMETER, type=int, default=DEFAULT_MAXIMUM_BACKUPS,
                        help="maximum number of backups to keep")
    parser.add_argument("--%s" % _BACKUP_NAME_SUFFIX_LONG_CLI_PARAMETER, type=str, default=DEFAULT_BACKUP_NAME_SUFFIX,
                        help="suffix to add to all backup names")

    arguments = vars(parser.parse_args(cli_args))
    return Configuration(
        current_backup_names=arguments[_CURRENT_BACKUPS_POSITIONAL_CLI_PARAMETER],
        maximum_number_of_backups=arguments[_MAX_NUMBER_OF_BACKUPS_LONG_CLI_PARAMETER],
        backup_name_suffix=arguments[_BACKUP_NAME_SUFFIX_LONG_CLI_PARAMETER]
    )


def _create_date_name_map(backup_names, backup_name_suffix):
    """
    Creates a mapping between backup dates and backup names based on the timestamp in the backup name.
    :param backup_names: names of all backups
    :type backup_names: Iterable[str]
    :param backup_name_suffix: backup name suffix
    :type backup_name_suffix: str
    :return: mapping between backup date and its name
    :rtype: Dict[Arrow, str]
    """
    return {arrow.get(re.sub(r"%s$" % backup_name_suffix, "", backup_name)): backup_name
            for backup_name in backup_names if backup_name.endswith(backup_name_suffix)}


def _generate_backup_name(timestamp=arrow.utcnow(), backup_name_suffix=DEFAULT_BACKUP_NAME_SUFFIX):
    """
    Generates backup name given a timestamp and a suffix.
    :param timestamp: timestamp to associate to the backup
    :type timestamp: Arrow
    :param backup_name_suffix: suffix to append of the backup name
    :type backup_name_suffix: str
    :return: generated backup name
    :rtype: str
    """
    return "%s%s" % (timestamp, backup_name_suffix)


if __name__ == "__main__":
    main(sys.argv[1:])
