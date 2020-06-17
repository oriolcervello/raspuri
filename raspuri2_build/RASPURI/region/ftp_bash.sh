#!/bin/bash
#==========================================================================
#   RASPURI v2 a RASP(Regional Atmospheric
#   Soaring Predictions) COMPUTER PROGRAM
#   Original Creator: Oriol Cervelló i Nogués ( raspuri [at] protonmail.com )
#   Copyright (C) 2019+ by Oriol Cervelló i Nogués
#==========================================================================
# License: GNU GPLv3.0
# Copyright (C) 2019  Oriol Cervelló
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#==========================================================================
#==========================================================================
# ftp_bash.sh
# This script is part of RASPURI v2
# Script calling ftp function

python3 ftp_call.py $1 $2 $3 &
# $0 ftp_bash.sh
# $2 1st arg
# $3 2nd arg
