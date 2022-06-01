import time
import sys
#### GIANNIS MPARZAS 2765
_tags=[]
for i in range(1,len(sys.argv)):### take tags from user and put them in list: _tags 
     _tags.append(sys.argv[i].strip())

print("the input tags are:",_tags)
time0=time.time()
f=open('Restaurants_London_England.tsv','r+')
restaurant_list=[]
line=f.readline()
while(line):###set the list that holds the file

     restaurant_list.append(line)
     line=f.readline()

time1=time.time()


file_size=len(restaurant_list)
print("file length: ",file_size)
print("scan time :",time1-time0)
inverted_={}
def update_inverted(tags,row):###update dictionary (inverted file)inverted_
     
     for i in tags:
          
          if(i in inverted_.keys()):
               inverted_[i].append(row)
               sorted(inverted_[i])
               
          else:
               inverted_[i]=[row]
     

for i in range(file_size):### create the dictionary (inverted file) inverted_
                         ### key 1 tag and value a list of ints pointing into lines in restaurant_list
     line_array=restaurant_list[i].split("\t")
     tags=line_array[2].split(":")
     all_tags=tags[1].rstrip().split(",")
     #all_tags[len(all_tags)-1].rstrip()
     for j in range(len(all_tags)):
               all_tags[j]=all_tags[j].strip()
     update_inverted(all_tags,i)


def merge_join(list1,list2):### used by kwSearchIF to find the intersection
                         ### in two list of tags

     size_1=len(list1)
     size_2=len(list2)
     join_Result=[]
     c1=0
     c2=0
     while(c1!=size_1 and c2!=size_2):

          

          while(list1[c1]<list2[c2] and c1!=size_1-1):
               c1+=1
          while(list2[c2]<list1[c1]and c2!=size_2-1):
               c2+=1
          if( list2[c2]==list1[c1]):
               join_Result.append(list2[c2])
               c1+=1
               c2+=1
          else:
               if(c1==size_1-1 or c2==size_2-1):
                    return join_Result
               
          

     return join_Result



def kwSearchIF(tag_list):### THE kwSearchIF SEARCH USING inverted_  (dict) 
     tag_vertexes=[]
     if(len(tag_list)==0):
          print("[IF] there are no tags given!")
          return []
     for i in tag_list:### FOR EVERY TAG TAKE ITS LIST AND PUT IT TO tag_vertexes LIST 

          if(i in inverted_.keys()):

               tag_vertexes.append(inverted_[i])
          
     tags=len(tag_vertexes)
     if(len(tag_vertexes)==0):
          return[]
     tag1=tag_vertexes[0]
     if(tags==1):### CHECK IF THERE IS ONLY ONE TAG 

          return tag1

     join_Result=tag1
     for i in range(1,tags):### DO MERGE JOIN IF MORE THAN ONE TAGS EXISTS

          join_Result=merge_join(join_Result,tag_vertexes[i])

     return join_Result

          
          

def kwSearchRaw(tag_list):### THE kwSearchRaw search restaurant_list raw by raw
     
     raw_Result=[]
     if(len(tag_list)==0):
          print("[Raw] there are no tags given!")
          return []
     for i in range(len(restaurant_list)):

          line_array=restaurant_list[i].split("\t")
          tags=line_array[2].split(":")
          all_tags=tags[1].rstrip().split(",")
          for j in range(len(all_tags)):
               all_tags[j]=all_tags[j].strip()
          
          if(set(tag_list).issubset(set(all_tags))):
               
               raw_Result.append(i)

     return raw_Result


print("number of keywords:",len(inverted_))
print("frequencies:",[ len(inverted_[k]) for k in sorted(inverted_, key=lambda k: len(inverted_[k]), reverse=False)])### sort frequencies 


time2=time.time()
Result_IF=kwSearchIF(_tags)
time3=time.time()

cost_IF=time3-time2
IF_size=len(Result_IF)

Result_Raw=kwSearchRaw(_tags)
time4=time.time()

cost_Raw=time4-time3
Raw_size=len(Result_Raw)

print("\n\n")### show results

print("kwSearchIF:",IF_size,"results  cost =",cost_IF ,"seconds")
      
for i in Result_IF:
      print(restaurant_list[i])
      
print("kwSearchRaw:",Raw_size ,"results  cost =",cost_Raw ,"seconds")
      
for i in Result_Raw:
      print(restaurant_list[i])











     

     
     
     
     
     
     
