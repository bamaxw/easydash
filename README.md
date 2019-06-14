# EasyDash

## Installation
```bash
pip install easydash --index-url https://pypi.inyourarea.co.uk/inyourarea/prod
```

## Running

```
Usage: dash <resource_type> <command> -s/--service service -c/--cluster cluster [-st/--server-type server-type]
                            resource_type:
                                Choose from: 'ecs-service' (more coming)
	                        command:
                                Chose from: 'show', 'deploy'
	-s / --service		    service: str	    REQUIRED
	-c / --cluster		    cluster: str	    REQUIRED
	-st / --server-type	    server-type: str	default: <service>
	-r / --region		    region: str	        default: eu-west-1
```

