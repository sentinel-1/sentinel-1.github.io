#!/usr/bin/env python
# coding: utf-8

# ## Web Scrape Metadata of [The Open Graph protocol](https://ogp.me/) Compliant Posts/Articles
# 

# In[1]:


from datetime import datetime, timedelta
nb_st = datetime.utcnow()
print(f"\nNotebook START time: {nb_st} UTC\n")


# In[2]:


get_ipython().run_cell_magic('HTML', '', '<style>\n@media (max-width: 540px) {\n  .output .output_subarea {\n    max-width: 100%;\n  }\n}\n</style>\n<script>\n  function code_toggle() {\n    if (code_shown){\n      $(\'div.input\').hide(\'500\');\n      $(\'#toggleButton\').val(\'🔎 Show Python Code\')\n    } else {\n      $(\'div.input\').show(\'500\');\n      $(\'#toggleButton\').val(\'⌦ Hide Python Code\')\n    }\n    code_shown = !code_shown\n  }\n\n  $( document ).ready(function(){\n    code_shown=false;\n    $(\'div.input\').hide();\n    $(\'div.input:contains("%%HTML")\').removeClass( "input")\n    $(\'div.input:contains("%%capture")\').removeClass("input")\n  });\n</script>\n<form action="javascript:code_toggle()">\n  <input type="submit" id="toggleButton" value="🔎 Show Python Code"\n         class="btn btn-default btn-lg">\n</form>\n')


# In[3]:


import pandas as pd
from pathlib import Path
import warnings
import requests
from bs4 import BeautifulSoup
import json


# In[4]:


warnings.filterwarnings(action='error')


# In[5]:


VERBOSE = False
BASE_LANGUAGE = 'en'
OUTPUT_DIR = Path.cwd() / 'docs'


# In[6]:


df = pd.read_csv("data/shares.csv")

if VERBOSE:
    display(df)


# In[7]:


ogp_data = {}


for idx,row in df.iterrows():
    
    if VERBOSE:
        print(f"*** Processing: ({idx}) [{row['Language']}] {row['URL']}")
    
    if not row['Language'] in ogp_data:
        ogp_data[row['Language']] = []
        
        if VERBOSE:
            print(" ** New Language: ", row['Language'])
    response = requests.get(row['URL'])
    
    if VERBOSE:
        print("  * Response status code:", response.status_code)
    elif response.status_code < 200 or response.status_code >= 300:
        print(f"*** Processing: ({idx}) [{row['Language']}] {row['URL']}")
        print("  * Response status code:", response.status_code)

    soup = BeautifulSoup(response.text)

    ogp_data[row['Language']].append({
        "og_url": soup.find(
            "meta", attrs={"property": "og:url"}).attrs["content"],
        "og_type": soup.find(
            "meta", attrs={"property": "og:type"}).attrs["content"],
        "og_title": soup.find(
            "meta", attrs={"property": "og:title"}).attrs["content"],
        "og_description": soup.find(
            "meta", attrs={"property": "og:description"}).attrs["content"],
        "og_image": soup.find(
            "meta", attrs={"property": "og:image"}).attrs["content"],
        "og_image_alt": soup.find(
            "meta", attrs={"property": "og:image:alt"}).attrs["content"],
        "og_image_type": soup.find(
            "meta", attrs={"property": "og:image:type"}).attrs["content"],
        "og_image_width": soup.find(
            "meta", attrs={"property": "og:image:width"}).attrs["content"],
        "og_image_height": soup.find(
            "meta", attrs={"property": "og:image:height"}).attrs["content"],
        "article_published_time": soup.find(
            "meta",
            attrs={"property": "article:published_time"}).attrs["content"],
        "article_modified_time": soup.find(
            "meta",
            attrs={"property": "article:modified_time"}).attrs["content"],
        "article_publisher": soup.find(
            "meta", attrs={"property": "article:publisher"}).attrs["content"],
        "article_author": [
            x.attrs["content"]
            for x in soup.find_all("meta",
                                   attrs={"property": "article:author"})
        ],
        "article_section": soup.find(
            "meta", attrs={"property": "article:section"}).attrs["content"],
        "article_tag": [
            x.attrs["content"]
            for x in soup.find_all("meta", attrs={"property": "article:tag"})
        ],
    })


# In[8]:


if VERBOSE:
    print("*** Languages encountered:",", ".join(ogp_data.keys()))

for language in ogp_data.keys():
    
    if language == BASE_LANGUAGE:
        p = OUTPUT_DIR
    else:
        p = OUTPUT_DIR / language
    p.mkdir(parents=True, exist_ok=True)
    p /= "ogp.json"
    
    if VERBOSE:
        print(f"  * Writing [{language}]:", p.relative_to(Path.cwd()))
    with open(p , 'w') as f:
        f.write(json.dumps(ogp_data[language], indent="\t"))


# In[9]:


print(f"\n ** Total Elapsed time: {datetime.utcnow() - nb_st} ** \n")
print(f"Notebook END time: {datetime.utcnow()} UTC\n")

