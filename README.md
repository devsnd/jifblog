# jifblog
A super simple blog for publishing JIFs

They are JIFs, because the GIFs creator said so.

http://www.independent.co.uk/life-style/gadgets-and-tech/news/gif-inventor-steve-wilhite-says-it-should-be-pronounced-jif-8626882.html

-----------

To run JIFBLOG, just put a configuration.env in the root directory

secrets.env

```
DJANGO_SECRET_KEY=some_really_secret_key
```

to generate the secrets, use the gen_configuration_env.py

```
python gen_configuration_env.py > configuration.env
```