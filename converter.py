# converter.py
from markdown import markdown


# Default extensions: extra (tables, fenced code), codehilite (syntax highlighting)
DEFAULT_EXTENSIONS = [
'extra',
'codehilite',
'toc',
]


DEFAULT_EXTENSION_CONFIGS = {
'codehilite': {
'linenums': False,
'guess_lang': True,
}
}




def md_to_html(md_text: str, extensions=None, extension_configs=None) -> str:
"""Convert markdown text to full HTML body (not a full HTML page).


Returns HTML string that you can insert into a template.
"""
if extensions is None:
extensions = DEFAULT_EXTENSIONS
if extension_configs is None:
extension_configs = DEFAULT_EXTENSION_CONFIGS


# Use `markdown` package to convert
html = markdown(md_text, extensions=extensions, extension_configs=extension_configs)
return html
