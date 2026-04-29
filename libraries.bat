@echo off
chcp 65001 > nul
title ASCII Fixer

echo [1/2]
python -m pip install --upgrade pip setuptools

echo [2/2] instrall OpenCV и MoviePy...
python -m pip install opencv-python moviepy
echo.
echo ready to start...
pause