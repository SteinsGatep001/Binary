#!/bin/bash

echo "Start script $0"
echo "check flag file"
directory="."
flag_file="flag.txt"
if [ -f $flag_file ]
then
    echo "flag is `cat $flag_file`"
    chmod 755 $directory/*
else
    echo "flag file flag.txt does not exists"
    exit 1
fi

docker_img="ubuntu:pwn"
docker_dir="/home/pwn"
echo "args is $#"
if [ $# == 2 ]
then
    elf_file=$1
    socat_port=$2
    container_id=`docker run -it -d -p $2:$2 --name $elf_file $docker_img`
    docker cp $directory/$flag_file $container_id:$docker_dir
    docker cp $directory/$elf_file $container_id:$docker_dir
    docker exec -u pwn $container_id socat tcp-listen:$socat_port,reuseaddr,fork system:$docker_dir/$elf_file &
else
    echo "format: $0 [elf_file] [port]"
    exit 1
fi


