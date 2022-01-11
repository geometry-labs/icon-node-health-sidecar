# ICON Node Health Sidecar

A sidecar container to report liveliness and readiness of an ICON 2.0 node.

## Getting Started

### Docker

Using the health sidecar in a docker-compose stack requires adding the container to your compose file and optionally using the sidecar container as a health check for your node container.

See the [main docker-compose](docker-compose.yml) and [exporters docker-compose](docker-compose.exporters.yml) files in this repo for an example.

### Kubernetes

Using the health sidecar in a Kubernetes deployment requires adding the container as an additional container to your podspec.
In addition, it is necessary to specify the readiness/liveliness probes as part of the container definition.

For example:

```yaml
spec:
  containers:
    - name: health-sidecar
      env:
        - name: BLOCK_HEIGHT_VARIANCE
          value: "25"
        - name: CRON_SLEEP_SEC
          value: "5"
      image: geometrylabs/icon-node-health-sidecar:latest
      ports:
        - containerPort: 80
          name: readyz
          protocol: TCP
      readinessProbe:
        failureThreshold: 100
        httpGet:
          path: /readyz
          port: readyz
          scheme: HTTP
        initialDelaySeconds: 10
        periodSeconds: 10
        successThreshold: 1
        timeoutSeconds: 1
```

## Usage

### Environment Variables

| Variable              	| Type    	| Default                                      	| Description                                                             	|
|-----------------------	|---------	|----------------------------------------------	|-------------------------------------------------------------------------	|
| BLOCK_HEIGHT_VARIANCE 	| INTEGER 	| 50                                           	| Allowable difference between node and network (plus or minus value).    	|
| PEER_SEED_IP          	| STRING  	| "52.196.159.184"                             	| IP Address of a peer to check and collect network information from.     	|
| PEER_SEED_ADDRESS     	| STRING  	| "hx9c63f73d3c564a54d0eed84f90718b1ebed16f09" 	| Wallet address of a peer to check and collect network information from. 	|
| CRON_SLEEP_SEC        	| INTEGER 	| 5                                            	| Interval between successive network block height checks.                	|

### Endpoints

There are two available endpoints: `/healthz` and `/readyz`.

_Healthz_ is used to check the status of the node and whether it is responding to anything at all.
_Readyz_ is used to check the readiness of the node and whether it is able to correctly respond to a request.

If you only want to determine if your node is synced, you just need to monitor the `/readyz` endpoint. 

#### Status Codes

Healthy endpoints will return HTTP `200 "OK"`.
Unhealthy endpoints will return HTTP `503 "UNHEALTHY"`.

#### Verbose

Endpoints allow for a standard response, or a verbose response that will describe which (if any) checks are failing in an endpoint.

To access the verbose endpoint, you need to add the `?verbose=true` parameter to the endpoint query.
For instance, if you are checking the `/readyz` endpoint, your query URL would look like `http://health-container:8080/readyz?verbose=true`.

When enabled, the endpoint will use the same HTTP status code, but the content returned from the endpoint will include the individual checks.
As an example, the `/readyz` endpoint will return the following verbose output on success:

```text
[+] Node is within 2 blocks of network
```

and on failure:

```text
[-] Node is outside tolerance and is 100 blocks away from network
```

Additional checks can be added by modifying the `checks.py` file.

## License

Distributed under the Apache 2.0 License. See [LICENSE](LICENSE) for more information.
