import React, { useRef, useEffect } from 'react';

const VideoStream = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch(err => {
          console.log("Error accessing camera:", err);
        }); 
    }
  }, []);

  return <video ref={videoRef} autoPlay={true} />;
};

export default VideoStream;
