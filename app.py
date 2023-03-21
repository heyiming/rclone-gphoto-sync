#!/usr/bin/env python

import rclone
import logging
import json
import os

#logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

config_file_key = "CONFIG_FILE"
remote_name_key = "REMOTE_NAME"
dry_run_key = "DRY_RUN"
sync_target = "/sync_target"

def main():
    if config_file_key not in os.environ:
        logger.error(f"{config_file_key} is not defined.")
        return
    
    if remote_name_key not in os.environ:
        logger.error(f"{remote_name_key} is not defined.")
        return
    
    flags = []
    if dry_run_key in os.environ:
        flags.append("--dry-run")
    
    with open(os.environ[config_file_key], 'r') as file:
        cfg = file.read()
    
    remote = os.environ[remote_name_key] + ':'    
    rc = rclone.with_config(cfg)
    logger.debug(rc.listremotes())

    top = remote +  "media/by-month"
    years = json.loads(rc.lsjson(top, flags=["--dirs-only"]).get('out'))    
    
    for year in years:
        year_path = top + '/' + year.get("Path")
        months = json.loads(rc.lsjson(year_path, flags=["--dirs-only"]).get('out'))
        for month in months:
            month_path = year_path + '/' + month.get("Path")
            logger.debug(f"Working on {month_path}")
            result = rc.copy(month_path, sync_target, flags)
            # logger.debug(result)


if __name__ == "__main__":    
    main()