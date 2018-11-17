Single Sign On
==============

Single sign on is a way to authenticate user in useresponse using external
service as auth provider.

Technically it is implemented the following way:

1. Useresponse redirects user to `yourapp.domain` for logging in
2. External application authenticates user 
3. External app generates special URI on Useresponse domain and redirects user
   to it
4. As soon as user is redirected to that special URI, they are authenticad in
   useresponse

Usage
-----

.. code:: python
   from useresponse.sso import UseresponseSSO

   useresponse = UseresponseSso(
       domain='https://useresponse.domain',
       secret='s3kre7',
       source='example.com',
       full_name='John Doe',
       email='johndoe@example.com',
       user_id=42,
   )
   login_url = useresponse.get_login_url()
   redirect(login_url)

In the example above we create a UseresponseSSO instance, and among other data
provide it a secret, obtained from useresponse.  As soon as we created the
instance, we generate login_url and redirect user to it, using ``redirect``
functionality of the framework we use. 

Useresponse recently added custom fields support in their API. Those are
supported via optional ``properties`` param. Here is how to use it:

.. code:: python
    useresponse = UseresponseSso(
       ...
       properties={
           172: 'lorem ipsum',
           198: '2018-01-01',
       },
    )

Here the key is the custom fields's id, which can be taken from Administration
» Fields & Properties » Users, and the value is the custom field's value
