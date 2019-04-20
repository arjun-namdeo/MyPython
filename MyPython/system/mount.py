#!/usr/bin/env python

import os
import traceback

user_name = os.getenv("USER")

COMMAND = "echo e98 | sudo -S mount -t vboxsf {0} {1}"

def get_mount_path(drive):
    path = "/home/{0}/WindowsShared/{1}".format(user_name, drive)
    return path

def get_mount_name(drive):
    return "{0}_DRIVE".format(str(drive).upper())

def verify_mount(mount_name, mount_path):
    # check if the mount already exists.
    is_mounted = os.path.ismount(mount_path)
    if is_mounted:
        print ("{0} is has been mounted in your current system.".format(mount_name))
        print ("Mount Path for {0} : {1}".format(mount_name, mount_path))
        return True
    return False

def mount_drives(drives):
    for drive in drives:
        mount_name = get_mount_name(drive=drive)
        mount_path = get_mount_path(drive=drive)

        # If the directory is missing then create it
        if not os.path.isdir(mount_path):
            os.makedirs(mount_path)

        if verify_mount(mount_name, mount_path):
            continue

        command = COMMAND.format(mount_name, mount_path)

        try:
            os.system(command)
        except Exception:
            traceback.print_exc()

        if verify_mount(mount_name, mount_path):
            continue

        print ("Unable to mount {0}. Run this script in terminal to debug.".format(mount_name))

        return


if __name__ == "__main__":
    drives = ["D", "E"]
    mount_drives(drives=drives)