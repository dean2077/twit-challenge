#!/bin/bash
# Below is the reason for "-nolisten tcp" (this is not documented within Xvfb manpages)
# https://superuser.com/questions/855019/make-xvfb-listen-only-on-local-ip
Xvfb :99 -screen 0 640x480x8 -nolisten tcp &
# Now run the script
python3 -u twit-main.py "$@"