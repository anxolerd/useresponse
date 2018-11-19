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

.. automodule:: useresponse.sso
  :members:
