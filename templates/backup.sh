#!/usr/bin/env bash

set -eu -o pipefail


sudo -u {{ postgres_s3_backup_pg_dumpall_user }} pg_dumpall | gzip | mc pipe