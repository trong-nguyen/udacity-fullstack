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

### VirtualBox and Vagrant:
- vagrant is like a layer above virtualbox - the virtualization layer. Virtualization layers could be anything like virtualmachine, virtualbox, etc.
- `vagrant global-status`: list all vagrant machines:
- `VBoxManage list runningvms`: list all running virtualbox machines:
- `VBoxManage controlvm vm_id poweroff`: stop a virtualbox machine where `vm_id` could be obtained from the above `list` command
- `lsof -n -i4TCP:8080` check which PID occupies which port, for ex. 8080 here



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