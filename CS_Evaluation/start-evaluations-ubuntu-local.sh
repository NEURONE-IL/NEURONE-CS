#!/bin/bash
set -u
set -e
#PPP: For Production environment in Linux
#PPP: para ambiente de producción en Linux
python3 MMSS_evaluation/MS_a_evaluation/main.py & 
python3 MMSS_evaluation/MS_abbr_evaluation/main.py & 
python3 MMSS_evaluation/MS_acronym_evaluation/main.py & 
python3 MMSS_evaluation/MS_applet_evaluation/main.py & 
python3 MMSS_evaluation/MS_area_evaluation/main.py & 
python3 MMSS_evaluation/MS_audio_evaluation/main.py & 
python3 MMSS_evaluation/MS_button_evaluation/main.py & 
python3 MMSS_evaluation/MS_dd_evaluation/main.py & 
python3 MMSS_evaluation/MS_div_evaluation/main.py & 
python3 MMSS_evaluation/MS_embed_evaluation/main.py & 
python3 MMSS_evaluation/MS_fieldset_evaluation/main.py & 
python3 MMSS_evaluation/MS_figure_evaluation/main.py & 
python3 MMSS_evaluation/MS_headings_evaluation/main.py & 
python3 MMSS_evaluation/MS_iframe_evaluation/main.py & 
python3 MMSS_evaluation/MS_img_evaluation/main.py & 
python3 MMSS_evaluation/MS_input_evaluation/main.py & 
python3 MMSS_evaluation/MS_label_evaluation/main.py & 
python3 MMSS_evaluation/MS_legend_evaluation/main.py & 
python3 MMSS_evaluation/MS_link_evaluation/main.py & 
python3 MMSS_evaluation/MS_map_evaluation/main.py & 
python3 MMSS_evaluation/MS_object_evaluation/main.py & 
python3 MMSS_evaluation/MS_pre_evaluation/main.py & 
python3 MMSS_evaluation/MS_span_evaluation/main.py & 
python3 MMSS_evaluation/MS_table_evaluation/main.py & 
python3 MMSS_evaluation/MS_video_evaluation/main.py &
python3 MS_HTML_cleaning/main.py & 
python3 MS_HTML_extraction/main.py

set +e
set +u