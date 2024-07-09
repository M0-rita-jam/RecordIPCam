# RecordIPCam
## Usage
1. Camera Configuration
Edit the IPCAM_USER.json file to configure your IP cameras.  
An example configuration for one camera is provided.  
You can configure multiple cameras by separating them with " , ".   
[Note] that a thread will be generated for each camera.  
``` json
{
  "cams":[
        {
            "cam_name":"your camera name",
            "user_id":"rtsp id",
            "user_pw":"rtsp password",
            "host_ip":"rtsp ip addr"
        }
    ]
}
```
2. Start the Script
Run the Python script with the following command:
``` bash
$ python3 RecordIPCam.py
```

## Note
During operation, you may encounter the following error.  
This occurs when the IP camera fails to retrieve frames. Currently, there is no easy workaround for this issue. Please be aware of this limitation.
``` bash
error while decoding MB xxx xxx, bytestream xxx
```