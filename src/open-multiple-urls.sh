#!/bin/bash

urls=($1)

for url in ${urls[@]}
do
    /usr/bin/open "$url"
done
