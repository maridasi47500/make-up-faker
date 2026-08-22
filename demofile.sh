
mkdir templates 
python3 scaffold.py user pic:file username email phone password country_id:references fakejob fakebio
python3 scaffold.py country name
python3 scaffold.py htmlcolorcode content  user_id:references
python3 scaffold.py detectlanguage content language
