# quiltz-domain

Python domain concepts for quiltz

## Purpose

At [QWAN](https://www.qwan.eu) we're building some applications in Python. We collect useful stuff in
the different Quiltz projects:

* **quiltz-domain** (this package) contains domain oriented support modules like entity
  ids, results, email anonymization, validators and parsers
* [**quiltz-testsupport**](https://github.com/qwaneu/quiltz-testsupport) contains test support modules, that supports e.g. automated testing for SMTP integration, probing asynchronous results and
  asserting log statements
* [**quiltz-messaging**](https://github.com/qwaneu/quiltz-messaging) contains a
  messaging domain concept and an engines to send messages. Currently only
  sending emails over SMTP is supported.

## Installing 

```bash
pip install quiltz-domain
```

See [documentation](doc/index.md)
