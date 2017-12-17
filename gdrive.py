#!/usr/bin/env python

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json
import os
import click

@click.group()
def cli():
	"""GDrive Management"""


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

access_token = json.loads(open('gdriveauth').read())
access_token = access_token['access_token']

def list_file(folder_id='root', max_files=100000, output_file=None):
	command = "./google-drive --access-token %s list -q '\"%s\" in parents and trashed=False' -m %d" % (access_token, folder_id, max_files)
	
	if output_file:
		stdout = os.popen(command).read()
		output_file = open(output_file, 'w')

		output_file.write(stdout)
		output_file.close()
	else:
		os.system(command)


@cli.command()
@click.option('--id', help='ID of the parent directory')
@click.option('--url', help='URL of the parent directory')
@click.option('-m', '--mx' , type=int, default=100000, help='Max number of files')
@click.option('-o', '--output-file', help='Output the list in a file')
def list(id, url, mx, output_file):
	if id and not url:
		list_file(id, mx, output_file)
	elif not id and url:
		if url.find('id='):
			index = url.find('id=')+3
			id = url[index:]
			list_file(id, mx, output_file)


if __name__ == "__main__":
	cli()