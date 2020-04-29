# Installation and Deployment

## Installation

To install the Python package, use pip:

```
pip install nbforms
```

## Server Deployment

Before using nbforms in a notebook, you must deploy a webapp to Heroku which will collect and organize the responses. If you plan to have multiple notebooks, you only need one server, as you can provide a notebook identifier in the config files that will distinguish responses.

The webapp is maintained in [chrispyles/nbforms-server](https://github.com/chrispyles/nbforms-server) on Github. Click the button below to deploy to Heroku:

[![](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/chrispyles/nbforms-server)

Each server comes with a config generator, which will automatically generate the configuation file needed to run nbforms in the notebook (cf. [Notebook Usage](notebook_usage.md)).

## Managing the Server

The server prevents any user data from coming out through HTTP requests by ensuring that the only "identifier" for any individual that can get sent in a response is a randomly generated hash. The only way to extract a user's responses attached to their username is to run rake tasks on the Heroku dyno, which will print a CSV to the console. Some rake tasks are described in the sections they correspond to, although a comprehensive list is provided below.

| Task | Description |
|------|-------------|
| `rake attendance:open[NB_ID]` | Opens attendance on the notebook with identifier `NB_ID` |
| `rake attendance:close[NB_ID]` | Closes attendance on the notebook with identifier `NB_ID` |
| `rake attendance:report[NB_ID]` | Reports attendance on the notebook with identifier `NB_ID` (cf. [Attendance](attendance.md)) |
| `rake lock:question[NB_ID,Q_ID]` | Locks a question `Q_ID` in notebook `NB_ID` from being queried through requests |
| `rake lock:notebook[NB_ID]` | Locks all questions in a notebook `NB_ID` from being queried through requests |
| `rake unlock:question[NB_ID,Q_ID]` | Unlocks a question `Q_ID` in notebook `NB_ID` from being queried through requests |
| `rake unlock:notebook[NB_ID]` | Unlocks all questions in a notebook `NB_ID` from being queried through requests |
| `rake clear:all` | Deletes all responses in the database |
| `rake clear:user[USERNAME]` | Deletes all responses for user with username `USERNAME` |
| `rake reports:notebook[NB_ID]` | Prints a CSV of all responses to notebook `NB_ID` to the console (**with** identifying information) |

<!-- rake tasks, etc. -->
