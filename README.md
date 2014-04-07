## Bearton - static website generation system

Bearton is a system for managing and generating static websites.
It is aimed at people who dislike complex CMS-s like Joomla! or Drupal.

> **NOTICE:** Bearton is still alpha software!

----

### Features

Bearton uses elements which are connected to make pages.
For example, few core elements are `mainmenu`, `header`, `footer` and `head`.
Pages are also elements -- one basic page-element is `home`.

Bearton elements are split into three files:

- Mustache template,
- Mustache context,
- metadata about the element itself (e.g. what other elements it requires - used to build full context to render Musatche),

----

### Technology

Bearton is built upon Mustache and uses Muspyche as a library implementing this framework.

Bearton is not compatible with other Mustache implementations since it relies on some features
unique to Muspyche (which were, in turn, taken from a post about Mustache 2.0) -- mostly global
context access from the inside of sections.  
This extension of Mustache standard is required to build static websites with varying paths to
root directory (e.g. for including CSS and JavaScript) and
is a must-have for Bearton since it uses multiple contexts to render its Mustache templates.

**Software required to work with Bearton:**

- Python 3.x (Python from 2.x line won't work),
- Muspyche library,
- webserver (e.g. nginx),

Everything is kept on user machine - only generated HTML and reuired assets have to be sent
to the remote server.  
This provides users with the ability to work while being offline, and upload the results of work
when the connection becames available.

----

### License

Bearton is free software published under GNU GPL v3 license.

----

Copyright (c) 2014 Marek Marecki <github dot com slash marekjm>
