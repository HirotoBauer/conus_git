#!/usr/bin/env python
"""
Python script to download selected files from rda.ucar.edu.
After you save the file, don't forget to make it executable
i.e. - "chmod 755 <name_of_script>"
"""

import sys
import os
import time
from urllib.request import build_opener
from urllib.error import HTTPError
from http.client import IncompleteRead, RemoteDisconnected
import csv
from requests.exceptions import ConnectionError
from urllib.error import URLError
import socket

opener = build_opener()

with open("urls.csv", "r") as f:  # needs to be in same directory as this script
    reader = csv.reader(f)
    filelist = [row[0] for row in reader]


max_retries = 10
delay = 20


for file in filelist:
    ofile = os.path.basename(file)
    sys.stdout.write("downloading " + ofile + " ... ")
    sys.stdout.flush()

    # Retry loop
    for attempt in range(max_retries):
        try:
            # Open the remote file
            infile = opener.open(file)
            # Open the local file for writing
            outfile = open(ofile, "wb")
            # Read and write the file content
            outfile.write(infile.read())
            outfile.close()
            sys.stdout.write("done\n")
            break  # Exit the retry loop if successful

        except IncompleteRead:
            # Handle incomplete read
            if attempt < max_retries - 1:
                sys.stdout.write(
                    f"incomplete read, retrying ({attempt + 1}/{max_retries})... "
                )
                sys.stdout.flush()
                time.sleep(delay)  # Wait before retrying
            else:
                # If all retries fail, raise the exception
                sys.stdout.write("failed\n")
                raise

        except RemoteDisconnected:  # Handle RemoteDisconnected explicitly
            if attempt < max_retries - 1:
                sys.stdout.write(
                    f"connection closed, retrying ({attempt + 1}/{max_retries})... "
                )
                sys.stdout.flush()
                time.sleep(delay)
            else:
                sys.stdout.write("failed\n")
                raise

        except HTTPError as e:
            if attempt < max_retries - 1:
                if e.code == 500:
                    sys.stdout.write(
                        f"HTTP 500 error, retrying in {delay} seconds ({attempt + 1}/{max_retries})... "
                    )
                    sys.stdout.flush()
                    time.sleep(delay)
                elif e.code == 404:
                    sys.stdout.write(
                        f"HTTP 404 error, retrying in {delay} seconds({attempt + 1}/{max_retries})..."
                    )
                    sys.stdout.flush()
                    time.sleep(delay)
                else:
                    # Re-raise for non-500 HTTP errors
                    sys.stdout.write(f"failed: {str(e)}\n")
                    raise

        except ConnectionResetError:
            if attempt < max_retries - 1:
                sys.stdout.write(
                    f"connection reset by peer, retrying ({attempt + 1}/{max_retries})... "
                )
                sys.stdout.flush()
                time.sleep(delay)
            else:
                sys.stdout.write("failed: [Errno 104] Connection reset by peer\n")
                raise

        except URLError as e:
            if attempt < max_retries - 1:
                if isinstance(e.reason, socket.error) and e.reason.errno == 104:
                    sys.stdout.write(
                        f"connection reset by peer, retrying ({attempt + 1}/{max_retries})... "
                    )
                    sys.stdout.flush()
                    time.sleep(delay)
                else:
                    sys.stdout.write("failed: [Errno 104] Connection reset by peer\n")
                    raise

        except ConnectionError as e:
            if attempt < max_retries - 1:
                if "Connection reset by peer" in str(e) and attempt < max_retries - 1:
                    sys.stdout.write(
                        f"connection reset by peer, retrying ({attempt + 1}/{max_retries})... "
                    )
                    sys.stdout.flush()
                    time.sleep(delay)
                else:
                    sys.stdout.write("failed: [Errno 104] Connection reset by peer\n")
                    raise

        except Exception as e:
            if attempt < max_retries - 1:
                sys.stdout.write(
                    f"unrecognized error: {e}, retrying ({attempt + 1}/{max_retries})... "
                )
                sys.stdout.flush()
                time.sleep(delay)
            else:
                sys.stdout.write("failed: [Errno 104] Connection reset by peer\n")
                raise
