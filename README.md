## Simple Wsgi Flask

This is just a simple example of how to setup a flask server with apache and wsgi. I have compiled mod_wsgi for python 3.5.2 and will implement my DeployServer to update the site automatically.

### Setup

This probably isn't going to be comprehensive and even comprehensible, but these are the basic steps I took to setup my servers.

First, test what python you have setup
```
	python -V
```
Notice the V is capitalized, a lowercoase v is something else.

If your output looks like `Python 3.5.2` then it's the same as me and this should work better, you can skip to the next section

If it's some other `Python 3.x.y` version, you're probabably also good and can also skip to the next section. `Python 3.6.x` might not actually work tho.

If it shows up as some kind of `Python 2.x.y` you'll need to replace your regular python and pip commands with their python3 counterparts.

Here are the basic commands, this will get rid of the old python and pip commands and replace them with the python3 versions.
```
	sudo rm /usr/bin/python
	sudo rm /usr/bin/pip
	sudo ln -s /usr/bin/python3 /usr/bin/python
	sudo ln -s /usr/bin/pip3 /usr/bin/pip
```


---

This is where the python3 people come back.
We're going to install apache2 now, you might already have this.
```
	sudo apt-get update && sudo apt-get upgrade
	sudo apt-get install apache2 apache2-doc apache2-utils apache2-dev
```
You might want to add `KeepAlive Off` to your /etc/apache2/apache2.conf if you want to save memory. If you do edit it, restart apache with `sudo service apache2 restart`.

Next we'll install mod-wsgi for apache, make sure you use the '-py3' suffix.
```
	sudo apt-get install libapache2-mod-wsgi-py3 python3-dev
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

Paste the output in your apache config
```
	sudo nano /etc/apache2/apache2.conf
```

---

Now you need to setup your server. Start by making your server folder, I'm going to call it Server and put it in /var/www/ but you should call it something better.
```
	mkdir /var/www/Server
	cd /var/www/Server
```

If you do change the name of this folder, make sure to make it match line 2 and 7 in your conf file and line 6 of your wsgi file.

Then clone this repo in, or just copy the files you need.
```
	git clone https://github.com/kforth/SimpleWsgiFlask.git
	cd SimpleWsgiFlask
```

---

You don't need to do this but I'm going to setup this server as a [DeployServer](https://github.com/kforth/DeployServer). This command will replace this repo's server.py with the DeployServer.
```
	wget https://raw.githubusercontent.com/kForth/DeployServer/master/server.py server.py
```

If you want to do this you'll also need to setup a config.json, so create and open the file
```	
	nano config.json
```

and paste this in, changing filenames where needed.
```json
	"server_name_here": {
	    "github-secret":  "YouShouldUseASecretSinceTheFeatureIsHere",
	    "folder-path":    "/var/www/Server",
	    "save-packets":   true,
	    "command":        ["git pull", "touch server.wsgi"]
  	}
```
The commands I chose were `git pull` and `touch server.wsgi`. These commands run in the folder you specify with whatever use you set on line 6 of your server.conf file. 

`git pull` will obviously just pull any newly pushed data, it will fail if you have any uncommited changes. I'm sure you could have some powerful and/or dangerous commands here so be careful. 

`touch server.wsgi` will cause an update to your wsgi file, since the wsgi daemon we set up monitors this file for changes. Updating will cause the server to reload and start using the newly pushed data.


Finally, You'll need to then setup a webhook on github for your repo with these settings
```
	Payload URL: http://example.com:5050/update_server_name_here
	Content Type: application/json
	Secret: YouShouldUseASecretSinceTheFeatureIsHere
	Which events would you like to trigger this webhook? Just the push Event
```
Make sure to change the port to match line 1 in your conf and change 'server_name_here' to match line 1 of your config.json.

---

You should rename all of these files now so that they're meaningful. Here's an example of how to rename server.wsgi, server.conf, and server.py.
```
	mv server.wsgi example_server.wsgi
	mv server.conf example_server.conf
	mv server.py example_server.py
```
You'd replace 'example_server' with whatever you want.

If you rename server.wsgi, make sure to update line 3 of server.conf and line 5 of your config.json if you setup a DeployServer.

If you rename server.conf, make sure to remember that for the next 2 commands.

If you rename server.py, make sure to update line 8 of your server.wsgi.

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
