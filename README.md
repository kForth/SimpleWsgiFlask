## Simple Wsgi Flask

This is just a simple example of how to setup a flask server with apache and wsgi. I have compiled mod_wsgi for python 3.5.2 and will implement my DeployServer to update the site automatically.

### Setup

This probably isn't going to be comprehensive and even comprehensible, but these are the basic steps I took to setup my servers.

First, test what python you have setup
```
	python -V
```
Notice the V is capitalized, a lowercoase v is something else.

If your output looks like this:
```
	Python 3.5.2
```
or some other 
```
	Python 3.x.y
``` 
version, you're good to go and can skip ahead a bit.

If it shows up as 
```
	Python 2.x.y
```
you'll need to replace youre regular python with python3.

Here are the basic commands, this will get rid of the old python and pip commands and replace them with the python3 versions.
```
	sudo rm /usr/bin/python
	sudo rm /usr/bin/pip
	sudo ln -s /usr/bin/python3 /usr/bin/python
	sudo ln -s /usr/bin/pip3 /usr/bin/pip
```

This is where the python3 people come back.
We're going to install apache2 now, you might already have this.
```
	sudo apt-get update && sudo apt-get upgrade
	sudo apt-get install apache2 apache2-doc apache2-utils
```
You might want to add 
```
	KeepAlive Off
```
to your /etc/apache2/apache2.conf if you want to save memory. If you do edit it, restart apache with this command:
```
	sudo service apache2 restart
```

Now let's install mod-wsgi for apache, make sure you use the -py3 suffix to compile with python3.
```
	sudo apt-get install libapache2-mod-wsgi-py3 python-dev
	pip install mod_wsgi
```
Enable mod_wsgi with the following command
```
	sudo a2enmod wsgi
```

Now you need to add mod_wsgi's config to apache's config. Run this command and copy the output.
```
	mod_wsgi-express module-config
```

Now paste it in your apache config
```
	sudo nano /etc/apache2/apache2.conf
```

Now you need to setup your server. Start by making your server folder, I'm going to call it Server and put it in /var/www/ but you should call it something better.
```
	mkdir /var/www/Server
	cd /var/www/Server
```

Then clone this repo in, or just copy the files you need.
```
	git clone https://github.com/kforth/SimpleWsgiFlask.git
	cd SimpleWsgiFlask
```

You should rename all of these files now so that they're meaningful. Here's an example of how to rename server.wsgi and server.conf.
```
	cp server.wsgi example_server.wsgi
	cp server.conf example_server.conf
```
You'd replace 'example_server' with whatever you want.
If you rename server.wsgi, make sure to update line 3 of server.conf and for your config later on.
If you rename server.conf, make sure to remember that for future commands.

Next we need to move the conf file to the apache folder. Make sure to change the filename if you renamed it.
```
	sudo mv server.conf /etc/apache2/sites-available/
```

To enable the site run this command, make sure to replace 'server' with the name of the conf file we just moved.
```
	sudo a2ensite server
```

Finally just restart apache and this server should be running.
```
	sudo service apache2 restart
```



I mostly got my setup information from [this](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps) Digial Ocean tutorial and a bit from [this](https://www.linode.com/docs/web-servers/apache/apache-web-server-on-ubuntu-14-04) Linode guide.