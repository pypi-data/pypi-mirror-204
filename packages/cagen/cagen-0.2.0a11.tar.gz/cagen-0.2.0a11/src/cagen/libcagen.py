#!/usr/bin/env python

# SPDX-FileCopyrightText: 2023 Xavier Bordoy <somenxavier@posteo.net>
#
# SPDX-License-Identifier: GPL-2.0-only

"""
This is the library of [cagen project](https://sr.ht/~somenxavierb/cagen/).
The main aim of this library is to convert mardown files to other formats.

It is used in [cagen](https://git.sr.ht/~somenxavierb/cagen/tree/main/item/src/cagen/cagen.py) CLI front-end.
"""


## Python Library imports
from dataclasses import dataclass
from typing import Optional, List
from pprint import pprint
import os.path
import itertools
import types

# External imports
import frontmatter
import pypandoc
from mako.template import Template

class Entry:
    """
    An entry.

    It's simply a markdown file, with optional YAML header frontend. In other words:
    
    ```
    ---
    metadata
    ---
    content
    ```

    This class uses extensively the [frontmatter library](https://python-frontmatter.readthedocs.io/en/latest/) for read and write metadata easyly.
    """

    path: Optional[str]
    """
    The path of the entry, i.e. the path of the markdown file we want to process.
    If the path is None, then only processing fields are the provided by `additionalsearchlist` in `to` method.
    """

    def __init__(self, path: str):
        """Defines the `Entry` from `path`"""
        self.path = path

    @property
    def content(self) -> str:
        """Returns the content of the `Entry`"""
        if self.path != None:
            return frontmatter.load(self.path).content
        else:
            return ""

    @property
    def metadata(self) -> dict:
        """Returns the YAML metadata header (as a `dict`) of the `Entry`"""
        if self.path != None:
            return frontmatter.load(self.path).metadata
        else:
            return {}

    @property
    def to_dict(self) -> dict:
        """Returns the representation of `Entry` as a `dict`, containing metadata and content."""
        if self.path != None:
            return frontmatter.load(self.path).to_dict()
        else:
            return {'content': ""}

    def __str__(self):
        """Defines a representation of `Entry` like `str`"""

        if self.path != None:
            post = frontmatter.load(self.path)
            if 'title' in post.keys():
                return post['title']
            else:
                return self.path
        else:
            return self.path

    def __repr__(self):
        """Defines object representation"""
        return self.path

    def __le__(self, other):
        """Returns when a <= b, where a and b are `Entry` instances."""
        return self.__str__() <= other.__str__()

    def __lt__(self, other):
        """Returns when a < b where a and b are `Entry` instances."""
        return self.__str__() < other.__str__()

    def pandoc_convert(self, destsyntax: str = 'html5', removingheaders: bool = True) -> str:
        """
        Simply uses [pandoc](https://pandoc.org/) to convert `Entry` to `destsyntax` syntax.
        
        - If `removingheaders == True`, we remove all headers except the bibliography information from YAML metadata
        - If `removingheaders == False`, we convert the whole file.
        """

        if self.path != None:
            post = frontmatter.load(self.path)

            if removingheaders == True:
                # Remove all headers in YAML frontend except bibliographic ones
                keys = sorted(post.keys())

                for k in keys:
                    if k != 'references':
                        post.__delitem__(k)
            
            # This is the original markdown file
            #   - with all keys in metadata removed except references; in case of removingheaders == True
            #   - with no changes; in case of removingheaders == False
            markdown = frontmatter.dumps(post)
        else:
            markdown = ""

        # calling pandoc with options
        extra_args = ["--citeproc", "--katex", "--metadata=link-citations:true"]
        return pypandoc.convert_text(markdown, to=destsyntax, format="markdown+smart+ascii_identifiers+citations+strikeout", extra_args=extra_args)

    def to(self, mytemplatepath: str,  additionalsearchlist: dict = {}, destsyntax: str = 'html5') -> str:
        """
        It is basically a convert with using [Mako template system](https://www.makotemplates.org/).
        It calls `pandoc_convert` with `removingheaders == True` and it saves as `conversion` variable
        It saves all metadata variables.
        The template could use all these variables.
        
        It returns the rendered template.

        In the template, you can use the values of the variables on the metadata of the `Entry`.
        Also, you can pass additional list of variables and values as dict to use in a template.
        """

        mysearchlist = self.to_dict
        mysearchlist['conversion'] = self.pandoc_convert(destsyntax)

        # Merging two dictionaries using |= method
        mysearchlist |= additionalsearchlist
        tmp = Template(filename=mytemplatepath)
        return tmp.render(**mysearchlist)



