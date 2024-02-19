# Changelog

**v1.0.0:**

* Rewrote nbforms-server in Python
* Restructure server so that it can run on on an individual's machine instead of needing to be deployed to the cloud
* Changed server database from PostgresQL to SQLite
* Rewrote Python client library
* Removed support for Google OAuth to authenticate with a server instance
* Added ability to seed users from a CSV file for a server instance
* Allowed users to enter server URL during authentication

**v0.5.1:**

* Changed core class from `Notebook` to `Form`
* Changed API key storage to `dict` to store one key for each server URL in the case of different configs
