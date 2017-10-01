# Learning Full stack with Udacity

## Jump-start Toolkits
- Rolling a demonstrative server with shell + ncat:
```shell
!server                        !client
$ncat -l 8000                  $ncat 127.0.0.1 8000
listen              ---->      listen
response            <----      response
etc.                <---->     etc.
```
- Rolling a webserver in python3:
`python3 -m http.server 8000`

## Devops Tips
- [Refresh DNS](https://superuser.com/a/346519) on OSX 10.9 and above:
`sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
- Keep local and remote directories in sync with `lsyncd`, reference [here](https://serverfault.com/a/485808)
- Versioning is a standard practice to ease the pain of API changes (or transitions), allowing API consumers sufficient time to upgrade their code base, before officially ending an old API version.
### URN, URL and URI
Reference is right [here](https://danielmiessler.com/study/url_vs_uri/)

URLs and URNs are URIs. All refer to resources (letter R). For example, in http://domain.com/path, **http://** is the mean (or **ftp://**, or **mailto:**), **domain.com/path** is the name (URN) and so URLs would technically be `the mean + the name`. URIs are the most generic terms, they could be anything that somehow identify something. URLs are the most specific which show you exactly **how** and **what** to get.

Surprisingly (or not) by that definition, `tel:+1 728 9239` **is** a URI!!!
![](https://danielmiessler.com/images/URI-vs.-URL-e1464829000786.png)
### cURL tips
- Basic POST action with JSON data:
`curl -X POST -H "Content-Type: application/json" http:desiredurl -d '{"k1":"v1", "k2":"v2"}'`
- Basic READ action with username/password login
`curl -u myusernam:mypassword http:desiredurl`

## Python Tips
- Long string definition without unecessary indents and spaces
```python
long_string = (
  "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABG"
  "l0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAEN"
  "xBRpFYmctaKCfwrBSCrRLuL3iEW6+EEUG8XvIVjYWNgJdhFjIX"
  "rz6pKtPB5e5rmq7tmxk+hqO34e1or0yXTGrj9sXGs1Ib73efh1"
  "AAAABJRU5ErkJggg=="
)
```
- Or multiline string
```python
multiline_string = '''
for var in vars:
  print a
concat(a)
'''
```

### VirtualBox and Vagrant:
- vagrant is like a layer above virtualbox - the virtualization layer. Virtualization layers could be anything like virtualmachine, virtualbox, etc.
- `vagrant global-status`: list all vagrant machines:
- `VBoxManage list runningvms`: list all running virtualbox machines:
- `VBoxManage controlvm vm_id poweroff`: stop a virtualbox machine where `vm_id` could be obtained from the above `list` command
- `lsof -n -i4TCP:8080` check which PID occupies which port, for ex. 8080 here

## Oauth2 Protocols
![](https://developers.google.com/accounts/images/webflow.png)
Google's web server applications

There are 3 sides in the process:
- The user and his helper - the web client - TU
- The web server - TS
- The auth provider - TA

Scenario - Goals:
- The web server would like to make sure that the user is entitled to some resources which means:
  + The user is the one whom he claims to be
  + If so, then that identified user was granted access to the requested resources
- Technically, in order to verify the above 2 points what the web server need is:
  + A claim from the user (who he said he is)
  + A proof, which he obtained from a specific auth provider, - a CODE which can be exchanged for a TOKEN from the same provider (Google+, Facebook, etc.)
- From there authentication and authorization process can follow on the web server.

OAuth Flow:
1. The web client presents the user with a login / signup form AND a callback plus a redirect URL - what to do after signing in
2. The user sign in
3. The auth provider presents the user with login form
  - Success: return a CODE to the web client
  - Failed: return an ERR code
4. On receiving the CODE, the web client send it to the web server
5. On receiving the CODE, the web server send it to the auth provider and get back an ACCESS TOKEN (and probably an REFRESH TOKEN). Using the ACCESS TOKEN the web server can identify the user and obtain necessary information from the user.

![](https://scontent.fsgn5-4.fna.fbcdn.net/v/t39.2178-6/851584_503291546407012_1005168000_n.png?oh=b0af1d36bb8c4da5881739e7da0e371d&oe=5A409E8A)
Facebook Auth Scenario

## Templates

### Starter template with Bootstrap 4, HTML5
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>
  </body>
</html>
```

### Udacity Classroom Bugs
- First Project - Movie Trailer Website: Broken links to forum