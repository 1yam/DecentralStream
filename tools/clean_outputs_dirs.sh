#/bin/sh

# Clean the outputs and hls-outputs directories for rtmp dir
find ./rtmp/outputs/ -type f ! -name '.gitkeep' -exec rm -f {} +
find ./rtmp/hls-outputs/ -type f ! -name '.gitkeep' -exec rm -f {} +

# Clean the streams directories for api dir
find ./api/streams/ -type f ! -name '.gitkeep' -exec rm -f {} +
