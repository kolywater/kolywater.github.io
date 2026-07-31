#!/usr/bin/env python3
"""Local preview that behaves like GitHub Pages.

The site links to pages without the .html extension (href="konbit"). GitHub
Pages resolves those to konbit.html; python -m http.server does not, so every
nav link 404s under a plain static server. This adds that one behaviour.

    python3 preview.py [port]     # default 8899
"""
import functools
import http.server
import os
import sys


class PagesHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        full = super().translate_path(path)
        if not os.path.exists(full) and not path.endswith('/'):
            if os.path.isfile(full + '.html'):
                return full + '.html'
        return full

    def log_message(self, fmt, *args):
        code = args[1] if len(args) > 1 else ''
        if str(code).startswith(('4', '5')):
            super().log_message(fmt, *args)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8899
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    handler = functools.partial(PagesHandler, directory=os.getcwd())
    with http.server.ThreadingHTTPServer(('127.0.0.1', port), handler) as httpd:
        print(f'preview: http://localhost:{port}/  (ctrl-c to stop)')
        httpd.serve_forever()


if __name__ == '__main__':
    main()
