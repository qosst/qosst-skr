# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from qosst_skr import __version__


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "qosst-skr"
copyright = "2021-2024, Yoann Piétri"
author = "Yoann Piétri"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.todo",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx-prompt",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

root_doc = "index"

latex_documents = [
    (
        root_doc,
        "qosst-skr.tex",
        "qosst-skr",
        author.replace(", ", "\\and ").replace(" and ", "\\and and "),
        "manual",
    ),
]
latex_elements = {"preamble": r"\usepackage{enumitem}\setlistdepth{9}"}

intersphinx_mapping = {
    "qosst": ("https://qosst.readthedocs.io/en/latest/", None),
    "qosst-core": ("https://qosst-core.readthedocs.io/en/latest/", None),
    "qosst-hal": ("https://qosst-hal.readthedocs.io/en/latest/", None),
    "qosst-bob": ("https://qosst-bob.readthedocs.io/en/latest/", None),
    "qosst-alice": ("https://qosst-alice.readthedocs.io/en/latest/", None),
    "qosst-sim": ("https://qosst-sim.readthedocs.io/en/latest/", None),
}

html_logo = "_static/qosst_logo_square_white.png"
html_theme_options = {
    "logo_only": True,
    "display_version": False,
}
