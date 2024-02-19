# Notebook Usage

## Configuration File

nbforms requires a JSON-formatted config file to set up the `Form` class. The default path that `Form` checks is `./nbforms_config.json`, although you can pass a custom path to the `Form` constructor. The structure of the config file is very specific; it contains the information that the notebook needs to create widgets and send requests. The structure of this file is:

```javascript
{
    "server_url": "",      // URL to your Heroku app; optional
    "notebook": "",        // an identifier for this notebook to group responses together
    "auth": "",            // the type of authentication used by this server instance; optional
    "questions": [
      {
        "identifier": "",  // an identifer for this question, unique within this notebook
        "type": "",        // the question type
        "question": "",    // the question text
        "options": [       // options from which to choose if type is multiplechoice or checkbox
          "option 1",
          "option 2",
          // etc.
        ],
        "placeholder": ""  // placeholder text if type is text or paragraph; optional
    },
    // etc.
  ]
}
```

There is a sample config file [here](https://github.com/chrispyles/nbforms/blob/main/demo/nbforms_config.json).

### Server URL

The `server_url` key should be the URL to your nbforms-server instance including the protocol (e.g. `https://myserver.herokuapp.com`). If this key is not provided, users will be prompted to enter it before providing their authentication credentials. This allows you to leave this field out of the config and ask users to enter it for cases in which the URL is ephemeral (e.g. if you're running the server on your machine with something like ngrok for tunneling into it).

### Notebook identifier

The `notebook` key should be some string or number to identify the notebook that you're deploying. This is used to keep the notebook responses distinguished on the server. There is no need to create this notebook on the server; whenever the server receives a request with a notebook identifier unknown to it, it creates a new notebook row in the database.

### Authentication

The `auth` key is used to indicate what type of authentication the server instance you're running uses. It can be either `default` or `none` (`default` is assumed if this key is not provided). In the `none` cause, the server must be configured to create a new user every time someone authenticates by setting the `NBFORMS_SERVER_NO_AUTH_REQUIRED` environment variable to `true` in the environment that the server is running. In this case, the user will not be asked to enter credentials to authenticate.

### Questions

The `questions` tells nbforms what questions are available to ask the user. Questions can have one of four types: `multiplechoice`, `checkbox`, `text`, or `paragraph`. The `type` key in the question is used to create the correct widget. If you have a `multiplechoice` or `checkbox`, you must provide a list of options as the `options` key. For `text` and `paragraph` responses, you can provide an optional `placeholder` key which will replace the default placeholder.

Note that the `checkbox` type currently does not display actual checkboxes, but a list of options in a select box that users can use the Ctrl/Cmd key to select multiple options within. nbforms also parses the results of checkbox questions as tuples, so the data from these questions, when it is read into a `DataFrame` or `Table`, will need further parsing by the user.

## Using the `Form` API

To use the nbforms, you must first import it and create a `Form` instance. 

```python
import nbforms
form = nbforms.Form()
```

When this cell is run, it will first load the config file and check whether the server URL is provided. If it's not, it will ask the user to enter the server URL with an input prompt. Then, it will ask the user to provide their username and password (if `auth` is not `none`) and send a request to the server to obtain the user's API key.

### Collecting Responses

To collect the responses for a question, insert a cell that calls the `Form.ask` function on the **identifier** of the question.

```python
form.ask("q1")
```

This will output the widget and a "Submit" button that, when clicked, will send an HTTP request to your nbforms server with the student's API key, notebook ID, question identifier, and response to be stored on the server.

`Form.ask` can accept multiple questions; for example, `form.ask("q1", "q3")` would display a widget with `q1` and `q3`. Passing no arguments to `Form.ask` will display all of the questions.

### Retrieving Data

nbforms allows you to get your data from the server and collect it into either a datascience `Table` or a pandas `DataFrame`. To retrieve the responses from the server, use `Form.to_table` or `Form.to_df`; the optional `user_hashes` argument (default `False`) indicates whether or not to include a column with a pseudonymized username.

```python
# datascience Table
form.to_table("q1", "q2", ...)

# pandas DataFrame
form.to_df("q1", "q3", ..., user_hashes=True)
```

**Important:** The server route that these methods use to retrieve the data requires no authentication. This means that anyone with the server URL will be able to download any of the data in the responses provided by users. Be very careful about what kind of data you ask users to input to the server; it should not be used to store things like [PII](https://en.wikipedia.org/wiki/Personal_data).
