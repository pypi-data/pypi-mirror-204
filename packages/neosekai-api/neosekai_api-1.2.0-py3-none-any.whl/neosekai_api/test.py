from neosekai_api import Novel

novel = Novel('https://www.neosekaitranslations.com/novel/oresuki/')
print(novel.get_index_page())
