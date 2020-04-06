How to set up github for file and script backing up and version control
Minna Ho, Feb 2020

1. create an account at github.com

2. set up your user credientials on your remote server (ex. poseidon)
    a. type   
          git config user.email you@example.com
          and/or
          git config user.name YourUserName
 
3. initialize your local repository and begin saving/uploading process
    a. in the remote server, decide in which parent folder
       you want to save to github 
       (ex. /data/project1/yourname/)
    b. type 
       git init        
       while in that folder 
    c. type 
       git add 
       followed by an asterisk * if you want to save/upload everything
       or add certain folders 
       (ex. git add * or git add folder/*)
       this can be repeated for many folders if needed
    d. type 
       git commit -m  
       followed by some message within single apostrophes ''
       (ex. git commit -m 'first commit')
       new commits usually say what has been updated since the last commit

4. make a new repository on github.com 
    a. click green 'New' button
    b. choose a repository name based on what folder(s)/file(s) you added in 3c    
    c. choose to make it public or private

5. connect your remote server git to github.com
    a. in your new repository on the website, you'll find an SSH link
       (ex. https://github.com/yourname/test.git)
    b. in your remote session where you initialized your local repository, type
       git remote add origin ssh-link
       (ex. git remote add origin https://github.com/yourname/test.git)
    c. now to push your save/upload/changes, type
       git push -u origin master
    d. enter your credentials
    e. your folders and files should now show up on github.com in your new
       repository. you're done setting up your repository!

6. pushing new changes and version control
    a. github.com now has a version of your folders/files/scripts. you can
       repeatedly push new changes any time you make an update or regularly push
       changes (ex. every week) and github will keep track of changes you made
       in your files, files you deleted, and new files you make.
    b. you can look at and download old versions of commits you made if needed
    c. how to commit and push new changes
        i. with your repository initialized, you now only need to do steps
           3c, 3d, and 5c for any changes you made (you can still do git add *
           to track all changes in that folder)
           (ex. git add * 
                git commit -m 'changed something'
                git push -u origin master)

