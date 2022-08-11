"""
Upload a file to a ShotGrid entity.
"""
import argparse
import glob
import os

from shotgun_api3 import Shotgun


def main(cli_args=None):
    """
    Upload a file to a ShotGrid entity field based on the given cli arguments.

    :param list[str]|None cli_args: The list of command line arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True,
                        help='The file to upload. Glob patterns are supported '
                             'but only the first matching file will be uploaded.')
    # noinspection PyTypeChecker
    parser.add_argument('-id', '--entity_id', type=int, required=True,
                        help='The ID of the entity to upload to.')
    parser.add_argument('-type', '--entity_type', required=True,
                        help='The ShotGrid type of the entity.')
    parser.add_argument('-field', '--field_name', required=True,
                        help='The name of the entity field to upload to.')

    args = parser.parse_args(cli_args)

    upload_file_path = args.input
    if any((glob_chr in upload_file_path for glob_chr in ['*', '?', '[', ']'])):
        upload_file_path = sorted(glob.glob(upload_file_path))[0]

    sg = Shotgun(base_url=os.environ['SHOTGRID_SITE'],
                 script_name=os.environ['SHOTGRID_SCRIPT_USER'],
                 api_key=os.environ['SHOTGRID_APPLICATION_KEY'])

    print('Upload file "{}" to {} (id: {}) {}.'.format(upload_file_path,
                                                       args.entity_type,
                                                       args.entity_id,
                                                       args.field_name))
    attachment_id = sg.upload(entity_type=args.entity_type,
                              entity_id=args.entity_id,
                              path=upload_file_path,
                              field_name=args.field_name)

    print('Upload successful. Created attachment with ID {}'.format(attachment_id))


if __name__ == '__main__':
    main()
