extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.asyncio',
]

autoclass_content = 'both'
autodoc_member_order = 'bysource'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.6', None),
}

source_suffix = '.rst'
master_doc = 'index'

project = 'grpclib'
copyright = '2018, Oleksandr Kovalchuk'
author = 'Oleksandr Kovalchuk'

templates_path = []

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'display_version': False,
}
