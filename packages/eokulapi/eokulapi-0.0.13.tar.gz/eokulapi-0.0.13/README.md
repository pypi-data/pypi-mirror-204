# eokulapi
eokul vbs api wrapper for python

## install
`pip install eokulapi` or `poetry add eokulapi`

## usage
```python
from eokulapi import EokulAPI

user=EokulAPI(uid=...)
st=user.students[0]
user.update_student_data(st)
...
```