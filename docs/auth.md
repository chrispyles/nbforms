# OAuth Providers

## nbforms Auth

nbforms auth is the default auth provider, and is very simple. When you instantiate a Notebook, it will ask the user to input a username and a password. If the username already exists on the server, the password will be checked and an API key will be generated, to be stored in the `Notebook` class. If it does not exist, a new user will be created, and an API key generated. If the user _does_ exist but an incorrect password is provided, the cell will error. As noted in [Notebook Usage](notebook_usage.md), logging in creates a global variable that means if another `Notebook` instance is created, the user will _not_ be asked to log in again.

## Google OAuth

To use Google OAuth, you need to get set up a GCP project with OAuth and use the [Heroku dashboard](https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard) to set up the necessary environment variables. You should set `GOOGLE_KEY` to your client ID and `GOOGLE_SECRET` to your client secret.
