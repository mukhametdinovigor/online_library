# Online library

This website is online library of scifi books.


## How to install

Download code.
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Also you need to create `.env` file and write lines like this into it:

```
FOLDER='pages'
BOOKS_PER_PAGE=10
```

You can change the folder here to customize where your html files will be placed. And you can define how many books 
will be on the every page. By default, your folder is 'pages' and books_per_page=10.

## How to run script

Run script in command line:
```
python3 render_website.py
```

This command runs the website on your local machine. You should follow this link - [http://127.0.0.1:5500](http://127.0.0.1:5500) to open this 
website.


You can deploy your site on GitHub Pages. To see how it looks follow this link:

[Online library](https://mukhametdinovigor.github.io/online_library/pages)



## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
