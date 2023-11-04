# E-Bike Project Description
 I started this e-bike project many years ago. Starting with converting this bicycle to an e-bike, I have made many big changes to the powertrain and other systems throughout these years. The newest version is documented in this depository, including CAD files for the electric powertrain and python codes for the security system.

# Features
- 30 mph top speed, 0-30 time of approximately 3 seconds.
- Dual electric motors with peak power output of more than 5000W.
- 48V, 12Ah lithium-ion battery, 14S3P cell arrangement. 
- 15 miles of range at top speed. Range can be extended to around 40 miles with additional battery packs.
- Smart anti-theft system with vibration detection, GPS tracking, camera pointing at the lock, and email notifications.


# Electric Powertrain
- All CAD models were made in Fusion 360              
  <img width="500" alt="Screenshot 2023-11-04 at 10 42 51 AM" src="https://github.com/chc038/E-Bike/assets/146500723/e26f0fdd-e486-42e1-909c-cbe43739df03">

- FEA simulations using Ansys and Fusion 360 to assist with the design of the motor mount
  <img width="500" alt="Screenshot 2023-10-03 at 3 54 38 PM" src="https://github.com/chc038/E-Bike/assets/146500723/8b686a18-2987-49b2-8733-ca64ac6ce9a5">

- Plastic parts were 3D printed on my modified Ender-3 in PLA and Nylon; aluminum parte were machined on my DIY CNC mill
  <img width="300" alt="Screenshot 2023-11-04 at 10 50 42 AM" src="https://github.com/chc038/E-Bike/assets/146500723/7c255690-053b-46b1-87e3-5f7d77538c39">
  <img width="270" alt="Screenshot 2023-11-04 at 10 51 35 AM" src="https://github.com/chc038/E-Bike/assets/146500723/f89b02d8-25d2-4882-9aa0-3c9c91a85e04">

- Parts were designed to be bolted together. More pictures of the assembly below.
  
- Custom made lithium-ion battery pack by spot welding together 42 21700 cells in a 14S3P configuration.
  <img width="500" alt="Screenshot 2023-11-04 at 1 00 46 PM" src="https://github.com/chc038/E-Bike/assets/146500723/8d69001e-b928-4d19-a65b-23d824ecae6a">
  <img width="500" alt="Screenshot 2023-11-04 at 1 01 14 PM" src="https://github.com/chc038/E-Bike/assets/146500723/ed96f395-0efa-4981-b115-0a2af93e2d23">



# Security System
- System is based on a raspeberry pi computer with multiple sensors connected such as GPS module, IMU, ADC. All the programs that makes this system work are written in python. I made this system for theft prevension purpose.
  
- In lock mode, system automatically sends emails containing gps coordinates and picture when suspicious activities such as vibration or significant changes in GPS coordinates are detected.                  
  <img width="500" alt="Screenshot 2023-11-04 at 12 47 38 PM" src="https://github.com/chc038/E-Bike/assets/146500723/2e3aaa84-6ae5-48a0-96e9-6360fdff3f78">

- Remote control of things such as lights and viewing live camera feed through VNC remote desktop.
  <img width="500" alt="Screenshot 2023-11-04 at 12 04 45 PM" src="https://github.com/chc038/E-Bike/assets/146500723/5bdeea85-10ae-4aff-a52c-44554db957a2">

- 8" touchscreen showing a custon GUI serves as dashboard of the e-bike.
  <img width="500" alt="Screenshot 2023-11-04 at 12 49 17 PM" src="https://github.com/chc038/E-Bike/assets/146500723/8130974b-8ccf-45d8-a32b-0877d2d51e37">

- 3D printed custom housing for electrical components           
  <img width="500" alt="Screenshot 2023-11-04 at 11 09 10 AM" src="https://github.com/chc038/E-Bike/assets/146500723/e993a3ef-644c-4124-983b-b28216f6cfc7">


