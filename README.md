# LittleLearners

# Testing docker
Xauthority.  To run X server without disabling access control

Windows:

```
Open C:\Program Files\VcXrv\x0.hosts
Add your ip

Navigate to C:\Program Files\VcXrv\
Run .\xauth.exe add [YOURIP]:0 . 00000000000000000000000000000000
Navigate to C:\users\YOURUSERNAME
Copy .Xauthority to \littlelearners
```

Mac: (Not 100% sure about this)

```
run xhost [YOURIP]
run xauth add [YOURIP]:0 . 00000000000000000000000000000000
Navigate to your home\user directory
Copy .Xauthority to \littlelearners
```

Stop typing Display variable:

```
create file called 'display' in \littlelearners
Write 'export DISPLAY=[YOURIP]' in that file
```

The shell script should now use that display variable for X without you needing to type it in the docker run command


Docker options I use:

`--rm`  Automatically runs `docker rm <container_name>` Once the container finishes execution
`--name <container_name>`  Set the name for the container.  This is technically not necessary if you use --rm as the container is automatically deleted
`-it`  This is a combintiaotn of `interactive` and `terminal`.  So you access to standard in and standard out in the console
`--env` Set environment variables.  Typically only the display variable to foward X info for the GUI and mysql host password
`--link <name>` Allows the container to get the docker IP address of another container with the name provided
`-v` Maps a volume from your local file system to the internal container file system.  This will save data from the container outside of the container so it will persist once the container is removed.
`-p` Maps the docker port to the host port.  I can't exactly remember about this one, I think I map the mysql port so it can be accessed outside docker by using local host and the mysql docker port number
`-d` Detached mode.  Runs the container in the background


Build littleleaners - cd to littlelearners directory.  image_name can be whatever you like
`docker build -t <image_name> .`

Run desktopApp.  Conatiner name can be whatever you like, image name is the name you used to build.
`docker run --name <container name> --env DISPLAY=[IP]:0.0 -it <image_name> [child] [parent] [local] [pytest] [db] [init] [y] [root]`

Add `parent` to run the app starting with the parent login. (This is default, so no parameters will run this)
Add `child` to run the app starting with the child login.

I took the `--rm` off the run command above so we can run the container twice and have the container data persist.
After the container is run once, start it again with `docker start <container name>`
Both child and parent will log in automatically after the first run
Might want to put `--rm` back on if you are making a lot of changes so you don't have to manually remove the container each time.

Add `local` to connect to local database
Add `pytest [tests]` to run pytest
Add `db` to run database.py
Add `init` to run database/init.py
Add `y` to tell init to reset the database tables with what is in dbTestInit.py
Add `root` in conjunction with `init` and `y` to reset the VM database 

Run tests (Broken at the moment)
`docker run --rm --name lltest -it --link mysql littlelearners pytest`

X Server - https://sourceforge.net/projects/vcxsrv/
Need this to run GUI applications in docker on Windows.  Check disable access control when running it.

MySql container - If you want to run database locally
`docker run -d -v data:/var/lib/mysql -p 3306:3306 --name mysql --env MYSQL_ROOT_PASSWORD=1234 mysql`

To run littlelearners docker container and connect to local mysql change run 
`docker run --rm --name <container_name> --env DISPLAY=[IP]:0.0 -it --link mysql <image_name> local

To run mysql in the container
`docker exec -it mysql mysql -uroot -p1234`

The database schema is in database/dbTestInit.py

To initialize a local database and create/recreate the tables
`docker run --rm --link mysql <image_name> local init y`

To just initalize the data locally
`docker run --rm --link mysql <image_name> local init`

To initialize the VM database and create/recreate the tables
`docker run --rm <image_name> init y root`

To just initalize the VM data
`docker run --rm <image_name> init`