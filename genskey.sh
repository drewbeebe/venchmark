#!/bin/bash
GEN_SECRET_KEY=`python3 -c 'import secrets; print(secrets.token_hex(100))'`;
echo "SECRET_KEY=${GEN_SECRET_KEY}" > .env
