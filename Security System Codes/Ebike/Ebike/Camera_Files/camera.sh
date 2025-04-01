#camera: keep taking pictures

libcamera-jpeg --output pic.jpg -t 1 -n --tuning-file /usr/share/libcamera/ipa/raspberrypi/imx219_noir.json 2> /dev/null

#libcamera-still --exposure sport -n --width 720 --height 480
