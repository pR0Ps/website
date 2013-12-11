Title: Setting up TortiseHg on Windows
Date: 2012-05-26 20:47
Author: Carey Metcalfe
Tags: application, code, windows

TortiseHg can be a bit of a pain to set up if you don't want to
have [peagent][] running in the background all the time for
authentication. This method uses TortisePlink (comes with the install)
for authentication, and runs it only when it needs to authenticate.  

Generating a public/private key pair
------------------------------------

1. Download [PuTTYgen][peagent] and run it.
2. Generate the key pair by clicking the generate button.
3. Optionally, enter a passphrase to protect the private key.
4. Save the public and private keys somewhere. I prefer to save them as
   `id_rsa.pub` and `id_rsa.ppk` in `C:/Users/[username]/.ssh/` but it
   doesn't really matter.

  
Setting up TortiseHg
--------------------

1. Download [TortiseHg][] and install it.
2. When installing, make sure that SSH Utils are installed.
3. When it finishes installing, run the program (it'll be called
   "TortiseHg Workbench" in the start menu).
4. Configure the settings as you see fit. This will generate a
   configuration file at `C:/Users/[username]/mercurial.ini`.
5. Close the program and open up `mercurial.ini` in a text editor.
6. Under the "[ui]" section (if it doesn't exist, create it) add/edit two
   entries (adjusting for your own custom settings):

```
username = [name] <[email]@[domain]>
ssh = "C:\\Program Files\\TortoiseHg\\TortoisePlink.exe" -i "C:\\Users\\[username]\\.ssh\\id_rsa.ppk"
```

Now all that's needed is to upload the generated public key to the
server(s) you wish to pull from or push to.

When asked, just open the
key up in a text editor (make sure it's the public key, NEVER share your
private key) and copy-paste the text.

After configuring this, you'll be able to push to repositories on the
servers you give your public key to, without having to enter your password every time.

  [peagent]: http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
  [TortiseHg]: http://tortoisehg.bitbucket.org/download/index.html
