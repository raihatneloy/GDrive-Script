#!/usr/bin/env python

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from pprint import pprint
import json, yaml
import io
import os
import httplib2
import click

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

store = Storage('gdriveauth')
credentials = store.get()
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)

@click.group()
def cli():
    """Gdrive Management"""


def list_file(folder_id='root', max_files=1000, output_file=None):
    results = service.files().list(
            q="'%s' in parents and trashed=False" % folder_id,
            pageSize=max_files
        ).execute()

    file_path = None
    if output_file:
        file_path = open(output_file, 'w')

    files = []
    max_name_len = 0
    max_id_len = 0

    for file in results.get('files',[]):
        info = {}
        info['name'] = file['name']
        info['type'] = file['mimeType']
        info['id'] = file['id']

        max_name_len = max(max_name_len, len(file['name']))
        max_id_len = max(max_id_len, len(file['id']))

        files.append(info)

    if output_file:
        file_path.write(yaml.safe_dump({'files': files}, default_flow_style=False))
    else:
        for file in files:
            print "Name: %s Id: %s Type: %s" % (file['name'].ljust(max_name_len+1, ' '), file['id'].ljust(max_id_len+1, ' '), file['type'])


@cli.command()
@click.option('--id', help='ID of the parent directory')
@click.option('--url', help='URL of the parent directory')
@click.option('-m', '--mx' , type=int, default=1000, help='Max number of files')
@click.option('-o', '--output-file', help='Output the list in a file')
def list(id, url, mx, output_file):
    if id and not url:
        list_file(id, mx, output_file)
    elif not id and url:
        if url.find('id=') != -1:
            index = url.find('id=')+3
            id = url[index:]
        else:
            if url.find('?usp=sharing') != -1:
                url = url[:-12]
            id = url.split('/')
            id = id[-1]
        list_file(id, mx, output_file)
    elif not id and not url:
        list_file()


@cli.command()
@click.option('--id', help='ID of the file to download')
@click.option('-f', '--file', help='Specify file to read info regarding download')
@click.option('-o', '--output-dir', default='output/', help='Path to the directory where to save the file, default = ./output/*')
def download(id, file, output_dir):
    to_download = []

    if file:
        to_download = yaml.load(open(file).read())['files']
            
    if id:
        metadata = service.files().get(
                fileId=id
            ).execute()
        to_download.append({
                'name': metadata['name'],
                'type': metadata['mimeType'],
                'id': metadata['id']
            })

    for file_info in to_download:
        try:
            request = service.files().get_media(fileId=file_info['id'])
            fh = io.FileIO(output_dir + '/' + file_info['name'], 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False

            while done is False:
                status, done = downloader.next_chunk()
                print('Download %d%%.' % int(status.progress() * 100))
        except:
            pass


if __name__ == "__main__":
    cli()