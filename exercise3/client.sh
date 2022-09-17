#!/bin/bash
var=$(docker ps -aqf "name=webapp") && docker exec -it $var python client.py