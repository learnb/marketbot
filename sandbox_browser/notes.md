
Container has full chrome browser, selenium, and a VNC server.

## Start container

in `marketbot/sandbox_browser` run:
```
docker compose up -d
```


## connect vnc client to running sandbox container

```
vncviewer localhost:5900
```

default password is `secret`.
- can be set with `VNC_PASSWORD` env var.


