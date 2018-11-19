API
===

You can use Useresponse REST API from :py:module:`useresponse.api` module.
Currently implemented APIs are:

.. toctree::
  :maxdepth: 2

  users

To use api, you have to initialize it first with the useresponse domain and the
API token, obtained from useresponse.

.. code:: python

   from useresponse.api import API
   api = API('https://useresponse.domain', 'useresponse_api_token')

After API is initialized, you can use its services by simply accessing them by
name:

.. code:: python

   user = api.users.get(42)
