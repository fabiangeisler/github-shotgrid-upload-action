# github-shotgrid-upload-action
GitHub action to upload an artefact to a ShotGrid entity

The purpose of this GitHub workflow is to automate the uploading of your SGTK config
as explained in [this workflow](https://developer.shotgridsoftware.com/tk-core/initializing.html#uploading-a-configuration-to-shotgrid).
There might be other use cases for it. Let me know if you find one :). 

# Usage
Here is an example how to use the GitHub action.

```yaml
# When a release on GitHub is created we upload the repository zip file to a
# Pipeline configuration entity in ShotGrid.
name: Publish to ShotGrid

on:
  release:
    types: [published]

jobs:
  publish:
    name: Publish release to ShotGrid
    runs-on: ubuntu-latest
    steps:
      - name: Download repo zip file
        uses: robinraju/release-downloader@v1.4
        with:
          tag: "${{ github.ref_name }}"
          zipBall: true
          token: "${{ github.token }}"

      - name: Upload to ShotGrid
        uses: fabiangeisler/github-shotgrid-upload-action@v1
        with:
          upload_file: REPOSITORY-NAME-*.zip
          entity_type: PipelineConfiguration
          entity_id: 1
          field_name: uploaded_config
          shotgrid_base_url: ${{ secrets.SHOTGRID_BASE_URL }}
          shotgrid_script_name: ${{ secrets.SHOTGRID_SCRIPT_NAME }}
          shotgrid_api_key: ${{ secrets.SHOTGRID_API_KEY }}
```
