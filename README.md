# Syracuse University Summer College cybersecurity webapp

[Check out the course here!](http://summercollege.syr.edu/cybersecurity-hack-a-thon-challenge/)

This is a simple webapp for an SU course I attended.
The webapp is intended to check for open ports over a given range of IPs, then update a scoreboard based on which ports are open.
The intention was to keep score for the course's hackathon.
While teams attempt to start and maintain different services, (FTP, HTTP, etc.) a group of hackers tries to bring those services down.

* **NOTES:**
	+ Requires Flask
    + Python 3 only
    + ips.txt should contain the IPs you would like to check
    + database_manager.py must be run before main.py
    + Sending a SIGBREAK is the best way to stop the execution of main.py