class Collection:
    """A collection of `Entry` instances"""

    entries: list
    """A list of entries"""

    def __init__(self, filenames: list):
        """Initializes the `Collection` from a list of filenames. Non-existing files are ignored."""
        self.entries = [Entry(p) for p in filenames if os.path.exists(p)]

    def __str__(self):
        """Returns a str representation of `Collection`"""
        return ", ".join([e.__str__() for e in self.entries])

    def values(self, criterium: types.FunctionType):
        """
        Returns the values of criterium(x) for all x in `self.entries`.

        - When criterium(x)=y is not a list, we add y to `values`
        - When criterium(x)=y is a list, we add z to `values` for every z in y.

        It is mainly related to `group_by` method.
        """

        # Compute the values
        vals = []
        for v in [criterium(e) for e in self.entries]:
            if isinstance(v, list):
                for element in v:
                    vals.append(element)
            else:
                vals.append(v)

        # Remove repated elements
        uniq = []
        [uniq.append(x) for x in vals if x not in uniq]

        return uniq


    def group_by(self, criterium: types.FunctionType):
        values = self.values(criterium)
        grouped = {}

        for v in values:
            grouped[v] = []
            for x in self.entries:
                c = criterium(x)
                if isinstance(c, list) and v in c:
                    grouped[v].append(x)
                if c == v:
                    grouped[v].append(x)
        return grouped

def extract_assignments(listofwords: Optional[List[str]], splitter: str = "=") -> dict:
    """
    Extracts assignments of the type `<variable>`=`<value>` from a list of words (separated of spaces) `listofwords`. The `splitter` is the character which splits words into variable and value.

    Example:

    if
    ```
    splitter == ':'
    ``` 
    and
    ```
    listofwords == date:2022-04-02 title='this is a title'
    ```
    then it produces
    ```
    {'date': '2022-04-22', 'title': 'this is a title'}
    ```

    Note we just split *once*. So,
    ```
    listofwords == date:foo:bar
    ```
    produces
    ```
    {'date': 'foo:bar'}
    ```

    Note that words without splitter will be ignored.

    Example:
    ```
    listofwords == foo date:2022-04-02
    ```
    produces
    ```
    {'date': '2022-04-22'}
    ```
    (`foo` is ignored because it lacks splitter (in our case `':'`))
    """

    assignments = {}
    if listofwords != None:
        for word in listofwords:
            parts = word.split(splitter, maxsplit=1)
            # if we match `splitter`, OK. Else ignore the word
            if len(parts) == 2:
                assignments[parts[0]] = parts[1]

    return assignments

def evaluate_assignments(assignments: Optional[dict], evals: Optional[list]) -> dict:
    """
    It tries to evaluate the assignments in `assignments` variables which appear in `evals` list.

    Example:
    ```
    assignments == {'revision': '1'}
    evals = ['revision']
    ```
    produces:
    ```
    {'revision': 1}
    ```

    If the cast is not possible, it cast the variable as `str` and not returning any error (just printed message).
    """

    if assignments != None:
        if evals != None:
            if isinstance(evals, list):
                for variable in evals:
                    try:
                        assignments[variable] = eval("{}".format(assignments[variable]))
                    except:
                        print("{} cannot be evaluated. Stored as str".format(variable))
    return assignments
