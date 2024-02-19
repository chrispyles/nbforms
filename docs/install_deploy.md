# Installation and Deployment

## Installation

To install the Python package, use pip:

```
pip install nbforms
```

## Server Deployment

Before using nbforms in a notebook, you must setup a server to collect and organize the responses. This server can be run on your machine (with a tool like [ngrok](https://ngrok.com) to allow users to connect to it, more on this in the next section) or deployed to the cloud. If you plan to have multiple notebooks, you only need one server, as you can provide a notebook identifier in the config files that will distinguish responses.

The webapp is maintained in [chrispyles/nbforms-server](https://github.com/chrispyles/nbforms-server) on GitHub.

### Running a local server

It is possible to run a development instance of the nbforms server on your machine and allow users to connect to it with a tool like [ngrok](https://ngrok.com). To do this, follow their [getting started guide](https://ngrok.com/docs/guides/getting-started/) to install and setup ngrok, then clone the [server repo](https://github.com/chrispyles/nbforms-server), `cd` into it, and install the dependencies:

```
git clone https://github.com/chrispyles/nbforms-server
cd nbforms-server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Now start the flask app:

```
gunicorn -w 4 -b 127.0.0.1:8000 nbforms_server.wsgi:app
```

Finally, start a tunnel with ngrok:

```
ngrok http 8000
```

Since ngrok generates a different server URL each time you run it, in this case it may be eaiser to leave the server URL out of your nbforms config file and ask users to enter it themselves as part of the authentication process (more info [here](./notebook_usage)).

Note that the process described above involves running a **development** server and allowing anyone with the ngrok URL the ability to send arbitrary requests to your machine, so be very careful about who you share the URL with and don't leave the server or ngrok running any longer than necessary.

## Authentication

<!-- TODO: NBFORMS_SERVER_NO_AUTH_REQUIRED -->

## Managing the Server

The server prevents any user data from coming out through HTTP requests by ensuring that the only "identifier" for any individual that can get sent in a response is a randomly generated hash. The only way to extract a user's responses attached to their username is to run the server's CLI, which connects to the SQLite database file that the application stores its data in.

To run the server's CLI, `cd` into nbforms-server repo and run the `nbfroms_server` package there as a module:

```
python -m nbforms_server --help
```

### Attendance

To open or close attendance on a notebook, use the `attendance` command group:

```
# open attendance
python -m nbforms_server attendance open <notebook identifier>

# close attendance
python -m nbforms_server attendance close <notebook identifier>
```

These commands require that the notebook already exists in the database (notebooks are created whenever the server receives a request with a new notebook identifier). To use this command to create a new notebook in the database, add the `--create` flag.

### Reports

The CLI can be used to generate CSV reports of the data in its database. To generate these reports, use the `reports` command group. Each comand takes an optional destination path argument; if this is left off, the CSV is printed to stdout.

```
# list all users
python -m nbforms_server reports users <dest>

# list all notebooks
python -m nbforms_server reports notebooks <dest>

# list all resonses for a notebook
python -m nbforms_server reports responses <notebook identifier> <dest>

# list all attendance submissions for a notebook
python -m nbforms_server reports attendance <notebook identifier> <dest>
```

### Seeding data

When a user authenticates with the server, the server looks for whether a user with the provided username exists in the database. If none is found, the user's account is created with the password provided. If you want users to use specific usernames but prevent malicious users from creating an account with another user's username and their own password, you can seed the users table with usernames and passwords with the `seed` command.

```
python -m nbforms_server seed <input path>
```

This command requires a CSV file path as its only argument. The CSV file must contain two columns, `username` and `password` (in that order), and should have 1 row for each user to add.

```
username,password
username 1,password 1
username 2,password 2
username 3,password 3
# etc.
```

### Deleting data

To delete response and attendance submission data, the CLI provides the `clear` command group.

```
# delete all responses and atendance submissions
python -m nbforms_server clear all

# delete all responses and atendance submissions linked to a user
python -m nbforms_server clear user <username>

# delete all responses and atendance submissions linked to a notebook
python -m nbforms_server clear notebook <notebook identifier>
```

Each of these commands asks you to confirm that you'd like to delete the data, but this can be prevented with the `--force` flag.
