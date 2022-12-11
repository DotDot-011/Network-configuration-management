# Network-congiure-management
network cofigure management website for Kasetsart University

docker run -e MYSQL_ROOT_PASSWORD=test --name mydbcontainer -p 8888:3306 -d mariadb -> docker mariadb running

docker run --name odin --network asgard -p 7000:8000 --rm -d my-python-app -> docker run with network

docker network create asgard -> creat network 