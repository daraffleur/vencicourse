#!/bin/bash
echo Run db upgrade
flask db upgrade
echo Run app
flask run -h 0.0.0.0 --port=5000
