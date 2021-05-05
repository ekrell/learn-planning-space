# This script removes any outputs from path-planning runs that failed
# (Possibly no valid solution?)

RESULTS=( $(ls data | grep res | sed -e 's/res_//' -e 's/.txt//') )

for i in "${RESULTS[@]}"
do
    # If failed to produce path file, remove output file
    if [ ! -f data/path_$i"".txt  ]; then
        rm data/res_$i.txt
    fi
done

ls data | grep path
