import time
import sys
import math
#### GIANNIS MPARZAS 2765

query=[]
for i in range(1,len(sys.argv)):### TAKE THE COMPOSITE QUERY FROM USER AND PUT IT IN query list
     if(i<5):
          query.append(float(sys.argv[i]))
     else:
          query.append(sys.argv[i].strip())
          

print("the input cordinates are:",query[:4])
print("the input tags are:",query[4:])
time0=time.time()
f=open('Restaurants_London_England.tsv','r+')
restaurant_list=[]

x_min=1000
y_min=1000
x_max=0
y_max=0
grid_size=50

line=f.readline()
while(line):

     restaurant_list.append(line)### save file in restaurant_list
     
     line_array=line.split("\t")
     cordinates=line_array[1].split(":")
     all_cordinates=cordinates[1].rstrip().split(",")
     
     for j in range(len(all_cordinates)):
          all_cordinates[j]=all_cordinates[j].strip()

     x=float(all_cordinates[0])
     y=float(all_cordinates[1])
     
     if(x<x_min):### find min x,y and max x,y in order to find x,y steps and create the grid table
          x_min=x
     if(x>x_max):
          x_max=x
     if(y<y_min):
          y_min=y
     if(y>y_max):
          y_max=y

     line=f.readline()

time1=time.time()


file_size=len(restaurant_list)

print("file length: ",file_size)
print("scan time :",time1-time0)

grid=[[[] for i in range(50)] for j in range(50)]
inverted_={}

x_width=x_max-x_min
y_width=y_max-y_min

x_step=x_width/grid_size### compute the x,y steps
y_step=y_width/grid_size

x_borders=[]
y_borders=[]

for i in range(grid_size):##### calculate the borders min x,y max x,y for every cell of grid table


     x_begin= x_min + i*x_step
     x_end= x_min + (i+1)*x_step

     y_begin= y_min + i*y_step
     y_end= y_min + (i+1)*y_step

  
     x_borders.append([x_begin,x_end])###save the borders of every cell in x_borders ,y_borders lists
     y_borders.append([y_begin,y_end])



         


for i in range(file_size):### fill the grid cells with restaurants

     line_array=restaurant_list[i].split("\t")
     cordinates=line_array[1].split(":")
     all_cordinates=cordinates[1].rstrip().split(",")
     
     
     for j in range(len(all_cordinates)):
          all_cordinates[j]=all_cordinates[j].strip()

     x=float(all_cordinates[0])
     y=float(all_cordinates[1])

     for j in range(grid_size-1):#### calculate which restaurants correspond in which cell

          if( x>= x_borders[j][0] and x< x_borders[j][1]):

               x_shell=j

          if( y>= y_borders[j][0] and y< y_borders[j][1]):

               y_shell=j
      
     if (float(x) >= x_borders[grid_size - 1][0] and float(x) <= x_max) :###due to round issues do separately the last case of x,y
	
          x_shell = grid_size - 1

     if (float(y) >= y_borders[grid_size - 1][0] and float(y) <=y_max) :
     
          y_shell = grid_size - 1
	

     if( i not in grid[x_shell][y_shell]):## fill in 

          grid[x_shell][y_shell].append(i)

          

def update_inverted(tags,row):### update inverted_ dict (inverted file)
     
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



####  x2,x2m,y2,y2m is query window m->max          
def isIntersected(x1,x1m,y1,y1m,x2,x2m,y2,y2m):
    if(x1m<x2 or x2m<x1):
        return False
    if(y1m<y2 or y2m<y1):
        return False
    
    return True



def spaSearchGrid(range_query): ###the spaSearchGrid serch using grid

     q_x_min=range_query[0]
     q_x_max=range_query[1]
     q_y_min=range_query[2]
     q_y_max=range_query[3]
     
     min_x=100
     min_y=100
     max_x=0
     max_x=0
     
     Grid_Result=[]
     for i in range(50):

          for j in range(50):
               
               if(len(grid[i][j])>0):### CHECK IF IS EMPTY CELL
                    
                    if( isIntersected(x_borders[i][0],x_borders[i][1],y_borders[j][0],y_borders[j][1],q_x_min,q_x_max,q_y_min,q_y_max) ):
                    
                         for r in grid[i][j]:

                              res_line=restaurant_list[r]
                              line_array=res_line.split("\t")
                              cordinates=line_array[1].split(":")
                              all_cordinates=cordinates[1].rstrip().split(",")
     
                         

                              x=float(all_cordinates[0])
                              y=float(all_cordinates[1])
                         
                              if(x>=q_x_min and x<=q_x_max):### CHECK IF THE RESTAURANT IS INSIDE QUERY WINDOW BECAUSE MAYBE ITS CELL IS BUT RESTAURANT IS NOT.
                                   if( y>=q_y_min and y<=q_y_max):
                                   
                                        Grid_Result.append(r)
                                   
     return Grid_Result
                    




