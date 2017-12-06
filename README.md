# Full-stack Web Development

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
- All text related commands explained
- Jenkins instead of cron jobs.

```shell
$cat   # dump the content to stdout / directed channel (by stream operator ">" )
$more
$less
$view
$tail  # remember this when I submitted jobs to compute clusters (atlas4/5/6/7), to follow what flyh.ext dumped output to stdout

$touch # update file timestamps, create 0 kb files if not existed
$nano  # file editor, standard or not depending on platforms.
       # as for
       $vim
       $vi
       $emacs
```
- Administrative Linux commands:

```shell
# read the manual of a command
$man [COMMAND]

# List recent activities on the machine
$finger [USERNAME]
# or
$cat /etc/passwd
    # and with filter
    $cat /etc/passwd | grep "[FILTERING_WORDS]"

# Add users (requires sudo)
$sudo adduser

# list all local users
$cut -d: -f1 /etc/passwd

# switch to another user (the polite way)
su - [USERNAME]
# or the bossy way, you can login as any user if having sudo privileges
sudo su - [USERNAME] # think about this as a forceful (sudo) login

# a user with sudo privileges could run commands as any user with
sudo -u [OTHER_USERNAME] [COMMAND]
# ex.
sudo -u postgres createuser tester # run the command, as if he is user postgres, to create PostgreSQL usernamed tester
```

## Linux file permission model

Commands:
```shell
$chmod [OCTAL_PERMISSION. ex 744] [FILE/DIR_NAME.] # change permission
$chown [NEW_OWNER] [FILE/DIR_NAME.]                # change the owner
$chgrp [NEW_GROUP] [FILE/DIR_NAME.]                # change the group
```

A standard text-based permission description has this form (when type `$ls [FILE/DIR] -al`). The 10-character length string

Example of `ls [DIR] -al` command

```shell
drwxr-xr-x 6 vagrant vagrant    4096 Jul 24 13:58 redis-stable
-rw-r--r-- 1 root    root    1743687 Jul 24 13:59 redis-stable.tar.gz
drwx------ 2 vagrant root       4096 Sep 15 07:55 .ssh
```

can be intepreted as:

|permission string| hard links | owner | group | size | last modified | name |
|-|-|-|-|-|-|-|
|drwxr-xr-x | 6 | vagrant | vagrant |    4096 | Jul 24 13:58 | redis-stable|
|-rw-r--r-- | 1 | root |    root |    1743687 | Jul 24 13:59 | redis-stable.tar.gz|
|drwx------ | 2 | vagrant | root |       4096 | Sep 15 07:55 | .ssh|

and the permission string can be dissected further:

|position|value|description|targeting|
|--------|-----|-----------|----------------|
|0.      |d  |  is directory or not | |
|1.      |r  |  Read permission    | Owner |
|2.      |w  |  Write permission   | Owner |
|3.      |x  |  eXecute permission | Owner |
|4.      |r  |  Read permission    | Group |
|5.      |w  |  Write permission   | Group |
|6.      |x  |  eXecute permission | Group |
|7.      |r  |  Read permission    | Public |
|8.      |w  |  Write permission   | Public |
|9.      |x  |  eXecute permission | Public |

where the value (either d or r/w/x) if present implies allowed (or is), dash (-) disallowed.

