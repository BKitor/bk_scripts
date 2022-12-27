#!/usr/bin/bash


if [ -e "$HOME/.profile" ]; then 
	OUT_FILE="$HOME/.profile"
elif [ -e "$HOME/.bash_profile" ]; then
	OUT_FILE="$HOME/.bash_profile"
else
	OUT_FILE="$HOME/.bashrc"
fi	

echo "PATH=\"$PWD/bin:\$PATH" >> $OUT_FILE

mkdir ~/.chk_bak
