import glob

files = glob.glob('StopWords/*')

with open("all_stop_word.txt", "wb") as outfile:
    for f in files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
  