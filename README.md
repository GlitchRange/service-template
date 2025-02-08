# Glitch Service Template

To create a service, place service source code in the `service` directory.  This must include a docker-compose.yaml file to start the service.

Place the checker in the `checker` directory.  Set the contents of the `.template` file to the name of the checker template (default is the standard glitch template, but forcad and cini are also available).

Finally, modify `service.yaml` to include the service name and ports.

To test, run `python3 test.py`, which will start the service and run the tests against it (only supports glitch checker templates).
