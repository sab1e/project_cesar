import os


DB_NAME = 'projects_db.sqlite'

path_to_templates = os.path.dirname(os.path.abspath(__file__))
PATH_TO_INDEX_HEAD = os.path.join(path_to_templates,
                                  'templates', 'index_head.html')
PATH_TO_INDEX_FOOT = os.path.join(path_to_templates,
                                  'templates', 'index_foot.html')

with open(PATH_TO_INDEX_HEAD, 'r') as f:
    INDEX_HEAD = f.read()

with open(PATH_TO_INDEX_FOOT) as f:
    INDEX_FOOT = f.read()