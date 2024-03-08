# plone.edu

A new Plone Distribution

## Features

### Content Types

- TBD

### Initial content

This package contains a simple volto configuration.

## Installation

Install plone.edu with `pip`:

```shell
pip install plone.edu
```

And to create the Plone site:

```shell
make create_site
```

## Development

Checkout repo:

```shell
git checkout git@github.com:collective/plone.edu.git
cd plone.edu
make
make create-site
```

Start backend instance:

```shell
make start
```

Export content:

http://localhost:8080/Plone/@@dist_export_all

Re-create the site:

DELETE_EXISTING=1 make create-site

## Contribute

- [Issue Tracker](https://github.com/collective/plone.edu/issues)
- [Source Code](https://github.com/collective/plone.edu/)

## License

The project is licensed under GPLv2.
