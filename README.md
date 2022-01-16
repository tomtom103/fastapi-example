# Dockerized FastAPI Project Skeleton

## How to use localtunnel

In order for our server to be visible for a production app (in our case Gitlab Pages) we need to be able to expose our localhost endpoint.

Since ngrok no longer offers a static URL for the free tier, we chose to go with [localtunnel](https://github.com/localtunnel/localtunnel)

### How to make it work:

First, you need to install localtunnel globally

```bash
npm install -g localtunnel
```

Then, to run the tunnel, simply run `lt --port {port_number}`

For our application, this is automatically done through a child process. 