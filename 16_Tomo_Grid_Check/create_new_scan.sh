#!/bin/bash
folder_in=00_Master
folder_out=00

cp -r ${folder_in} ${folder_out}_00
cp -r ${folder_in} ${folder_out}_01
cp -r ${folder_in} ${folder_out}_02
cp -r ${folder_in} ${folder_out}_10
cp -r ${folder_in} ${folder_out}_11
cp -r ${folder_in} ${folder_out}_12

folder_out=01

cp -r ${folder_in} ${folder_out}_00
cp -r ${folder_in} ${folder_out}_01
cp -r ${folder_in} ${folder_out}_02
cp -r ${folder_in} ${folder_out}_10
cp -r ${folder_in} ${folder_out}_11
cp -r ${folder_in} ${folder_out}_12
