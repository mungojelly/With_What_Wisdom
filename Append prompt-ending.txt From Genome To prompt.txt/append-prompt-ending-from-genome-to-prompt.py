# set the cwd to the dir this script itself is in
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# go through each subdir of the ./inbox
# get the prompt-ending.txt from their genome subdir & append it to the prompt.txt in the subdir
# then move them to the ./outbox
import glob
import shutil
for process_dir in glob.glob('./inbox/*'):
    genome_dir = process_dir + '/genome'
    prompt_ending = open(genome_dir + '/prompt-ending.txt', 'r').read()
    prompt = open(process_dir + '/prompt.txt', 'a')
    prompt.write(prompt_ending)
    prompt.close()
    shutil.move(process_dir, './outbox')
    print('appended prompt-ending.txt from ' + genome_dir + ' to prompt.txt in ' + process_dir)

# now print some cute emojis
print('👍')