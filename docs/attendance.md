# Taking Attendance

nbforms can be used to track attendance. All attendance requests are logged and you have the ability to run commands that will open and close the attendance form. If a student submits when the attendance is not open, their submission will indicate that the form was closed when they submitted. If it is open, this will be reflected in their submission. If a student submits attendance for a notebook when it is open and then resubmits after it is closed again, the submission when the notebook was open will not be overwritten.

For instructions on opening and closing attendance for a notebook, see [here](./install_deploy).

To take attendance in the notebook, use `Form.take_attendance`:

```python
form.take_attendance()
```

nbforms does not notify students if they submit when the attendance form is closed. `Form.take_attendance` will only error if the submission was not recorded successfully (i.e. if the server responses with an error HTTP status).
