# -*- coding:utf-8 -*-

import os
import sys


def format_container_names():
    """Format containers names
    """

    # containers
    containers = []

    # current work directory path
    cwd_path = os.getcwd()

    # current work directory name
    _, cwd_name = os.path.split(cwd_path)

    # add containers
    containers.append(f"{cwd_name}_web_1")  # odoo container
    containers.append(f"{cwd_name}_db_1")   # postgresql container

    return containers


def main():
    """Launch docker-compose services
    """

    # containers
    containers = format_container_names()

    # shutdown services and remove containers
    print("kill services and remove it")

    for container in containers:
        try:

            os.system(f"docker rm -f {container}")

        except Exception as error:
            print(f"[Error] : {error} ")

        else:
            print(
                f"[Success] : Container '{container}' shutdown and remove success")

    # set-up services

    try:

        os.system("docker-compose up -d")

    except Exception as error:
        print(f"[Error] : {error}")

    else:
        os.system("docker ps")


if __name__ == "__main__":
    main()
