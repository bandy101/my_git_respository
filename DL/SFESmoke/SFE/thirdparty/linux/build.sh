#!/usr/bin/env bash

mkdir Thplateid/build
cd Thplateid/build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j8

cd ../..

mkdir VideoStream/build
cd VideoStream/build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j8

cd ../..

mkdir Esegment/build
cd Esegment/build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j8