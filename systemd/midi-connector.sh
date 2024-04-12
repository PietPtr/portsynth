#!/bin/bash

while true; do
    aconnect 20:0 128:0
    status1=$?
    aconnect 20:0 129:0
    status2=$?
    
    if [ $status1 -eq 0 ] && [ $status2 -eq 0 ]; then
        echo "Connected successfully to both."
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
        echo "Failed to connect to one or both devices. Retrying in 1 second..."
        sleep 1
    fi
done
