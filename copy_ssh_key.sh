#!/bin/bash

# List of IP addresses
ip_addresses=(
    "210.91.154.153"
    "210.91.154.154"
    "210.91.154.155"
    "210.91.154.164"
    "210.91.154.166"
    "210.91.154.175"
    "210.91.154.176"
    "210.91.154.177"
    "210.91.154.178"
    "210.123.135.139"
    "210.123.135.140"
    "210.123.135.141"
    "210.123.135.142"
    "210.123.135.143"
    "210.91.154.134"
    "210.91.154.135"
    "210.91.154.136"
    "210.91.154.137"
    "210.91.154.138"
    "210.91.154.139"
    "210.91.154.140"
    "210.91.154.158"
    "210.91.154.163"
    "210.123.135.145"
    "203.251.85.195"
    "203.251.85.196"
    "203.251.85.197"
    "203.251.85.198"
    "203.251.85.199"
    "203.251.85.200"
    "203.251.85.201"
    "203.251.85.202"
    "203.251.85.203"
    "203.251.85.204"
)

# Path to the local public key file
local_key=~/.ssh/id_rsa.pub

# Destination path on the remote servers
remote_path=~/.ssh/id_rsa.pub

# Loop through each IP address and copy the public key
for ip in "${ip_addresses[@]}"; do
    scp "$local_key" "root@$ip:$remote_path"
done