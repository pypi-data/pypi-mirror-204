# URL Redirection Plugin for Pelican

Pelican plugin for redirecting to URLs.

This Pelican plugin allows you to generate pages which redirect to any URL, using plain HTML.

## Installation

The package is available on PyPI and can be installed using `pip install pelican-redirect-url`.

Alternatively, you may want to install it straight from a source checkout: `python -m pip install .`

## Usage

Include the plugin by adding it to your `pelicanconf.py` and add the `redirect_url` directive to the metadata block of the corresponding page:

```
redirect_url: https://github.com
```

## Credits

This plugin draws some inspiration from the [pelican-redirect](https://github.com/bryanwweber/pelican-redirect) plugin by Bryan Weber. Nevertheless, the target usage of both plugins differs, and so does the implementation.
