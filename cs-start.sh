#!/bin/bash
set -u
set -e

#variables de entorno desde archivo environmentVar
set -o allexport
source environmentVar
set +o allexport

#levantamiento de imagenes
cd CS_Evaluation
cd MMSS_evaluation
sudo docker build -t mss_evaluations .
cd ..
cd ..

cd CS_Recomendation
cd MMSS_recomendation
sudo docker build -t mss_recomendations .
cd ..
cd ..

printf "%b\n" "\e[1;92m>> Starting compatibility Service"

#levantamiento de contenedores
docker-compose -p compatibilityservice up -d

set +e
set +u