## What is DecentralStream 

DecentralSteam is A new way to allow user to live stream using IPFS network instead of using server to send video

This give multiple advantages:
- It solve principal issue of live stream **bandwidth usage**: User can simply ask themself for moment of live and never ask for video on server
- Every moment of the stream is publicly store on IPFS that mean you can't censor anymore
- Anyone who want to save extract from live stream can simply pin this moment on IPFS:
  - Viewer can pay to store rediffusion not necessarily host or streamer
  - IPFS allow two people to save same moment without creating anycopy of the video (really usefull if lot a people create almost same clips)


# Requirement
 OBS (Open Broadcaster Software)
 
 MetaMask wallet for authentification

 User don't need to install anythings to access the steam




# Dependency
Python:
- Uvicorn===0.27.1
- Fastapi===0.109.2
- Aleph-sdk-python===0.9.0
- Python-multipart===0.0.9
- PyJWT===2.8.0
- asyncio===3.4.3
- logging===0.4.9.6
- pyrtmp===0.3.0
- aiohttp===3.9.3

  