### Summary
![](https://www.ics.uci.edu/computing/bin/img/perms1.png)

***The logic behind number-based permission forms and text-based permission forms***: the former can be converted to the latter by noticing that for each permission target (owner / group / public), there are 3 rights (rwx) which theoretically translates to 8 possibilities (2<sup>3</sup>). Therefore each permission target can be represented by a number from 0 to 7. Then a full text-based permission form `rwxrwxrwx` can be translated to a number-based permission form of `777`. Another example would be `rw-` = 1 x 2 <sup>2</sup> + 1 x 2<sup>1</sup> + 0 x 2<sup>0</sup>. The number-based labeling has a simple name of octal permissions.

### URN, URL and URI
Reference is right [here](https://danielmiessler.com/study/url_vs_uri/)

URLs and URNs are URIs. All refer to resources (letter R). For example, in http://domain.com/path, **http://** is the mean (or **ftp://**, or **mailto:**), **domain.com/path** is the name (URN) and so URLs would technically be `the mean + the name`. URIs are the most generic terms, they could be anything that somehow identify something. URLs are the most specific which show you exactly **how** and **what** to get.

Surprisingly (or not) by that definition, `tel:+1 728 9239` **is** a URI!!!
![](https://danielmiessler.com/images/URI-vs.-URL-e1464829000786.png)

### AWS cheat-sheets
- Creating a folder (or an S3 object), note that the `--region` parameter is required if the region of the targeted bucket is different from the default region (i.e. *us-east-1* *us-east-2*, etc):

`aws s3api put-object --bucket [BUCKET_NAME] --key [FOLDER_NAME]/ --region [REGION_NAME]`

- Removing a folder:

`aws s3 rm s3://[BUCKET_NAME]/[PATH_TO_FOLDER] --region [REGION_NAME]`


### cURL tips
- Basic POST action with JSON data:
`curl -X POST -H "Content-Type: application/json" http:desiredurl -d '{"k1":"v1", "k2":"v2"}'`
- Basic READ action with username/password login
`curl -u myusernam:mypassword http:desiredurl`

### Web APIs
Web APIs, regardless of their problems and solutions (and the technologies they used to solve), agree in physical (e.g geographically) regards. For example, many APIs (Foursquare, Google Map, Twitter, Yelp) have a search endpoint that take in or return a `latlng` or some kind of `geocode` parameter. By utilizing this common, we can compose an API that internally patches together multiple APIs, which eventually solve our own problem. The point is all APIs aim to solve some real-world problems so it might not be so surprized that they have real-word constraints and approaches.

### Steps in Iterative Development
- Mockups
- Routing
- Templates and forms
- CRUD functionalities
- API endpoints

### Separation of Concerns Or How to deal with legacy / spaghetti codes
Depending on the level or the scale of the spaghetti-ness of the code part of interests, you have 2 options:
- If the part is not the entirety of the whole, meaning most of the code is not very horrible, you can locate that part and refactor it. It can be thought as the process of finding the strongly connected components in Graph Theory Languague. And your task is to find the component that badly connects to everything else and change it:
![](https://www.researchgate.net/profile/Katy_Borner/publication/259043184/figure/fig3/AS:297121283624963@1447850642815/Figure-3-Component-structure-of-directed-networks-such-as-the-WWW-Adopted-from-Broder.png)
- If you speculate and (fully or partially) verify that most of the code is highly coupled or in Graph Theory, a complete graph, just rewrite the whole thing.
![](https://cdn2.hubspot.net/hubfs/468123/spaghetti_code3_blog-illustrations.png)

Don't forget to do tests.

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

## JavaScript
- [Best practices and conventions from Airbnb](https://github.com/airbnb/javascript)

- Make use of `Promise.all()` to load app asynchronously while guaranteeing app is only functioning if all promises are resolved.

```javascript
allComponentsLoaded = Promise.all([
    component1.init(),
    component2.fetch(),
    component3.load()
    ]);

allComponentsLoaded.then(function () {
    app = new App(dependentAndLoadedComponents);
    app.wireDependencies();
    app.run();
    })
```

- Class constructors must only return instances, asynchrounous activities should happen either in: 1)pre-construction in loading process or 2) on-the-fly or on-demand. In general, any component depending on asynchronous functions should not be dependencies of deterministic components.

`Array.prototype.forEach.call(lackingFunctionalitiesObject, workingFunction)`
- Borrow the functionalities of a well-developed entity (Array, Object, String, 3rdParty) on another less-developed object. Think an object that is iterating like a list but is not quite a list (like HTMLCollection which is returned from `.getElementsByClassName()`)

### `apply` vs. `call` vs. `bind`
- All three modify *context*s of defined functions. *context* is technically the `this` variable in JavaScript.
```javascript
function func(x, y) {
    console.log('Context variable is', this.z);
    console.log('First variable is', x);
    console.log('Second variable is', y);
}

var context = {z: 9};

func.call(context, 1, 2); // params passed as usual
func.apply(context, [1, 2]); // params passed as list

newFunc = func.bind(context);
newFunc(1, 2); // invoked later

// results for all three:
/*
Context variable is 9
First variable is 1
Second variable is 2
*/
```
- `apply` and `call` vs. `bind`: `apply` and `call` invokes functions immediately. `bind` returns a new function with a modified context. `bind` is analogous to Python's decorators.
- `apply` vs. `call`: `call` takes variables [1:] and passes it to the function, while `apply` takes variable [1], assumed a list, unpacks it and passed the unpacked items to the function.


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
- Make [GoogleMap section responsive](https://stackoverflow.com/a/15668970/8849793).

```html
<!--
create a container
apply styles / layout to the container, not the actual google map.
The google-map element is styled as above.
-->
<div class="gmap-container">
    <div id="google-map"></div>
</div>
```

![](http://gregfranko.com/images/requirejs.png)

[Understanding RequireJS, you should read this](https://www.devbridge.com/articles/understanding-amd-requirejs/) and [How to use Bootstrap with RequireJS](https://getfishtank.ca/blog/how-to-use-bootstrap-3-with-requirejs)

- RequireJS might be obsolete when ES6 is becoming the norm but it was great at the time. RequireJS is a module loader, advocates for AMD (asynchronous) module format but also support non-AMD, conventional global variable attached scripts (those that attach themselve to `window` when loaded).
    + AMD specification requires a handshake from supporting modules - which check for a global `define` function and return the actual codes in the `define` scopes.
    + To load non-AMD modules by RequireJS, we need to use the `shim` option in `require.config`. It wraps module in a scope and register it loadable by other modules. Google Maps JS API could be successfully loaded by using the `shim` option.
```javascript
require.config({
    paths: {
        module: 'non_amd_external_or_packaged_library' // without .js extension
    },

    shim: {
        deps: [dependency_list_of_module],
        exports: 'module_name' // which will be available as a window-attached module (window.module_name)
    }
});

```

-
    + A quirky thing about RequireJS and AMD is that if an AMD module was defined as a named module (to ensure integrity or universal recognition of the library). The exact name must be used in the `path` config. Examples: jQuery `jquery` and Twitter Widgets JS `twttr`

```javascript
require.config({
    paths: {
        jquery: '//cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min' // must be exactly jquery, not jQuery not jq, nor $.
    }
});

```

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

## Serverless services with AWS Lambda and API Gateway

The idea is you only need to care about the logic part of your services, not the infrastructures that they run on. Literally, it is the Python code or Node code that you have to pay attention to, not the Linux server / or Windows IIS / plus WSGI / on Nginx / or Apache / Load balancing and a slew of other DevOps aspects and services that you normally have to setup and maintain, for example, on EC2 instances.

To be clear, with Amazon Web Services you define and manage the meat of your services (the codes) with Lambda. And all other things (API interface, documentation, access points, routing, request / response configurations) with API Gateway.

### Example project
[Build a proxy server that ports request and attaches authentication from a web app to popular APIs such as Twitter, Yelp and Foursquare](https://github.com/trong-nguyen/udacity-fullstack/tree/master/aws_lambda). Why do we need a proxy you may ask? Most modern APIs requires some form of consumer identification (it could be the webapp that built on top of those APIs or a web client that provides user interfaces to interact with such APIs).

The identification process manifests into different protocals and schemes from classic username - password authentication to standard OAuth processes.
- For simple client API consumer, browser-based OAuth applications are widely available to enable actual users (humans) identify themselves with the API they want to access (such as Google+ or Facebook login).
- For web-app scenarios, the communication is between a 3rd-party app and API providers. The API providers specifically distingush these kind of communications as server-side access and consequently enforce server-side authentication and authorization, which means we need a server key / token to consume their APIs. These kind of keys / tokens being server-side are presumably not to be exposed to end-users (those that consume the app, or the humans).

Technically it is impossible to protect these secrets (keys, tokens) if you only have a browser-only web app. The proper way to implement authentication for web apps is to have a backend that receives authenticated requests from your browser-client and do the server-server communication. A single authentication channel (which might utilize many available identification services - Google+ / Facebook / Microsoft) is needed from the client to your backend. But if you want your services public just leave it out, accepts and proxies all requests. In this way, your server secrets are properly protected. Web app done right!

Untill now, serverless architecture has no specific role in web app developement we discussed thus far. However if you want to stay lean yet insists on security and performance, you can rely on serverless services such as AWS Lambda + API Gateway or Google Cloud to build your **backend** and, obviously secure your secrets.

![](https://d1.awsstatic.com/Test%20Images/MasonTests/Lambda_WebApplications.c89e27ca2ef46c59e15107e9f5ede25dc0829207.png)

### Example implementation in AWS Lambda + API Gateway

Serverless architecture definitely requires some getting used to such as how to build a Lambda function, to deploy it with API gateway, but basically the steps required are:
- Implement service code(s):
    + Accepts requests from API Gateway (in a specific format)
    + Processes, applies business logics (probably calling other APIs, with authentication)
    + Returns a handler (a function that wraps the above two steps) to callers
- Deploy code to AWS Lambda:
    + Package your code, along with all non-built in libraries that your code depends on in a Zip format and upload it to AWS Lambda (with CLI `aws lambda create-function / update-function-code` or AWS console interface).
    + Test, add environment variables, to your deployed Lambda function.
- Build access points to your function:
    + Create an API in API gateway
    + Customize requests / responses cycle (adding CORS, error handling, etc.)
    + Hook up an API method (GET/POST) to your deployed Lambda function
    + Deploy your API in prod/dev stages, apply throtling, use plans (limit calling quota).


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


## Miscelaneous tips

### Help Github detect the correct language of your repo

- Github uses github-linguist internally to dectect your primary languages.
- This has minor cosmetic effects on your displayed repo, like how many percentages of yours is Python, C++, Javascript, etc. But it might be important in case you want to showcase resume / portfolio.
- Give Github hints by adding an `.gitattributes` and follow documentation of [github-linguist](https://github.com/github/linguist) to ignore files in statistics summary.
- Basically:
```git
path1/everything/mark/as/vendor/* linguist-vendored # or linguist-vendored=true
path2/documentation/mark/as/documentation/* linguist-documentation # or =true
path3/generated/or/minified/files/* linguist-generated # or =true
```
- Install `gem install github-linguist` to check locally
- Run `linguist [PATH] --breakdown` to read statistics, this will be identical to what Github reports.
- And remember it only takes effect after **commits**. So, commit if you want to view changes.

### Git - Mercurial
Same local repo pushes to different server repos, e.g one is git (github), the other mercurial (bitbucket).
- Follow this [http://hg-git.github.io]() to install hg-git
- Modify the `~/.hgrc` file with
```
[extensions]
hgext.bookmarks =
hggit = [path to hg-git or empty if via pip install]
```
- To correctly display the authors, modify the username field in the above `.hgrc` file as well (the email should be valid and exact)
- Add an entry to the file [repo]/.hg/hgrc

```
[paths]
default = https://trong2nguyen@bitbucket.org/trong2nguyen/stanford_software_hire_programs
github = https://github.com/trong-nguyen/aux-sshp.git # add here
```
- Install dulwich with `pip install dulwich`
- Install mercurial version 3.7 exactly `pip install mercurial==3.7` since hg-git only supports this version of mercurial
- This scenario is to push from an existing hg repo (created first) to a newly created git repo:
    + Create an empty git repo (no code, no readme, no description, etc.)
    + Add the git path to the `./hg/hgrc` file
    + Create bookmarks with `hg bookmark -r default master`
    + first push to github with `push github` (if you name the git repo as github in `.hg/hgrc`)



### Udacity Classroom Bugs
- First Project - Movie Trailer Website: Broken links to forum

## Ideas:
- Create a website to let self-taught CS students take notes and document what they learn more conveniently, systematically and demonstrably (to the hiring parties).
- A tool to help recruiters build personas from Github repo. Like how active a person is (contrib/day or month), how is his working habit, which languages he used, etc.