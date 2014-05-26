#!/bin/sh

rm -rf html/*
cd ..
export ROBOCOMP_SUPPORT=1
make doc ROBOCOMP_SUPPORT=1
cd -
cp tabs.css html/tabs.css
cp AGGLEditor.png html/AGGLEditor.png
cp AGGLEditor_A.png html/AGGLEditor_A.png

