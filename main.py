from optparse import OptionParser
from ssl import VerifyMode
from flask import Flask, render_template, request
import hurry.filesize, secrets, json, os
from os.path import splitext
from PIL import Image
from multidict import getversion
from tomlkit import key
import config
from config import version, api_key, description, domain, port, uploader_name, keywords, logo, website ,author_name, storage_folder, github, discord
from getversion import versiondata
from getchangelog import string1

print("[KOOLIMGS] Starting KoolIMGS..")

print("[KOOLIMGS] Checking version..")
if version == versiondata:
 print("[KOOLIMGS] You are up to date your version is", versiondata)
 app = Flask(__name__)
 print("[KOOLIMGS] Loading Pages...")
 @app.route('/')
 def index():
     return render_template('index.html',embeddsc=description ,keyemwords=keywords, websitelogo=logo,uploaderhostname=uploader_name, URL=domain, git=github, websiteurl=website, dsc=discord)
 @app.route('/info')
 def info():
     return render_template('svinfo.html', keyemwords=keywords, websitelogo=logo, uploaderhostname=uploader_name, URL=domain, git=github, websiteurl=website, dsc=discord)

 @app.route('/<page>')
 def screenshoturl(page):
     if f'{page}.png' not in os.listdir(storage_folder):
         return render_template('404.html', URL=domain)

     uploader = 'N/A'
     try:
         with open(f'static/screenshots/json/{page}.json') as f:
             uploader = json.load(f)["author_name"]
     except Exception as e:
         print(e)
         pass
     return render_template('sstemplate.html',
                            ss_location=f'./static/screenshots/images/{page}.png',
                            json_location=f'./static/screenshots/json/{page}.json',
                            upload_username=uploader,
                            uploaderhostname=uploader_name,
                            cur_url=page, git=github, websiteurl=website, dsc=discord, keyemwords=keywords, websitelogo=logo)
 @app.route('/upload', methods=['POST']) 
 def upload():
     if not request.method == 'POST':
         return {"error": "Method Not Allowed"}, 405
     used_api_key = request.form.to_dict(flat=False)['secret_key'][0]

     if used_api_key == api_key:
         file = request.files['image']
         extension = splitext(file.filename)[1]
         file.flush()
         size = os.fstat(file.fileno()).st_size
         if extension != '.png':
             return 'File type is not supported', 415

         elif size > 6000000:
             return 'File size too large', 400

         else:
             image = Image.open(file)
             data = list(image.getdata())
             file_without_exif = Image.new(image.mode, image.size)
             file_without_exif.putdata(data)
             filename = secrets.token_urlsafe(8)
             file_without_exif.save(os.path.join(storage_folder, filename + extension))
 
             image_json = {"title": uploader_name,   
                           "author_name": author_name,
                           "author_url": domain,
                           "provider_name": hurry.filesize.size(size, system=hurry.filesize.alternative)}
 
             with open(f'./static/screenshots/json/{filename}.json', 'w+') as f:
                 json.dump(image_json, f, indent=4)
             return json.dumps({"filename": filename, "extension": extension}), 200
     else:
        return 'Unauthorized use', 401

 @app.route('/delete')
 def delete():
     del_url = request.args.get('del_url')
     used_api_key = request.args.get('api_key')
     if f"{del_url}.png" in os.listdir('./static/screenshots/images'):

         if used_api_key == api_key:
             os.remove(f'./static/screenshots/images/{del_url}.png')
             os.remove(f'./static/screenshots/json/{del_url}.json')
             return render_template('succes.html', URL=domain), 200
         else:
             return render_template('faild.html', URL=domain), 401
     else:
         return render_template('404.html', URL=domain), 404

 print("[KOOLIMGS] Loading webserver..")
 print("[KOOLIMGS] Starting webserver on", port)
 app.run("0.0.0.0", port)
 print("[KOOLIMGS] DONE")
else:
    print("You have to update KoolIMGS")
    print("You have the version",version, "and you need to update to", versiondata)