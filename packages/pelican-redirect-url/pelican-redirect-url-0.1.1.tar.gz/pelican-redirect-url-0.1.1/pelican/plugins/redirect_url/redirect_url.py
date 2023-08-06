#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pelican plugin for redirecting to URLs.

This Pelican plugin allows you to generate pages which redirect to any URL,
using plain HTML.
"""

from pathlib import Path

from pelican.generators import PagesGenerator
from pelican.plugins import signals
from pelican.writers import Writer


TEMPLATE = """\
<!DOCTYPE html>
<html>

    <head>
        <link rel="canonical" href="{redirect_url}" />
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta http-equiv="refresh" content="0;url={redirect_url}" />
    </head>

    <body>
        <p>This content has moved. If you are not redirected, please click here:</p>
        <p><a href="{redirect_url}">{redirect_url}</a></p>
    </body>

</html>
"""


def overwrite_files(page_generator: PagesGenerator, writer: Writer):
    """
    Overwrite the generated page files if they are redirects.

    :param page_generator: The generated pages.
    :param writer: The page writer.
    """
    for page in page_generator.pages:
        redirect_url = page.metadata.get("redirect_url")
        if not redirect_url:
            # Keep pages which should not carry a redirect.
            continue
        rendered = TEMPLATE.format(redirect_url=redirect_url)
        path = Path(writer.output_path, page.save_as)
        path.write_text(rendered)


def register():
    """
    Act after the regular page content has been written. This is required as we
    want to overwrite the content of some pages. Adding a dedicated generator as
    in the `pelican-redirect` plugin does not really work here, as Pelican will
    warn about two generators writing to the same file. This is the expected
    behaviour in our case, but the plugin tries to avoid any confusion for the
    user by re-writing the file with plain filesystem functionality.
    """
    signals.page_writer_finalized.connect(overwrite_files)
