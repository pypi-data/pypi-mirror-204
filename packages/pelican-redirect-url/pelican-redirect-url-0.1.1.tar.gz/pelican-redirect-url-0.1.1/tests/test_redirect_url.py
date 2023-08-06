#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase

from pelican.contents import Page
from pelican.readers import Readers
from pelican.tests.support import get_settings

from pelican.plugins.redirect_url import redirect_url


# Disable verbose logging of `pelican`.
logging.getLogger().setLevel(logging.WARNING)


class RedirectUrlPluginTestCase(TestCase):
    def _get_html_page_from_markdown(self, markdown: str) -> Page:
        with NamedTemporaryFile(suffix=".md") as path:
            path = Path(path.name)
            path.write_text(markdown)
            result = Readers(get_settings(filenames=dict())).read_file(
                base_path=path.parent,
                path=path.name,
            )
        return result

    @contextmanager
    def _run_on_page(self, page: Page):
        with TemporaryDirectory() as directory:

            class PageGenerator:
                pages = [page]

            class Writer:
                output_path = directory

            redirect_url.overwrite_files(
                page_generator=PageGenerator(), writer=Writer()
            )
            yield Path(directory)

    def test_with_redirect_url(self):
        page = self._get_html_page_from_markdown(
            """\
title: My page
save_as: with_redirect.html
redirect_url: https://www.example.org/hello_world/

### My page

Welcome to my page!
            """
        )
        old_content = page._content

        with self._run_on_page(page=page) as directory:
            self.assertSetEqual(
                {"with_redirect.html"}, {x.name for x in directory.glob("*")}
            )
            new_content = (directory / "with_redirect.html").read_text()
        self.assertNotEqual(old_content, new_content)
        self.assertEqual(
            """\
<!DOCTYPE html>
<html>

    <head>
        <link rel="canonical" href="https://www.example.org/hello_world/" />
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta http-equiv="refresh" content="0;url=https://www.example.org/hello_world/" />
    </head>

    <body>
        <p>This content has moved. If you are not redirected, please click here:</p>
        <p><a href="https://www.example.org/hello_world/">https://www.example.org/hello_world/</a></p>
    </body>

</html>
""",
            new_content,
        )

    def test_without_redirect_url(self):
        page = self._get_html_page_from_markdown(
            """\
title: My page
save_as: without_redirect.html

### My page

Welcome to my page!
            """
        )

        with self._run_on_page(page=page) as directory:
            self.assertSetEqual(set(), {x.name for x in directory.glob("*")})
