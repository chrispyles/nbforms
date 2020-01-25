# Notebook Usage

## Configuration File

nbforms requires a JSON-formatted config file to set up the `Notebook` class. The default path that `Notebook` checks is `./nbforms_config.json`, although you can pass a custom path to the `Notebook` constructor. The structure of the config file is very specific; it contains the information that the notebook needs to create widgets and send requests. The structure of this file is:

```python
{
    "server_url": "",             # URL to your Heroku app

    "notebook": "",               # an ID to collect responses

    "auth": "",                   # indicates auth provider, defaults to nbforms

    "questions": [{               # questions to ask, a list of dicts

      "identifier": "",           # a question identifer, should be unique within
                                  # this notebook

      "type": "",                 # question type; can be one of:
                                  #   multiplechoice, checkbox, text, paragraph

      "question": "",             # the question text

      "options": [                # options from which to choose if type is 
        ...                       # multiplechoice or checkbox
      ],
      "placeholder": ""           # placeholder for textbox if type is text or
                                  # paragraph
    }, 
    ...                           # more question dictionaries
  ]
}
```

The `server_url` key should be the URL to your Heroku-deployed nbforms-server, e.g. `https://my-nbforms-server.herokuapp.com`. The `notebook` key should be some string or number to identify the notebook that you're deploying. This is used to keep the notebook responses distinguished on the server. The `auth` key is used to indicate which auth provider you would like to use. Currently, we only offer Google OAuth (`google`). If you do not want to use Google, leave this key out of the config file and the default nbforms auth will be used. Finally, the `questions` key should be a list of dictionaries that define the information for your questions.

There is a sample config file at [`demo/nbforms_config.json`](https://github.com/chrispyles/nbforms/blob/master/demo/nbforms_config.json). Each nbforms-server comes with a page that will generate a config file for you; for example, the config generator for the demo server can be found at [https://nbforms-demo-server.herokuapp.com/config_generator.html](https://nbforms-demo-server.herokuapp.com/config_generator.html).

### Question Types

Questions can have one of four types: `multiplechoice`, `checkbox`, `text`, or `paragraph`. The `type` key in the question is used to create the correct widget. If you have a `multiplechoice` or `checkbox`, you must provide a list of options as the `options` key. For `text` and `paragraph` responses, you can provide an optional `placeholder` key which will replace the default placeholder.

Note that the `checkbox` type currently does not display actual checkboxes, but a list of options in a select box that users can use the Ctrl/Cmd key to select multiple options within. nbforms also parses the results of checkbox questions as tuples, so the data from these questions, when it is read into a DataFrame or Table, will need further parsing by the user.

## Using the Notebook API

To use the nbforms, you must first import it and create a `Notebook` instance. This will load the config file (defaulting to look at `./nbforms_config.json`) and will have the user log in using the auth provider specified in the config file, or the normal nbforms login if none was provided. Note that if there is already an existing `Notebook` instance, the user will not be asked to log in again, as their API key was stored in a global variable that the new instance accessed.

```python
import nbforms
form = nbforms.Notebook()
```

If you elect to use a 3rd party auth provider (indicated in the config file), then the cell above will instead provide a link to that provider's login page. Once the user logs in, they will be redirected back to the nbforms server and given an API key, which they will be asked to enter in the notebook.

### Collecting Responses

To collect the responses for a question, insert a cell that calls the `Notebook.ask` function on the **identifier** of the question. For example, if I had a question `q1`, I would call

```python
form.ask("q1")
```

This will output the widget and a "Submit" button that, when clicked, will send an HTTP POST request to your nbforms server with the student's API key, notebook ID, question identifier, and response to be stored on the server.

`Notebook.ask` can accept multiple questions; for example, `form.ask("q1", "q3")` would display a widget with `q1` and `q3` as its tabs. Passing no arguments to `Notebook.ask` will display all of the questions.

**Users must press the "Submit" button on _each_ tab of the widget, as the button will only send their response for the question in the current tab.** If you call `form.ask("q1", "q3", "q4")`, then users should press "Submit" three times, once in each tab.

### Retrieving Data

nbforms allows you to get your data from the server and collect it into either a datascience `Table` or a pandas `DataFrame`. To retrieve the responses from the server, use `Notebook.to_table` or `Notebook.to_df`; the optional `user_hashes` argument (default `False`) indicates whether or not to include a column with a randomly generated hash as a pseudo-username.

```python
# datascience Table
form.to_table("q1", "q2", ...)

# pandas DataFrame
form.to_df("q1", "q3", ..., user_hashes=True)
```
