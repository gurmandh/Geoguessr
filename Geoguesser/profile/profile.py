from flask import (
    Blueprint, 
    render_template, 
    url_for, 
    redirect,
    request,
    flash,
    abort
)
from .. import db
from .forms import UpdateUserForm