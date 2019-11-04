# Web Proxy Server
## Ryan Shu | 916850524

## Project description
Implement a client/server web proxy that will allow a certain company to privately browse websites that the users may not have access to. This involves multiple user types (Admin/Manager/None) which each have different access rights listed below. For the web server to proxy server connection we will be using sockets in order to create a new thread each time a new web server client connects to the proxy server.

 1. Admin
    - Access to every site
    - Access to private mode
    - Delete cache
    - Add Admins/managers
    - Add blockedsites
    - Add admin only sites
2. Managers
    - Access to all sites except admin only sites
    - Access to Private Mode
3. Not logged in
    - Access to sites except Blocked and admin only sites
    - No private mode access

## Project purpose
The goal of this assignment is to implement a working proxy server for use by a company using a server/client system.

## Dependencies
Python 3.6.8
## Instructions to Clone/Execute
 1. Clone this repo
  ```
  git clone https://github.com/sfsu-joseo/csc645-01-fall2019-projects-ryanshuzzz.git
  ```
 2. Navigate to project folder
  ```
  cd 645-01-fall2019-projects-ryanshuzzz/applications/web-server-proxy/
  ```
 3. Run Web Server
  ```
  python3 webserver.py
  ```
 4. Run Proxy Server
  ```
  python3 proxyserver/proxyserver.py
  ```
 5. Navigate to localhost:5000 to begin using the proxy
-   Default admin credentials username: admin password: pass
-   Default manager credentials username: man password: pass
 
## Compatibility issues 
This project was compiled and executed using Python 3.6.8 on Ubuntu 18.1 with BASH 4.4.19. There may be issues compiling and executing on a windows system.

## Challenges
Some challenges that I have ran into during this assignment was largely due to sending large amounts of data from the proxy server to the web server client. This was overcome by using a buffer and looping until the received packets were less than the buffer size. 
Another issue that I ran into during implementation was how to authenticate the users when they logged in, and also when admins logged in to get all of the admins information. To overcome this I created a dictionary template where it would send the user information to the server and the server would return whether the user was validated or not. 
Caching was also an issue that I had. I had issues attempting to jsonify the reqest data, and ended up using pickle to store it into files.
The final issue I had was losing scope of the proxy data (proxy_admins, blocked_sites, ..). Everytime I would attempt to use "get" functions in the proxymanager, it would not return the list of data, and would return '<'bound method at (mem address)'>'. After a while I just accessed the lists in the proxythread. 
