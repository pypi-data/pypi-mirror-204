#!/usr/bin/env python




import base64

import httplib2

import json

import os

import os.path

import sys


if len(sys.argv) != 4 and len(sys.argv) != 6:

    print("""

Sample script to recursively import in Orthanc all the DICOM files

that are stored in some path. Please make sure that Orthanc is running

before starting this script. The files are uploaded through the REST

API.


Usage: %s [hostname] [HTTP port] [path]

Usage: %s [hostname] [HTTP port] [path] [username] [password]

For instance: %s 127.0.0.1 8042 .

""" % (sys.argv[0], sys.argv[0], sys.argv[0]))

    exit(-1)


URL = 'http://%s:%d/instances' % (sys.argv[1], int(sys.argv[2]))


dicom_count = 0

json_count = 0

total_file_count = 0



def IsJson(content):

    try:

        if (sys.version_info >= (3, 0)):

            json.loads(content.decode())

            return True

        else:

            json.loads(content)

            return True

    except:

        return False



# This function will upload a single file to Orthanc through the REST API

def UploadFile(path):

    global dicom_count

    global json_count

    global total_file_count


    f = open(path, 'rb')

    content = f.read()

    f.close()

    total_file_count += 1


    sys.stdout.write('Importing %s' % path)


    if IsJson(content):

        sys.stdout.write(' => ignored JSON file\n')

        json_count += 1

        return


    try:

        h = httplib2.Http()


        headers = { 'content-type' : 'application/dicom' }


        if len(sys.argv) == 6:

            username = sys.argv[4]

            password = sys.argv[5]


            # h.add_credentials(username, password)


            # This is a custom reimplementation of the

            # "Http.add_credentials()" method for Basic HTTP Access

            # Authentication (for some weird reason, this method does

            # not always work)

            # http://en.wikipedia.org/wiki/Basic_access_authentication

            creds_str = username + ':' + password

            creds_str_bytes = creds_str.encode('ascii')

            creds_str_bytes_b64 = b'Basic ' + base64.b64encode(creds_str_bytes)

            headers['authorization'] = creds_str_bytes_b64.decode('ascii')


        resp, content = h.request(URL, 'POST',

                                  body = content,

                                  headers = headers)


        if resp.status == 200:

            sys.stdout.write(' => success\n')

            dicom_count += 1

        else:
            print(resp)
            sys.stdout.write(' => failure (Is it a DICOM file? Is there a password?)\n')


    except:

        type, value, traceback = sys.exc_info()

        sys.stderr.write(str(value))

        sys.stdout.write(' => unable to connect (Is Orthanc running? Is there a password?)\n')



if os.path.isfile(sys.argv[3]):

    # Upload a single file

    UploadFile(sys.argv[3])

else:

    # Recursively upload a directory

    for root, dirs, files in os.walk(sys.argv[3]):

        for f in files:

            UploadFile(os.path.join(root, f))



if dicom_count + json_count == total_file_count:

    print('\nSUCCESS: %d DICOM file(s) have been successfully imported' % dicom_count)

else:

    print('\nWARNING: Only %d out of %d file(s) have been successfully imported as DICOM instance(s)' % (dicom_count, total_file_count - json_count))


if json_count != 0:

    print('NB: %d JSON file(s) have been ignored' % json_count)


print('')