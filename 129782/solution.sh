#!/bin/bash

groupadd shared
useradd -m -G shared user1
useradd -m -G shared user2
mkdir /shared_files
touch /shared_files/shared_file
chown -R user1:shared /shared_files
chmod 660 /shared_files/shared_file
userdel -r user1
userdel -r user2
groupdel -f shared
rm -r /shared_files