#!/bin/bash

while true; do
    aconnect 20:0 128:0
    if [ $? -eq 0 ]; then
        echo "Connected successfully."
        connection_active=false
        while true; do
            if aconnect -l | grep -q 'Connected From: 20:0'; then
                if [ "$connection_active" = false ]; then
                    echo "Connection is active."
                    connection_active=true
                fi
                sleep 1
            else
                echo "Connection lost. Reconnecting..."
                break
            fi
        done
    else
        echo "Failed to connect. Retrying in 1 second..."
        sleep 1
    fi
done