def merge_join(list1,list2):### merge join to find intersection in two lists

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



def kwSpaSearchIF(complex_query):### use kwSearchIF searching by tags and then check whice rows of the result is inside the range query

     q_x_min=complex_query[0]
     q_x_max=complex_query[1]
     q_y_min=complex_query[2]
     q_y_max=complex_query[3]

     keywords=complex_query[4:]

     kwIF_Result=kwSearchIF(keywords)
     kwSpaIF_Result=[]
     for i in kwIF_Result:

          candidate_restaurant=restaurant_list[i]
          line_array=candidate_restaurant.split("\t")
          cordinates=line_array[1].split(":")
          all_cordinates=cordinates[1].rstrip().split(",")

          x=float(all_cordinates[0])
          y=float(all_cordinates[1])

          if(x>=q_x_min and x<=q_x_max):
               
               if( y>=q_y_min and y<=q_y_max):
                                   
                         kwSpaIF_Result.append(i)
                         
                         
     return kwSpaIF_Result
          
          
          
     
def kwSpaSearchGrid(complex_query):### use spaSearchGrid searching by range query window and then check whice rows of result contains all tags

     
     window_query=complex_query[:4]
     keywords=complex_query[4:]

     spaGrid_Result=spaSearchGrid(window_query)
     kwSpaGrid_Result=[]

     for i in spaGrid_Result:

          line_array=restaurant_list[i].split("\t")
          tags=line_array[2].split(":")
          all_tags=tags[1].rstrip().split(",")
          for j in range(len(all_tags)):
               all_tags[j]=all_tags[j].strip()
          

          if(set(keywords).issubset(set(all_tags))):
               
               kwSpaGrid_Result.append(i)

     return kwSpaGrid_Result

          
     





def kwSpaSearchRaw(complex_query):### read the restaurant_list row by row and take the lines that have all tags and are inside the range query window

     q_x_min=complex_query[0]
     q_x_max=complex_query[1]
     q_y_min=complex_query[2]
     q_y_max=complex_query[3]
     
     keywords=complex_query[4:]
     kwSpaRaw_Result=[]

     for i in range(len(restaurant_list)):

          line_array=restaurant_list[i].split("\t")
          tags= line_array[2].split(":")
          all_tags= tags[1].rstrip().split(",")
          for j in range(len(all_tags)):
               all_tags[j]=all_tags[j].strip()
         
          if(set(keywords).issubset(set(all_tags))):

               cordinates= line_array[1].split(":")
               all_cordinates= cordinates[1].rstrip().split(",")
               x=float(all_cordinates[0])
               y=float(all_cordinates[1])
               
               if(x>=q_x_min and x<=q_x_max):
                    if( y>=q_y_min and y<=q_y_max):

                         kwSpaRaw_Result.append(i)

                        
     return kwSpaRaw_Result


print("\n\n")#### show the results
time2=time.time()
kwSpaRaw_Result=kwSpaSearchRaw(query)
time3=time.time()
print("kwSpaSearchRaw:",len(kwSpaRaw_Result)," results, cost =",time3-time2 ,"seconds")
for i in kwSpaRaw_Result:
     print(restaurant_list[i])

print("\n\n")
time4=time.time()
kwSpaIF_Result=kwSpaSearchIF(query)
time5=time.time()
print("kwSpaSearchIF:",len(kwSpaIF_Result)," results, cost =",time5-time4 ,"seconds")
for i in kwSpaIF_Result:
     print(restaurant_list[i])

print("\n\n")
time6=time.time()
kwSpaGrid_Result=kwSpaSearchGrid(query)
time7=time.time()
print("kwSpaSearchGrid:",len(kwSpaGrid_Result)," results, cost =",time7-time6 ,"seconds")
for i in kwSpaGrid_Result:
     print(restaurant_list[i])


     















