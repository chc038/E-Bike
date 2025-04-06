# E-Bike Project Description
 This e-bike project was started many years ago. Starting with converting this bicycle to an e-bike, I have made many changes to the powertrain and other systems throughout the years. This depository includs CAD files for the electric powertrain and python codes for the security system.                    
 <img width="500" src="Fig/full_side_view.jpeg" alt="Full Size View">




# Features
- 35 mph top speed
- Accelerates from 0 to 30mph in 3.2 seconds. (Measured with the same GPS module, my car did 0-30 in 3.7 seconds) 
- Dual electric motors with peak power output of 6000W.
- Custom made 48V, 12Ah lithium-ion battery pack. 
- 15 miles of range at top speed. Range can be extended to around 40 miles with additional battery packs.
- Smart anti-theft system with vibration detection, GPS tracking, camera pointing at the lock, and email notifications.


# Electric Powertrain
- All CAD models were made in Fusion 360              
  <img width="500" src="Fig/powertrain_cad.png" alt="Powertrain CAD">

- FEA simulations using Ansys and Fusion 360 to assist with the design of the motor mount
  <img width="500" alt="Powertrain FEA" src="https://github.com/chc038/E-Bike/assets/146500723/54a93b7c-6a0e-4a5b-b0a0-0592d6931f8e">

- Plastic parts were 3D printed in PLA and Nylon; aluminum parte were machined on my CNC machine
  <img width="500" alt="Machining" src="https://github.com/chc038/E-Bike/assets/146500723/bd45c499-08dc-4cfe-80fe-32a6447f7c04">
  
- Custom made lithium-ion battery pack by spot welding together 42 21700 cells in a 14S3P configuration.
  <img width="500" alt="Battery Pack" src="https://github.com/chc038/E-Bike/assets/146500723/b7e855f1-4201-4519-81a3-1e68df08a4a2">

- More pictures of the electric powertrain below.                   
  <img width="500" alt="Powertrain Picture (Top)" src="Fig/powertrain_pic_top.jpeg">
                                                   
  <img width="250" alt="Powertrain Picture (Right Side)" src="Fig/powertrain_pic_side.jpeg">

  <img width="250" alt="Powertrain Picture (Left Side)" src="Fig/powertrain_other_side.jpeg">






# Security System
- System is based on a raspeberry pi computer with multiple sensors connected such as GPS module, IMU, ADC. All the programs that makes this system work are written in python. This system was made for theft prevension purposes.
  
- In lock mode, system automatically sends emails containing gps coordinates and picture when suspicious activities such as vibration or significant changes in GPS coordinates are detected.                  
  <img width="350" alt="Aleart Email" src="https://github.com/chc038/E-Bike/assets/146500723/647c9174-856f-4f27-9bd9-b462b14fa3d4">

- Remote control of things such as lights and viewing live camera feed through VNC remote desktop.
  <img width="500" alt="Remote Controls" src="https://github.com/chc038/E-Bike/assets/146500723/2c16cf52-e460-4481-a4e6-7108d24fc3dc">

- 7" touchscreen showing a custon GUI serves as dashboard of the e-bike.
  <img width="500" alt="Dashboard" src="https://github.com/chc038/E-Bike/assets/146500723/52a2c5a4-00b1-4148-9939-b0fe712caa43">

- 3D printed custom housing for electrical components           
  <img width="500" alt="Electronics Box CAD" src="Fig/elec_box_cad.png">
  
  <img width="500" alt="Battery Box CAD" src="Fig/batt_box_cad.png">



