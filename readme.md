# PyMongoCopy

PyMongoCopy is a desktop GUI tool (CustomTkinter) for copying MongoDB documents from a source namespace to a target namespace.

It is designed for Atlas-style URIs and supports:
- separate source and target clusters
- separate source and target database/collection names
- idempotent writes using upsert behavior (`_id`-based)
- clear error handling for auth/TLS/empty-source cases

## App Screenshots

### Main View
![PyMongoCopy main view](assets/app-overview.png)

### Namespace + Action Section
![PyMongoCopy form and action](assets/app-form-and-action.png)

### App Icon
![PyMongoCopy app icon](assets/app-icon-source.png)

### Launcher Icon Preview
![PyMongoCopy launcher icon preview](assets/app-launcher-preview.png)

## Requirements

- Python 3.9+ (3.10+ recommended)
- macOS, Linux, or Windows
- MongoDB user credentials with read access to source and write access to target

## Setup

1. Clone or download this project.
2. Create and activate a virtual environment.
3. Install dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install customtkinter pymongo certifi
```

## Run the Project

From the project root:

```bash
python3 script.py
```

## How to Use

1. Enter **SOURCE URI** and **TARGET URI**.
2. Enter **SOURCE DATABASE** and **SOURCE COLLECTION**.
3. Enter **TARGET DATABASE** and **TARGET COLLECTION**.
4. Click **START MIGRATION**.

On completion, a summary dialog shows scanned/inserted/updated counts and source/target namespaces.

## URI Notes

- Atlas format example:
  - `mongodb+srv://username:password@cluster0.xophswp.mongodb.net/?authSource=admin&retryWrites=true&w=majority`
- If your password has special characters (`@`, `:`, `/`, `?`, `#`, `%`), URL-encode it.
- Ensure Atlas Network Access allows your current IP.

## Build as a macOS App (Optional)

```bash
pip install pyinstaller
pyinstaller --clean --windowed --name "PyMongoCopy" --icon "assets/app-icon.icns" --collect-all customtkinter script.py
ls dist
open dist/PyMongoCopy.app
```

The production launcher icon is configured from:
- source image: `assets/app-icon-source.png`
- macOS icon file used by PyInstaller: `assets/app-icon.icns`

You can also build directly from the spec file:

```bash
pyinstaller --clean PyMongoCopy.spec
```

## Build Troubleshooting

If PyInstaller reports:

`The 'pathlib' package is an obsolete backport...`

remove the global backport package, then rebuild:

```bash
/usr/local/bin/python3 -m pip uninstall -y pathlib
/usr/local/bin/python3 -m pip show pathlib
pip install pyinstaller
pyinstaller --clean --windowed --name "PyMongoCopy" --icon "assets/app-icon.icns" --collect-all customtkinter script.py
```

`pip show pathlib` should return `Package(s) not found`.

If `dist/PyMongoCopy.app` still does not exist, the build did not complete; check the PyInstaller error output and fix that first.
