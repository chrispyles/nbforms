# nbforms

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/chrispyles/nbforms/master?filepath=demo%2Fdemo.ipynb)

nbforms is a Python package designed to allow forms to be submitted by users such that the data they submit is immediately available for use in the notebook by the entire group. This is accomplished using ipywidgets and a Heroku-deployable Sinatra webapp, [nbforms-server](https://github.com/chrispyles/nbforms-server).

## Installation

To install the Python package, use pip:

```
pip install nbforms
```

## Deployment

### Setup: Server

Before using nbforms in a notebook, you must deploy a webapp to Heroku which will collect and organize the responses. If you plan to have multiple notebooks, you only need one server, as you can provide a notebook identifier in the config files that will distinguish responses.

To deploy the webapp, click the deploy button in the [nbforms-server README](https://github.com/chrispyles/nbforms-server).

### Setup: Config File

nbforms requires a config file to set up the `Notebook` class. The default path that `Notebook` checks is `./nbforms_config.py`, although you can pass a custom path to the `Notebook` constructor. The structure of the config file is very specific; you must assign the variable `nbforms_config` to a dict containing the information that the notebook needs to create widgets and send requests. The structure of this file is:

```python
nbforms_config = {
		"server_url": "",        		  # URL to your Heroku app

		"notebook": "",  		 		  # an ID to collect responses

		"questions": [{					  # questions to ask, a list of dicts

			"identifier": "",   		  # a question identifer, should be unique within
										  # this notebook
			"type": "",					  # question type; can be one of:
										  # 	multiplechoice, checkbox, text, paragraph

			"question": "",				  # the question text

			"options": [				  # options from which to choose if type is 
				...						  # multiplechoice or checkbox
			],
			"placeholder": ""			  # placeholder for textbox if type is text or
										  # paragraph
		}, 
		...								  # more question dictionaries
	]
}
```

The `server_url` key should be the URL to your Heroku-deployed nbforms-server, e.g. `https://my-nbforms-server.herokuapp.com`. The `notebook` key should be some string or number to identify the notebook that you're deploying. This is used to keep the notebook responses distinguished on the server. Finally, the `questions` key should be a list of dictionaries that define the information for your questions.

Questions can have one of four types: `multiplechoice`, `checkbox`, `text`, or `paragraph`. The `type` key in the question is used to create the widget. If you have a `multiplechoice` or `checkbox`, you must provide a list of options as the `options` key. For `text` and `paragraph` responses, you can provide an optional `placeholder` key which will replace the default placeholder.

There is a sample config file at [`demo/nbforms_config.py`](demo/nbforms_config.py).

### In-Notebook: Import and Instantiate

To use the nbforms, you must first import it and create a `Notebook` instance. This will load the config file (defaulting to look at `./nbforms_config.py`) and ask the user to input a username and a password. If the username already exists on the server, the password will be checked and an API key will be generated, to be stored in the `Notebook` class. If it does not exist, a new user will be created, and an API key generated. If the user _does_ exist but an incorrect password is provided, the cell will error.

```python
import nbforms
form = nbforms.Notebook()
```

### In-Notebook: Collecting Responses

To collect the responses for a question, insert a cell that calls the `Notebook.ask` function on the **identifier** of the question. For example, if I had a question `q1`, I would call

```python
form.ask("q1")
```

This will output the widget and a "Submit" button that, when clicked, will send an HTTP POST request to your nbforms server with the student's username hash, notebook ID, question identifier, and response to be stored on the server.

### In-Notebook: Retrieving Data

nbforms allows you to get your data from the server and collect it into either a datascience `Table` or a pandas `DataFrame`. To retrieve the responses from the server, use `Notebook.to_table` or `Notebook.to_df`; the optional `user_hashes` argument (default `False`) indicates whether or not to include a column with the hashes username.

```python
# datascience Table
form.to_table("q1", "q2", ...)

# pandas DataFrame
form.to_df("q1", "q3", ..., user_hashes=True)
```

### Database Maintenance

There is not much database maintance that can be done, but you can optionally delete all responses on the server by running `rake clear` on your Heroku app.
