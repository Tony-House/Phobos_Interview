#!/bin/bash
if [ $# -ne 3 ] || [ $1 -lt 1 ] || [ $1 -gt 50 ] || [ $2 -lt 1 ] || [ $2 -gt 50 ] || [ -z $3 ]; then
    echo 'Test script for phobos_server.py. Emulates multiple clients with multiple random requests with curl.'
    echo 'Usage: phobos_test.sh arg1 arg2 arg3'
    echo '       arg1 - amount of clients per test, >= 1, <= 50.'
    echo '       arg2 - amount of requests per client, >= 1, <= 50.'
    echo '       arg3 - log file(s) with test commands and output'
    exit 1
fi

METHODS=('curl -X GET http://localhost:5000/' \
         'curl -X GET http://localhost:5000/api/prime/' \
         'curl -X GET http://localhost:5000/api/factoring/' \
         'curl -X POST -d "127.0.0.1" -i http://localhost:5000/api/ping/')

RES_CMD=''
for (( i = 1; i <= $1; i++ )); do
    RES_CMD=$RES_CMD'( '
    > $3$i.txt
    for (( j = 1; j <= $2; j++ )); do
        RAND_METHOD=$(( $RANDOM % 4 ))
        RAND_ARG=''
        case $RAND_METHOD in
        0)
            RAND_ARG=''
            ;;
        1)
            RAND_ARG=$(( $RANDOM % 10000000 + 1 ))
            ;;
        2)
            RAND_ARG=$(( $RANDOM % 123456788 + 2))
            ;;
        3)
            RAND_ARG=$(( $RANDOM % 10 + 1))
            ;;
        esac
        TMP_CMD=${METHODS[$RAND_METHOD]}$RAND_ARG' >> '$3$i'.txt 2>&1'
        RES_CMD=$RES_CMD"echo -e '\r\n\$ "$TMP_CMD"\r\n' >> '$3$i'.txt; "$TMP_CMD"; "
    done
    RES_CMD=$RES_CMD') & '
done
echo $RES_CMD
eval $RES_CMD
wait
echo 'Done.'
exit 0