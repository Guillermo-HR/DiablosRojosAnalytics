#!/bin/bash

# Ver si existe la carpeta ../reporte
if [ -d "../reporte" ]; then
    rm -rf ../reporte
fi

# Carpet general
mkdir ../reporte

# Carpeta para csv
mkdir ../reporte/csv
# Carpeta para distribucion de pitcheo
mkdir ../reporte/csv/distribucionPitcheo
mkdir ../reporte/csv/distribucionPitcheo/left
mkdir ../reporte/csv/distribucionPitcheo/right
mkdir ../reporte/csv/distribucionPitcheo/total
# Carpeta para linea de pitcheo
mkdir ../reporte/csv/lineaPitcheo
# Carpeta para lineUp
mkdir ../reporte/csv/lineUp
# Carpeta para pitchers
mkdir ../reporte/csv/pitchers
# Carpeta para secuencia de pitcheos
mkdir ../reporte/csv/secuenciaPitcheo
mkdir ../reporte/csv/secuenciaPitcheo/left
mkdir ../reporte/csv/secuenciaPitcheo/right

# Carpeta para img
mkdir ../reporte/img
# Carpeta para distribucion de pitcheo
mkdir ../reporte/img/distribucionPitcheo
mkdir ../reporte/img/distribucionPitcheo/left
mkdir ../reporte/img/distribucionPitcheo/right
mkdir ../reporte/img/distribucionPitcheo/total
# Carpeta para situacion de riesgo
mkdir ../reporte/img/situacionRiesgo
# Carpeta para situacion de ventaja
mkdir ../reporte/img/situacionVentaja