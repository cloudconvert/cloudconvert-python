cloudconvert-python
===================

This is a lightweight wrapper for the
`CloudConvert <https://cloudconvert.com>`__ API.

Feel free to use, improve or modify this wrapper! If you have questions
contact us or open an issue on GitHub.

.. image:: https://img.shields.io/pypi/v/cloudconvert.svg
           :alt: PyPi Version
           :target: https://pypi.python.org/pypi/cloudconvert
.. image:: https://travis-ci.org/cloudconvert/cloudconvert-python.svg?branch=master
           :alt: Build Status
           :target: https://travis-ci.org/cloudconvert/cloudconvert-python

Quickstart
----------

.. code:: python

    import cloudconvert

    api = cloudconvert.Api('your_api_key')

    process = api.convert({
        'inputformat': 'png',
        'outputformat': 'jpg',
        'input': 'upload',
        'file': open('tests/input.jpg', 'rb')
    })
    process.wait() # wait until conversion finished
    process.download("tests/output.png") # download output file

You can use the `CloudConvert API
Console <https://cloudconvert.com/apiconsole>`__ to generate
ready-to-use python code snippets using this wrapper.

Installation
------------

The easiest way to get the latest stable release is to grab it from
`pypi <https://pypi.python.org/pypi/cloudconvert>`__ using ``pip``.

.. code:: bash

    pip install cloudconvert

Download of multiple output files
---------------------------------

In some cases it might be possible that there are multiple output files
(e.g. converting a multi-page PDF to JPG). You can download them all to
one directory using the ``downloadAll()`` method.

.. code:: python

    import cloudconvert

    api = cloudconvert.Api('your_api_key')

    process = api.convert({
        'inputformat': 'pdf',
        'outputformat': 'jpg',
        'converteroptions': {
            'page_range': '1-3'
        },
        'input': 'upload',
        'file': open('tests/input.pdf', 'rb')
    })
    process.wait()
    process.downloadAll("tests")


Alternatively you can iterate over ``process['output']['files']`` and
download them seperately using
``process.download(localfile, remotefile)``.

How to run tests?
-----------------

::

    pip install -r requirements-dev.txt
    export API_KEY=your_api_key
    nosetests

Resources
---------

-  `API Documentation <https://cloudconvert.com/apidoc>`__
-  `Conversion Types <https://cloudconvert.com/formats>`__
-  `CloudConvert Blog <https://cloudconvert.com/blog>`__

.. |Build Status| image:: https://travis-ci.org/cloudconvert/cloudconvert-python.svg?branch=master
   :target: https://travis-ci.org/cloudconvert/cloudconvert-python
