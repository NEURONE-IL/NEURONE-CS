import os
#For Production environment in Windows
#para ambiente de producción en windows
os.system('powershell MMSS_recomendation/MS_a_recomendation/main.py -WindowStyle hidden') #9010
os.system('powershell MMSS_recomendation/MS_abbr_recomendation/main.py -WindowStyle hidden') #9011
os.system('powershell MMSS_recomendation/MS_acronym_recomendation/main.py -WindowStyle hidden') #9012
os.system('powershell MMSS_recomendation/MS_applet_recomendation/main.py -WindowStyle hidden') #9013
os.system('powershell MMSS_recomendation/MS_area_recomendation/main.py -WindowStyle hidden') #9014
os.system('powershell MMSS_recomendation/MS_audio_recomendation/main.py -WindowStyle hidden') #9015
os.system('powershell MMSS_recomendation/MS_button_recomendation/main.py -WindowStyle hidden') #9016
#os.system('powershell MMSS_recomendation/MS_caption_recomendation/main.py -WindowStyle hidden') #9017
os.system('powershell MMSS_recomendation/MS_dd_recomendation/main.py -WindowStyle hidden') #9018
os.system('powershell MMSS_recomendation/MS_div_recomendation/main.py -WindowStyle hidden') #9019
os.system('powershell MMSS_recomendation/MS_embed_recomendation/main.py -WindowStyle hidden') #9020
#os.system('powershell MMSS_recomendation/MS_fieldset_recomendation/main.py -WindowStyle hidden') #9021
#os.system('powershell MMSS_recomendation/MS_figcaption_recomendation/main.py -WindowStyle hidden') #9022
#os.system('powershell MMSS_recomendation/MS_figure_recomendation/main.py -WindowStyle hidden') #9023
os.system('powershell MMSS_recomendation/MS_headings_recomendation/main.py -WindowStyle hidden') #9024
#os.system('powershell MMSS_recomendation/MS_iframe_recomendation/main.py -WindowStyle hidden') #9025
os.system('powershell MMSS_recomendation/MS_img_recomendation/main.py -	WindowStyle hidden') #9026
os.system('powershell MMSS_recomendation/MS_input_recomendation/main.py -WindowStyle hidden') #9027
os.system('powershell MMSS_recomendation/MS_label_recomendation/main.py -WindowStyle hidden') #9028
#os.system('powershell MMSS_recomendation/MS_legend_recomendation/main.py -WindowStyle hidden') #9029
os.system('powershell MMSS_recomendation/MS_link_recomendation/main.py -WindowStyle hidden') #9030
#os.system('powershell MMSS_recomendation/MS_map_recomendation/main.py -WindowStyle hidden') #9031
os.system('powershell MMSS_recomendation/MS_object_recomendation/main.py -WindowStyle hidden') #9032
os.system('powershell MMSS_recomendation/MS_pre_recomendation/main.py -WindowStyle hidden') #9033
os.system('powershell MMSS_recomendation/MS_span_recomendation/main.py -WindowStyle hidden') #9034
os.system('powershell MMSS_recomendation/MS_table_recomendation/main.py -WindowStyle hidden') #9035
os.system('powershell MMSS_recomendation/MS_video_recomendation/main.py -WindowStyle hidden') #9036
os.system('powershell ../CS_Evaluation/MS_HTML_cleaning/main.py -WindowStyle hidden') #8002 #ok
os.system('powershell ../CS_Evaluation/MS_HTML_extraction/main.py -WindowStyle hidden') #8001 #ok
os.system('python Recomendation_Service/main.py') #9000