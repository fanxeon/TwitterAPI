# TwitterAPI
For cloud and cluster computing


#Added three harvesting instances

--------------------------------------------------------------------------------
#Upstart jobs created on Ubuntu vm that will make sure these instances are always up and running.
ex. /etc/init/twitter1.conf

cat /etc/init/twitter1.conf
start on runlevel [2345]
stop on runlevel [016]

respawn
exec python3 /home/ubuntu/TwitterAPI/tweetsmining.py
--------------------------------------------------------------------------------
