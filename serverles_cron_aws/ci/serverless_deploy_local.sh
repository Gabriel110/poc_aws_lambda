#!/usr/bin/env bash
cd ..
cd src
serverless deploy --stage local
#serverless info --stage local
exit