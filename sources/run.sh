#!/bin/bash
g++ -shared -o compmath/bnMath.so -fPIC compmath/math.cpp -w 
./main.py

