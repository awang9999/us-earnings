#!/bin/bash

# Copies the github repo website to the directory Apache2 reads.

cp index.html /var/www/html/index.html
cp about.html /var/www/html/about.html
cp signup.html /var/www/html/signup.html
cp -r css /var/www/html/css