#!bin/bash
names_array=("Alex", "Egor", "Igor")
while true; do
    for element in "${names_array[@]}"; do
        echo "$element"
    done
done