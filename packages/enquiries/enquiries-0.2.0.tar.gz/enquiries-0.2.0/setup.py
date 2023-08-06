# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enquiries']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'curtsies>=0.3.4,<0.4.0']

setup_kwargs = {
    'name': 'enquiries',
    'version': '0.2.0',
    'description': 'Ask simple questions - get simple answers',
    'long_description': 'Enquiries\n=========\n\n``enquiries`` aims to provide a straightforward way to get decisions from your users.\nIt can offer multiple choice, yes/no or free text\n\n.. code-block:: python\n\n    import enquiries\n\n    options = [\'thing 1\', \'thing 2\', \'thing 3\']\n    choice = enquiries.choose(\'Choose one of these options: \', options)\n\n    if enquiries.confirm(\'Do you want to write something?\'):\n        text = enquiries.freetext(\'Write something interesting: \')\n        print(text)\n\nInput for these questions is fully interactive and prevents any incorrect\nresponses. No more loops checking if the answer matches the question. No more\nmapping the text entered to original objects. Let users choose the objects\ndirectly.\n\n.. image:: https://asciinema.org/a/6OyuQH9H03vSP2gf79f0KwaCO.png\n   :target: https://asciinema.org/a/6OyuQH9H03vSP2gf79f0KwaCO\n   :width: 80%\n\nMultiple choice\n---------------\nAll choices consist of letting users pick one of several items. For ``enquiries`` these\ncan be in any iterable.\n\nUsers can pick one or many of the options offered to them.\n\nSingle Selection\n~~~~~~~~~~~~~~~~\n\nFor single choice, use the ``choose`` method with the list of choices.\n\n.. code-block:: python\n\n    >>> options = [\'Thing 1\', \'Thing 2\']\n    >>> response = enquiries.choose(\'Pick a thing\', options)\n    # interactive prompt\n    >>> print(\'You chose "{}"\'.format(response))\n    You chose "Thing 1"\n    >>>\n\nThe interactive prompt here appears as list of options you can scroll through\nand select using the return key::\n\n    Pick a thing\n    > Thing 1\n      Thing 2\n      Thing 3\n\nWhere up/down arrow keys will scroll through the options moving the ``>``\nmarker. The currently selected option is also in bold typeface (if the terminal\nsupports it).\n\nMultiple Selections\n~~~~~~~~~~~~~~~~~~~\nFor cases where the user can choose multiple options, the ``multi`` keyword can\nbe used.\n\n.. code-block:: python\n\n    >>> options = [\'Thing 1\', \'Thing 2\', \'Thing 3\']\n    >>> response = enquiries.choose(\'Pick some things\', options, multi=True)\n    # interactive prompt\n    >>> print(\'You chose "{}"\'.format(response))\n    You chose "[\'Thing1\', \'Thing 3\']"\n    >>>\n\nThe interactive prompt for multiple choice is similar to that used for single\nchoice but the `>` marker is replaces with ◉ and ◌ to signify chosen or not\nchosen. As before, the arrow keys change the selection and the current line is\nbold. The space key is used to mark an option as selected.::\n\n    pick a thing\n    ◉ Thing 1\n    ◌ Thing 2\n    ◌ Thing 3\n\nYes/No Confirmation\n-------------------\n\nUsed to get a simple boolean response from users.\n\n.. code-block:: python\n\n    >>> if enquiries.confirm(\'Do you really want to do the thing\')\n    ...     print(\'Carrying on\')\n    ... else:\n    ...     print(\'Exiting\')\n    ...\n    # interactive prompt\n    Carrying on\n    >>>\n\nResults in the prompt below::\n\n    Do you really want to do the thing? [y/N]\n\nThe prompt for confirmation by default accepts ``y``/``n`` keys to choose and\nreturn to accept the choice. Return without choosing accepts the default value\n(usually ``False``). The keys used and the default can be changed as required.\nBy default, the user should choose y/n then hit return but ``single_key`` mode\ncan be used to remove the need to hit return.\n\n\nFreetext\n--------\n``enquiries`` free text offering is offers a slightly enhanced version of the\n`input <https://docs.python.org/3/library/functions.html>`_ builtin function. It adds multi line support as well as basic\nreadline like controls (``Ctrl-a``, ``Ctrl-w`` etc). The text entry area is also cleared after the text is\naccepted keeping terminal history clean.\n\n.. code-block:: python\n\n    >>> text = enquiries.freetext(\'Write some stuff\')\n    >>> print(text)\n    This is the text you entered\n    on many lines\n    >>>\n\nNew lines in text can be entered using ``Alt``-``Return``.\n',
    'author': 'Peter Holloway',
    'author_email': 'holloway.p.r@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
