#!/env/python

# first, we want to read in the latex file

# then, we split the latex file up into data:
#    Header
#      Title
#      Author 1
#        Institution
#        Email
#        Website
#      ...
#      Date Published
#      DOI
#      Citation
#    Section 1
#      Text
#      Figures
#      Tables
#      Algorithms
#    ...
#    References

# Then, we write those to html files, etc
# Header files go to yaml files
# Text goes to md files
# Figures go to svg files

# Then, we commit and push 