#!/bin/bash

version=$(hatch version)
if [[ "$version" =~ ^[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+$ ]] then
    echo 'pyaccord version:' $version 'is valid to release'
    exit 0
else
    echo 'pyaccord version:' $version 'is invalid to release, it is still development/release candidate'
    exit 1
fi
