"""
Upload files to ShotGrid.
"""
import argparse
import glob
import os

from shotgun_api3 import Shotgun, ShotgunError


def sg_upload_with_retry(sg, entity_type, entity_id, path, field_name=None,
                         display_name=None, tag_list=None, retries=1):
    """
    :param shotgun_api3.shotgun.Shotgun sg: A shotgun API instance.
    :param str entity_type: Entity type to link the upload to.
    :param int entity_id: Id of the entity to link the upload to.
    :param str path: Full path to an existing non-empty file on disk to upload.
    :param str field_name: The ShotGrid field name on the entity to store the file in.
        This field must be a File/Link field type.
    :param str display_name: The display name to use for the file. Defaults to the file name.
    :param str tag_list: comma-separated string of tags to assign to the file.
    :param int retries: How often to retry to upload. Can be between 0 and 3.
    :returns: ID of the Attachment entity that was created for the image.
    :rtype: int
    :raises ShotgunError: When an error occurred during upload after
                          the maximum retries have been reached.
    """
    retries = max(0, min(retries, 3))
    retry = 0
    while True:
        retry += 1
        try:
            return sg.upload(entity_type=entity_type, entity_id=entity_id, path=path,
                             field_name=field_name, display_name=display_name, tag_list=tag_list)
        except ShotgunError:
            if retry > retries:
                raise


def cli(args=None):
    """
    Command line interface.

    :param list[str]|None args: The list of command line arguments.
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
    parser.add_argument('-field', '--entity_field', required=True,
                        help='The name of the entity field to upload to.')

    args = parser.parse_args(args)

    shotgun = Shotgun(base_url=os.environ['SHOTGRID_SITE'],
                      script_name=os.environ['SHOTGRID_SCRIPT_USER'],
                      api_key=os.environ['SHOTGRID_APPLICATION_KEY'])

    upload_file_path = args.input
    if any((glob_chr in upload_file_path for glob_chr in ['*', '?', '[', ']'])):
        upload_file_path = sorted(glob.glob(upload_file_path))[0]

    sg_upload_with_retry(sg=shotgun,
                         entity_type=args.entity_type,
                         entity_id=args.entity_id,
                         path=upload_file_path,
                         field_name=args.entity_field)


if __name__ == '__main__':
    cli()
