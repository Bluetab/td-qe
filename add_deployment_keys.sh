#!/bin/bash

rm -f ~/.ssh/td_qe.pem
echo "$PRODUCTION_PEM" | sed 's/\r//g' | sed 's/^ //g' > ~/.ssh/td_qe.pem
chmod 400 ~/.ssh/td_qe.pem
touch ~/.ssh/config
chmod 600 ~/.ssh/config
cp -f ~/.ssh/config ~/.ssh/config.bk
echo "Host ${PRODUCTION_HOST}" > ~/.ssh/config
echo "IdentityFile ~/.ssh/td_qe.pem" >>  ~/.ssh/config
chmod 400 ~/.ssh/config
