#!/bin/sh

./docker/wait-for-rabbitmq.sh

make db_migrate
make listener
