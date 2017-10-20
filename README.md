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

### Steps in Iterative Development
- Mockups
- Routing
- Templates and forms
- CRUD functionalities
- API endpoints

### CSS Layout Structure
#### Flows

Playground can be seen [here](templates/test_css.html).

Courses can be found [here](https://classroom.udacity.com/nanodegrees/nd004/parts/fe2ad0cf-06b0-4541-87ab-0b6d59e21ef1/modules/31cc93f7-9d62-44d2-b0fc-ab68b4ff90f0/lessons/5bc1143d-6294-412b-9a32-27d17142f9d2/concepts/3346831f-e58c-4aca-863c-a785d6bc56f7).

1. **Normal flow** (default): block elements (`<div>`) stack vertically, inline elements (`<span>`) horizontally and wrap to the next line if overflow.


```css
.default {
  position: static;
}
```

You can change the default `display` attribute to change their default behaviors:

*Block*:

```css
div {
  /*default is block*/
  display: inline;
  background-color: cyan;
}
```

*Inline*:
```css
span {
  /*default is inline*/
  display: block;
  background-color: magenta;
}
```

Block elements can be sized (with `width`), inlined elements can not.

*Hybrid*: elements assigned with `inline-block` display attribute can be sized like `block` and laid out (inline) like `inline` elements.

```css
hybrid-elm {
  display: inline-block;
}
```

2. **Relative flow**: used to shift elements after they were laid out with *normal flow*.

```css
.relative {
  position: static;
  /*either this or bottom*/
  top: 10px;
  /*either this or right*/
  left: 10px;
}
```




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

## jQuery

- Create a virtual element with attributes and values:
```javascript
function dance (event) {
    danceItOff();
}

// with a property object
var e = $('<div>', { // no need to specify closing tag
    href: 'https://google.com',
    class: 'super-deco',
    click: dance
    });

var e = $('<div>')
    .attr('name', 'pretty') // or chaning method
    .text('Big deal!') // or text
    .click(dance) // or hookup events
    ;

// add children to it as you normally do to DOM elements
anotherElm = $('<li>');
e.append(anotherElement);

// or add another virtual node
e.append('<span></span>')
```

## Frontend
- CORS (Cross-Origin-Resource-Sharing) is a feature that enforced by a **web browser** to allow an access of resources on server X request resources on server Y (Access-Control-Origin: `*` or `Y` or `X, Y` etc.) or not (Access-Control-Origin: X).

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

### Preprocessing Tools
#### Convert videos for web playback with `ffmpeg`
```shell
brew install ffmpeg
ffmpeg -i [input].[inputformat] -filter:v "setpts=0.2*PTS" -s 640x480 -profile:v baseline -level 3.0 -pix_fmt yuv420p [output].[outputformat]
```

Here the parameters are:
+ `-filter:v setpts=0.2*PTS` means convert with speed up modification. Reduced frames by 0.2 means speed up playback speed 5 times, roughly. `filter:v` means video stream, likewise `:a` means audio stream
+ `-s 640x480` means adjusting the resolution by specified one.
+ `-profile:v baseline -level 3.0 -pix_fmt yuv420p` is PARTICULARLY important for web playback compatibility. It essentially says to use `baseline` profile at level 3, with pixel format `yuv420p`. This configuration proved to be compatible with Safari.




### Udacity Classroom Bugs
- First Project - Movie Trailer Website: Broken links to forum

## Ideas:
- Create a website to let self-taught CS science take notes and document what they learn more conveniently, systematically and demonstrably (to the hiring parties).