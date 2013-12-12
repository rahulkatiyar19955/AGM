#!/bin/sh

rm -rf html/*
cd ..
make doc
cd doc
cp tabs.css html/tabs.css
cp AGGLEditor.png html/AGGLEditor.png
cp AGGLEditor_A.png html/AGGLEditor_A.png

