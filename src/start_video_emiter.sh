#cvlc -vvv v4l2:///dev/video0 --sout '#transcode{vcodec=mp1v,vb=800,acodec=mpga,mux=mpeg1}:rtp{sdp=rtsp://:8554/}'

#cvlc v4l2:///dev/video0 :v4l2-standard= :v4l2-width=320 :v4l2-height=200 :live-caching=0 :v4l2-fps=25 :v4l2-audio-mute --sout '#transcode{deinterlace,vcodec=mpgv}:standard{access=http,mux=ts,mime=video/ts,dst=:8099}'

#cvlc v4l2:///dev/video0 :chroma=h264 :v4l2-width=320 :v4l2-height=200 :live-caching=0 :v4l2-fps=25 :v4l2-audio-mute --sout '#standard{access=http,mux=ts,mime=video/ts,dst=:8099}' :demux=h264

# :v4l2-standard=

# :chroma=h264

# :input-slave=alsa://hw:1,0 
#     :v4l2-width=320 :v4l2-height=200 :live-caching=0 :v4l2-fps=25 :v4l2-audio-mute \

# vcodec=mp2v

cvlc v4l2:///dev/video0 \
    :chroma=MJPG :v4l2-caching=0 :v4l2-width=320 :v4l2-height=240 :live-caching=0 :v4l2-fps=25 :v4l2-audio-mute \
    --sout 'standard{access=http,mux=ts,mime=video/ts,dst=:8099}'
    
    # #transcode{vcodec=mpgv,vb=128,acodec=none}:
    #--sout '#transcode{vcodec=mpgv,vb=800,acodec=none}:rtp{sdp=rtsp://:8554/}'
#:v4l2-width=320 :v4l2-height=240 :live-caching=0 :v4l2-fps=25 
#cvlc v4l2:///dev/video0 \
#    :v4l2-width=320 :v4l2-height=200 :live-caching=0 :v4l2-fps=25 :v4l2-audio-mute \
#    --live-caching=10 \
#    --sout '#transcode{vcodec=mp2v,vb=256,acodec=ne}:std{access=udp{caching=10},mux=ts,#dst=localhost:1234}'