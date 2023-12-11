#!/bin/sh

coverage run -m pytest
coverage report
coverage html
