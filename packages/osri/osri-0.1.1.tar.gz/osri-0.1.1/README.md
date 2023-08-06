# OSRI: OS Release Info

A CLI that shows parsed data from an linux os release file, usually located at /etc/os-release.

## Installation

Install from a git branch:

```sh
pip install git+https://github.com/odra/osri.git@master
```

## Usage

Showing the CLI version:

```sh
osri version
```

Displaying an os release info (path defaults to `/etc/os-release`):

```sh
osri display
osri display --path /etc/another-os-release
```

## License

[MIT](./LICENSE)
