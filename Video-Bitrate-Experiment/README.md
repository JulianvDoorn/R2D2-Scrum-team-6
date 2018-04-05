cli.py usage with config file:

./cli.py encode --conf videos.conf -o videos/

cly.py usage with individual files:

./cli.py encode -i videos/tractor_1080p25.y4m -o videos/tractor.mp4 -c x265 -r 1920x1080 --bitrate 7000 -s 00:00:00 -t 00:00:10
