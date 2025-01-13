#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Amplifies the audio in Audacity using the mod-script-pipe, changes the speed ( for copyright ), and exports the file as MP3.

Make sure Audacity is running first, an audio part is selected, and that mod-script-pipe is enabled
before running this script.

Requires Python 2.7 or later. Python 3 is strongly recommended.
"""

import os
import sys

if sys.platform == 'win32':
    print("pipe-test.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("pipe-test.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist.  Good.")

TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")


def send_command(command):
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

def get_response():
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

def amplify_audio(ratio=3, allow_clipping=False):
    allow_clipping_str = 'True' if allow_clipping else 'False'
    command = f'Amplify: Ratio={ratio} AllowClipping={allow_clipping_str}'
    response = do_command(command)
    print("Amplify Response:", response)

def change_speed(percentage=-40):
    command = f'ChangeSpeed: Percentage={percentage}'
    response = do_command(command)
    print("Change Speed Response:", response)

def export_audio(file_path, format="MP3"):
    command = f'Export2: Filename="{file_path}" Format={format}'
    response = do_command(command)
    print("Export Response:", response)

if __name__ == "__main__":
    amplify_audio()
    change_speed(-40)  # Change speed to 60% of the original speed
    downloads_folder = os.path.expanduser("~/Downloads")
    export_audio(os.path.join(downloads_folder, "exported.mp3"))
