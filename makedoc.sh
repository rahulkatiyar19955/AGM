#!/bin/sh

rm -rf doc/html/*
make doc
cp doc/tabs.css doc/html/tabs.css
cp doc/AGGLEditor.png doc/html/AGGLEditor.png
cp doc/AGGLEditor_A.png doc/html/AGGLEditor_A.png

