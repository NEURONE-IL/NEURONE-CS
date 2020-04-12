#!/bin/bash
set -u
set -e
#For Production environment in Linux
#para ambiente de producción en Linux
python3 MMSS_recomendation/MS_a_recomendation/main.py & 
python3 MMSS_recomendation/MS_abbr_recomendation/main.py & 
python3 MMSS_recomendation/MS_acronym_recomendation/main.py & 
python3 MMSS_recomendation/MS_applet_recomendation/main.py & 
python3 MMSS_recomendation/MS_area_recomendation/main.py & 
python3 MMSS_recomendation/MS_audio_recomendation/main.py & 
python3 MMSS_recomendation/MS_button_recomendation/main.py & 
python3 MMSS_recomendation/MS_dd_recomendation/main.py & 
python3 MMSS_recomendation/MS_div_recomendation/main.py & 
python3 MMSS_recomendation/MS_embed_recomendation/main.py & 
python3 MMSS_recomendation/MS_headings_recomendation/main.py &
python3 MMSS_recomendation/MS_img_recomendation/main.py & 
python3 MMSS_recomendation/MS_input_recomendation/main.py & 
python3 MMSS_recomendation/MS_label_recomendation/main.py & 
python3 MMSS_recomendation/MS_link_recomendation/main.py &
python3 MMSS_recomendation/MS_object_recomendation/main.py & 
python3 MMSS_recomendation/MS_pre_recomendation/main.py & 
python3 MMSS_recomendation/MS_span_recomendation/main.py & 
python3 MMSS_recomendation/MS_table_recomendation/main.py & 
python3 MMSS_recomendation/MS_video_recomendation/main.py

set +e
set +u