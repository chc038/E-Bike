# E-Bike Project Description
 I started this e-bike project many years ago. Starting with converting this bicycle to an e-bike, I have made many big changes to the powertrain and other systems throughout the years. The newest version is documented in this depository, including CAD files for the electric powertrain and python codes for the security system.                    
 <img width="500" alt="Screenshot 2023-11-04 at 5 46 38 PM" src="https://github.com/chc038/E-Bike/assets/146500723/c9ce0569-adf2-4f7a-9de5-bf45d7e73fc9">




# Features
- 30 mph top speed, 0-30 time of approximately 3 seconds.
- Dual electric motors with peak power output of more than 5000W.
- Custom made 48V, 12Ah lithium-ion battery pack. 
- 15 miles of range at top speed. Range can be extended to around 40 miles with additional battery packs.
- Smart anti-theft system with vibration detection, GPS tracking, camera pointing at the lock, and email notifications.


# Electric Powertrain
- All CAD models were made in Fusion 360              
  <img width="500" alt="Screenshot 2023-11-04 at 10 42 51 AM" src="https://github.com/chc038/E-Bike/assets/146500723/494649b3-90b0-4281-988f-ff030b1dea6b">\

- FEA simulations using Ansys and Fusion 360 to assist with the design of the motor mount
  <img width="500" alt="Screenshot 2023-10-03 at 3 54 38 PM" src="https://github.com/chc038/E-Bike/assets/146500723/54a93b7c-6a0e-4a5b-b0a0-0592d6931f8e">

- Plastic parts were 3D printed on my modified Ender-3 in PLA and Nylon; aluminum parte were machined on my DIY CNC mill
  <img width="350" alt="Screenshot 2023-11-04 at 6 11 58 PM" src="https://github.com/chc038/E-Bike/assets/146500723/2a54462b-1fb1-4c8a-93b5-2682f4c1a1b3">
  <img width="433" alt="Screenshot 2023-11-04 at 6 11 41 PM" src="https://github.com/chc038/E-Bike/assets/146500723/768787d0-ab18-4316-90c1-7aaf55beaaae">
  
- Custom made lithium-ion battery pack by spot welding together 42 21700 cells in a 14S3P configuration.
  <img width="500" alt="Screenshot 2023-11-04 at 6 14 55 PM" src="https://github.com/chc038/E-Bike/assets/146500723/b7e855f1-4201-4519-81a3-1e68df08a4a2">

- More pictures of the electric powertrain below.                   
  <img width="500" alt="Screenshot 2023-11-04 at 5 30 08 PM" src="https://github.com/chc038/E-Bike/assets/146500723/680c208d-1d2d-4b31-8d12-51081b808b94">
                                                   
  <img width="240" alt="Screenshot 2023-11-04 at 5 30 36 PM" src="https://github.com/chc038/E-Bike/assets/146500723/4a39eb37-b202-4b2d-9359-3a15555519a0">
  <img width="260" alt="Screenshot 2023-11-04 at 5 31 03 PM" src="https://github.com/chc038/E-Bike/assets/146500723/5bc778e5-5d76-4545-9186-9d3da128d138">






# Security System
- System is based on a raspeberry pi computer with multiple sensors connected such as GPS module, IMU, ADC. All the programs that makes this system work are written in python. I made this system for theft prevension purposes.
  
- In lock mode, system automatically sends emails containing gps coordinates and picture when suspicious activities such as vibration or significant changes in GPS coordinates are detected.                  
  <img width="350" alt="Screenshot 2023-11-04 at 6 21 10 PM" src="https://github.com/chc038/E-Bike/assets/146500723/647c9174-856f-4f27-9bd9-b462b14fa3d4">

- Remote control of things such as lights and viewing live camera feed through VNC remote desktop.
  <img width="500" alt="Screenshot 2023-11-04 at 6 22 55 PM" src="https://github.com/chc038/E-Bike/assets/146500723/2c16cf52-e460-4481-a4e6-7108d24fc3dc">

- 7" touchscreen showing a custon GUI serves as dashboard of the e-bike.
  <img width="500" alt="Screenshot 2023-11-04 at 6 24 04 PM" src="https://github.com/chc038/E-Bike/assets/146500723/52a2c5a4-00b1-4148-9939-b0fe712caa43">

- 3D printed custom housing for electrical components           
  <img width="500" alt="Screenshot 2023-11-04 at 6 25 08 PM" src="https://github.com/chc038/E-Bike/assets/146500723/b3ae7305-1763-42b2-8c32-c9f2d7d520d3">



