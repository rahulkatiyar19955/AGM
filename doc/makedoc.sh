#!/bin/sh

cd ..
rm -rf html/*
make doc
cd doc
cp doc/tabs.css html/tabs.css
cp doc/AGGLEditor.png html/AGGLEditor.png
cp doc/AGGLEditor_A.png html/AGGLEditor_A.png

