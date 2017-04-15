#!/usr/bin/env bash
coverage run --source=app/gratitude,app/prayer -m unittest
coverage report -m