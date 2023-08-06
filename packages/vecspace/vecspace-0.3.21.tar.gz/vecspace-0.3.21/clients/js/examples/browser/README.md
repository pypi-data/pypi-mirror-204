## Demo in browser 

Update your settings to add `localhost:3000` to `vecspace_server_cors_allow_origins`. 

For example:

```
client = vecspace.Client(
    Settings(vecspace_api_impl="rest", vecspace_server_host="localhost", vecspace_server_http_port="8000", vecspace_server_cors_allow_origins=["http://localhost:3000"])
)

```

1. `yarn dev` 
2. visit `localhost:3000`