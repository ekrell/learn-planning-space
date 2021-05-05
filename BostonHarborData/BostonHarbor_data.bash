# Generate data for Boston Harbor learning experiment
# Use the `conch` path planning package to solve paths on the raster
# Conch: https://github.com/ekrell/conch

CONCH_PATH=/projects/conch/
REGION_RASTER=data/full_shrink.tif
NPOINTS=100000

# Determine raster size (pixels)
COLS=$(gdalinfo $REGION_RASTER | grep "Size is" | grep -o -e '[0-9]*' | head -n 1)
ROWS=$(gdalinfo $REGION_RASTER | grep "Size is" | grep -o -e '[0-9]*' | head -n 2 | tail -n 1)

# Init arrays to store init and goal points
declare -a POINTS_INIT_X=()
declare -a POINTS_INIT_Y=()
declare -a POINTS_GOAL_X=()
declare -a POINTS_GOAL_Y=()

# Generate points
for i in $(seq 0 $NPOINTS); do
    RAND_INIT_X=$((1 + $RANDOM % $(($COLS-1))))
    RAND_INIT_Y=$((1 + $RANDOM % $(($ROWS-1))))
    RAND_GOAL_X=$((1 + $RANDOM % $(($COLS-1))))
    RAND_GOAL_Y=$((1 + $RANDOM % $(($ROWS-1))))
    VALUE_INIT=$(gdallocationinfo $REGION_RASTER $RAND_INIT_X $RAND_INIT_Y | tail -n 1 | awk -F ': ' '{print $2}')
    VALUE_GOAL=$(gdallocationinfo $REGION_RASTER $RAND_GOAL_X $RAND_GOAL_Y | tail -n 1 | awk -F ': ' '{print $2}')

    # Ensure a free cell
    if [ $VALUE_INIT == 0 ] && [ $VALUE_GOAL == 0 ]; then
        POINTS_INIT_X+=($RAND_INIT_X)
        POINTS_INIT_Y+=($RAND_INIT_Y)
        POINTS_GOAL_X+=($RAND_GOAL_X)
        POINTS_GOAL_Y+=($RAND_GOAL_Y)
    fi
done

NVALID=${#POINTS_INIT_X[@]}
echo "Generated $NVALID valid points"
for i in $(seq 0 $(($NVALID-1))); do
    echo Planning $i / $NVALID ...
    # Convert (row, col) to (lat, lon)
    INIT_LAT=$(python3 $CONCH_PATH""/tools/rowcol2latlon.py -g $REGION_RASTER -c ${POINTS_INIT_X[$i]} -r ${POINTS_INIT_Y[$i]} | \
        awk -F ": " '{print $3}' | sed -e 's/(//' -e 's/)//' | awk -F ", " '{print $1}')
    INIT_LON=$(python3 $CONCH_PATH""/tools/rowcol2latlon.py -g $REGION_RASTER -c ${POINTS_INIT_X[$i]} -r ${POINTS_INIT_Y[$i]} | \
        awk -F ": " '{print $3}' | sed -e 's/(//' -e 's/)//' | awk -F ", " '{print $2}')
    GOAL_LAT=$(python3 $CONCH_PATH""/tools/rowcol2latlon.py -g $REGION_RASTER -c ${POINTS_GOAL_X[$i]} -r ${POINTS_GOAL_Y[$i]} | \
        awk -F ": " '{print $3}' | sed -e 's/(//' -e 's/)//' | awk -F ", " '{print $1}')
    GOAL_LON=$(python3 $CONCH_PATH""/tools/rowcol2latlon.py -g $REGION_RASTER -c ${POINTS_GOAL_X[$i]} -r ${POINTS_GOAL_Y[$i]} | \
        awk -F ": " '{print $3}' | sed -e 's/(//' -e 's/)//' | awk -F ", " '{print $2}')

    # Solve path
    python3 $CONCH_PATH""/planners/rasterplanner.py -r $REGION_RASTER -n 16 \
        --sx $INIT_LON --sy $INIT_LAT --dx $GOAL_LON --dy $GOAL_LAT \
        -p data/path_$i"".txt -m data/plot_$i"".png > data/res_$i"".txt

    # If fail, delete
    if [ ! -f data/path_$i"".txt ]; then
        rm data/res_$i"".txt
    fi



done

