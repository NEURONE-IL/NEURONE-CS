import os
#PPP: For Production environment in Windows
#PPP: para ambiente de producción en windows
os.system('powershell MMSS_evaluation/MS_a_evaluation/main.py -WindowStyle hidden') #8010
os.system('powershell MMSS_evaluation/MS_abbr_evaluation/main.py -WindowStyle hidden') #8011
os.system('powershell MMSS_evaluation/MS_acronym_evaluation/main.py -WindowStyle hidden') #8012
os.system('powershell MMSS_evaluation/MS_applet_evaluation/main.py -WindowStyle hidden') #8013
os.system('powershell MMSS_evaluation/MS_area_evaluation/main.py -WindowStyle hidden') #8014
os.system('powershell MMSS_evaluation/MS_audio_evaluation/main.py -WindowStyle hidden') #8015
os.system('powershell MMSS_evaluation/MS_button_evaluation/main.py -WindowStyle hidden') #8016
#os.system('powershell MMSS_evaluation/MS_caption_evaluation/main.py -WindowStyle hidden') #8017
os.system('powershell MMSS_evaluation/MS_dd_evaluation/main.py -WindowStyle hidden') #8018
os.system('powershell MMSS_evaluation/MS_div_evaluation/main.py -WindowStyle hidden') #8019
os.system('powershell MMSS_evaluation/MS_embed_evaluation/main.py -WindowStyle hidden') #8020
#os.system('powershell MMSS_evaluation/MS_fieldset_evaluation/main.py -WindowStyle hidden') #8021
#os.system('powershell MMSS_evaluation/MS_figcaption_evaluation/main.py -WindowStyle hidden') #8022
#os.system('powershell MMSS_evaluation/MS_figure_evaluation/main.py -WindowStyle hidden') #8023
os.system('powershell MMSS_evaluation/MS_headings_evaluation/main.py -WindowStyle hidden') #8024
#os.system('powershell MMSS_evaluation/MS_iframe_evaluation/main.py -WindowStyle hidden') #8025
os.system('powershell MMSS_evaluation/MS_img_evaluation/main.py -	WindowStyle hidden') #8026
os.system('powershell MMSS_evaluation/MS_input_evaluation/main.py -WindowStyle hidden') #8027
os.system('powershell MMSS_evaluation/MS_label_evaluation/main.py -WindowStyle hidden') #8028
#os.system('powershell MMSS_evaluation/MS_legend_evaluation/main.py -WindowStyle hidden') #8029
os.system('powershell MMSS_evaluation/MS_link_evaluation/main.py -WindowStyle hidden') #8030
#os.system('powershell MMSS_evaluation/MS_map_evaluation/main.py -WindowStyle hidden') #8031
os.system('powershell MMSS_evaluation/MS_object_evaluation/main.py -WindowStyle hidden') #8032
os.system('powershell MMSS_evaluation/MS_pre_evaluation/main.py -WindowStyle hidden') #8033
os.system('powershell MMSS_evaluation/MS_span_evaluation/main.py -WindowStyle hidden') #8034
os.system('powershell MMSS_evaluation/MS_table_evaluation/main.py -WindowStyle hidden') #8035
os.system('powershell MMSS_evaluation/MS_video_evaluation/main.py -WindowStyle hidden') #8036
os.system('powershell MS_HTML_cleaning/main.py -WindowStyle hidden') #8002
os.system('powershell MS_HTML_extraction/main.py -WindowStyle hidden') #8001
os.system('python Evaluation_Service/main.py') #8000