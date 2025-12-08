# Processing Power Pack

Extends QGIS processing with additional algorithms.

## Included algorithms
- Unzip File (`unzipfile`): Extracts a ZIP archive to a destination folder.
- Update Field (`updatefield`): Evaluate an expression per feature and write the result to a field (optional feature filter).
- Glob Files (`globfiles`): Search a directory with a glob pattern and return matching paths.
- Copy File (`copyfile`): Copy a file to a destination (optional overwrite).
- Make Folder (`makefolder`): Create a folder (no error if it already exists).
- File Path Operations (`filepathops`): Return parts of a path (parent, basename, name, extension).

## Usage examples
- Unzip:
  - Input: path to `archive.zip`
  - Output: folder where files are extracted
- Glob Files (recursive):
  - Input folder: `C:\data`
  - Pattern: `*.shp`
  - Recursive: true
  - Output: list of file paths as strings
- Update Field:
  - Target layer: vector layer
  - Field to update: `my_field`
  - Expression: `length($geometry)` (or any valid QGIS expression)
  - Filter: optionally `population > 1000`

## Contributing
Open issues or send pull requests in the repository.

## License
GPLv2 or later
