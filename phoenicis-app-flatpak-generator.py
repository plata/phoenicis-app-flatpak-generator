import argparse
from shutil import copyfile
import errno
from PIL import Image
import json
import os
import re
from string import Template

parser = argparse.ArgumentParser(description='Generate Phoenicis app flatpaks.')
parser.add_argument('-i', '--input', help="input directory")
parser.add_argument('-o', '--output', help="output directory")

args = parser.parse_args()

# ensure that output directory exists
if not os.path.exists(args.output):
    try:
        os.makedirs(args.output)
    except OSError as exc:  # guard against race condition
        if exc.errno != errno.EEXIST:
            raise

####################
# info
####################
# parse app info
application_json_path = args.input + '/../application.json'

with open(application_json_path) as json_file:
    data = json.load(json_file)
    app_name = data['name']
    app_id = data['id']

# parse script info
script_json_path = args.input + "/script.json"

with open(script_json_path) as json_file:
    data = json.load(json_file)
    script_id = data['id']

print("Generate flatpak for \"" + app_name + "\" (" + script_id + ")")

app_name_clean = re.sub('[^a-zA-Z0-9 ]', '', app_name)
app_id_parts = app_id.split('.')
app_flatpak_id = app_id_parts[-1]
app_category = app_id_parts[1].capitalize()
# map category according to https://specifications.freedesktop.org/menu-spec/latest/apa.html
allowed_categories = ['AudioVideo',
                      'Development',
                      'Education',
                      'Game',
                      'Graphics',
                      'Network',
                      'Office',
                      'Science',
                      'System',
                      'Utility'
                      ]
map_categories = {'Games': 'Game', 'Accessories': 'Utility', 'Internet': 'Network', 'Multimedia': 'AudioVideo'}
if app_category in map_categories:
    app_category = map_categories[app_category]
if app_category not in allowed_categories:
    print("Warning: unknown category")
    app_category = 'X-' + app_category
script_id_parts = script_id.split('.')
script_install_id = ' '.join(script_id_parts)

####################
# copy files
####################
print("Copy repositories.json")
copyfile('templates/repositories.json', args.output + '/repositories.json')

####################
# templates
####################
replace_dict = {'APP_NAME': app_name,
                'APP_NAME_CLEAN': app_name_clean,
                'APP_ID': app_id,
                'APP_FLATPAK_ID': app_flatpak_id,
                'APP_CATEGORY': app_category,
                'SCRIPT_INSTALL_ID': script_install_id
                }

# input/output for templates
templates = {'README.md': 'README.md',
             'run-app.sh': 'run-app.sh',
             'org.phoenicis.template.yml': 'org.phoenicis.' + app_flatpak_id + '.yml',
             'org.phoenicis.template.desktop': 'org.phoenicis.' + app_flatpak_id + '.desktop',
             'org.phoenicis.template.appdata.xml': 'org.phoenicis.' + app_flatpak_id + '.appdata.xml'
             }

for template_in, template_out in templates.items():
    print("Generate " + template_out)
    template_file = open('templates/' + template_in)
    template_content = Template(template_file.read())
    result = template_content.substitute(replace_dict)
    with open(args.output + '/' + template_out, 'w') as output_file:
        output_file.write(result)

####################
# icons
####################
print("Generate icons")
icons_dir = args.output + '/icons'
if not os.path.exists(icons_dir):
    try:
        os.makedirs(icons_dir)
    except OSError as exc:  # guard against race condition
        if exc.errno != errno.EEXIST:
            raise

miniature_path = args.input + '/../miniatures/main.png'

# crop square image
im = Image.open(miniature_path)

width, height = im.size
square_size = min(width, height)

left = (width - square_size) / 2
top = (height - square_size) / 2
right = (width + square_size) / 2
bottom = (height + square_size) / 2

# crop the center of the image
square_im = im.crop((left, top, right, bottom))

icon_sizes = [16, 22, 24, 32, 48, 64, 256]
for icon_size in icon_sizes:
    thumbnail = square_im.resize((icon_size, icon_size), Image.ANTIALIAS)
    thumbnail.save(icons_dir + '/' + app_flatpak_id + '_' + str(icon_size) + '.png', "PNG")
