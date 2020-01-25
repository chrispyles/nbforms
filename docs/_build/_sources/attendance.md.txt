# Taking Attendance

nbforms can be used to track attendance. All attendance requests are logged and instructors have the ability to run rake tasks that will open and close the attendance form. If a student submits when the attendance is not open, their submission will indicate that the form was closed when they submitted. If it is open, this will be reflected in their submission. If a student submits attendance for a notebook when it is open and then resubmits after it is closed again, the submission when the notebook was open will not be overwritten.

To open the attendance submissions, run `rake attendance:open[NB_ID]` on the heroku add. Simiarly, to close it, run `rake attendance:close[NB_ID]`. To generate a CSV of the submissions for a particular notebook, run `rake attendance:report[NB_ID]`. In all of these, replace `NB_ID` with the identifier you provided for the notebook in the config file.

To take attendance in the notebook, use `Notebook.take_attendance`:

```python
form.take_attendance()
```

The default behavior of nbforms is not to notify students if they submit when the form is closed. `Notebook.take_attendance` will only error if the submission was not recorded successfully.
