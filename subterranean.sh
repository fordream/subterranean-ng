#!/bin/bash
python main.py $1

rm *.pyc
rm ./Libraries/*.pyc
rm ./Assets/Scenes/*.pyc
rm ./Assets/Characters/*.pyc
rm ./Assets/Items/*.pyc
rm ./Assets/Elements/*.pyc