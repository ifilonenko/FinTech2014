I will not be including app documentation (currently for pearPoll) here just yet. I/we will implement this packaging later with python setuptools. 

We will also need to add a manifest with license and additional documentation before packaging.

I am adding this directory to the pearProject repository only to see if I am able to update it, and other developers are able to push/pull properly from the repo. 

Seed directory includes:

- Polls app configures tests, urlConfs, and views for admin generated questions and choices (this should be a standalone directory within /seed from which the associated .html views are modified.) 
    - index, detail, and results views are available within the templates director in /seed/polls
    
- To modify the admin contents that generate the Django hosted admin site, you will likely need both admin.py files in /seed and in seed/polls
    - Most functionality type changes will occur in file types: models.py, views.py, urls.py and the majority of files found in the "templatesl" 
      directories
    - For folders named "templates" and "static," Django identifies the contents of each recursively, so please maintain that file structure otherwise 
      views.py will not work properly
      
- All of these instructions are for the very simple polls app developed as a starting point. Of course this will get more hairy when we think about 
  how to design the front end more completely
  
- Important note: pearProject is running on a mySQL database hosted locally on my computer. To get this running you will need to use the database connector
  (from Django in python to mySQL) called mysqlDB. I don't know how this works on Mac/Windows, but on Linux (especially if you have a different Python 
  distribution that didn't come native to your Linux package) I highly recommend using a virtual environment that loads Python 2.7 automatically. 
  If this is possible in windows/mac please opt for this route. 
  
- We need to talk about how all of you can gain access to mySQL database, I know how to add users and configure the settings for remote access, but 
  this is not being hosted on github and as such is limited to my computer being on/running (this will not be our solution). Same goes for the admin 
  site. I have added all of you as staff users to the admin site with username: firstnamefirstletteroflastname password: same as username. I think a 
  good option might be for all of us to get Django and mySQL (with needed database binding), working locally and then use Github (with forks) for version 
  control. We should talk about whether this is good strategy or not. 
  
- Let's get going, we got this. 
