import time
import sys
import math
#### GIANNIS MPARZAS 2765
query=[]
for i in range(1,len(sys.argv)):### take user's cordinates and put them in query list
     query.append(float(sys.argv[i]))

print("the input cordinates are:",query)
time0=time.time()
f=open('Restaurants_London_England.tsv','r+')
restaurant_list=[]

x_min=1000
y_min=1000
x_max=0
y_max=0
grid_size=50###set grid size

line=f.readline()
while(line):###save the file in restaurant_list and find the min x,y max x,y
          ### to set the x,y steps in grid 

     restaurant_list.append(line)
     
     line_array=line.split("\t")
     cordinates=line_array[1].split(":")
     all_cordinates=cordinates[1].rstrip().split(",")
     
     for j in range(len(all_cordinates)):
          all_cordinates[j]=all_cordinates[j].strip()

     x=float(all_cordinates[0])
     y=float(all_cordinates[1])
     
     if(x<x_min):
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


x_width=x_max-x_min
y_width=y_max-y_min

x_step=x_width/grid_size### compute the x,y steps
y_step=y_width/grid_size

x_borders=[]
y_borders=[]

for i in range(grid_size):### calculate the borders min x,y max x,y for every cell of grid table
               
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

print(grid[5][36])

#######  x2,x2m,y2,y2m is query window m->max          
def isIntersected(x1,x1m,y1,y1m,x2,x2m,y2,y2m):### intersection condition
    if(x1m<x2 or x2m<x1):
        return False
    if(y1m<y2 or y2m<y1):
        return False
    
    return True



def spaSearchGrid(range_query):### the spaSearchGrid search using the grid table

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
                    
                    if( isIntersected(x_borders[i][0],x_borders[i][1],y_borders[j][0],y_borders[j][1],q_x_min,q_x_max,q_y_min,q_y_max) ):### CHECK INTERSECTION MEANS POSSIBLY MATCH
                    
                         for r in grid[i][j]:

                              res_line=restaurant_list[r]
                              line_array=res_line.split("\t")
                              cordinates=line_array[1].split(":")
                              all_cordinates=cordinates[1].rstrip().split(",")
     
                         

                              x=float(all_cordinates[0])
                              y=float(all_cordinates[1])
                         
                              if(x>=q_x_min and x<=q_x_max): ### CHECK IF THE RESTAURANT IS INSIDE QUERY WINDOW BECAUSE MAYBE ITS CELL IS BUT RESTAURANT IS NOT.
                                   
                                   if( y>=q_y_min and y<=q_y_max):
                                   
                                        Grid_Result.append(r)
                                   
     return Grid_Result
                    
          
def spaSearchRaw(range_query):### the spaSearchRaw search scanning restaurant_list raw by raw

     q_x_min=range_query[0]
     q_x_max=range_query[1]
     q_y_min=range_query[2]
     q_y_max=range_query[3]
     Raw_Result=[]
     for i in range(file_size):

          res_line=restaurant_list[i]
          line_array=res_line.split("\t")
          cordinates=line_array[1].split(":")
          all_cordinates=cordinates[1].rstrip().split(",")
     
                         

          x=float(all_cordinates[0])
          y=float(all_cordinates[1])
                         
          if(x>=q_x_min and x<=q_x_max):
               if( y>=q_y_min and y<=q_y_max):
                                   
                         Raw_Result.append(i)
     return Raw_Result

          
          

print("bounds:",x_min,x_max,y_min,y_max)
print("widths:",x_max-x_min,y_max-y_min)
for i in range(50):
     for j in range(50):

          if(len(grid[i][j])>0):
               print(i,j,len(grid[i][j]))
          

time2=time.time()
          
Grid_Result=spaSearchGrid(query)

time3=time.time()### SHOW RESULTS


print("spaSearchGrid:",len(Grid_Result),"results, cost =", time3-time2 ,"seconds")
for i in Grid_Result:
     print(restaurant_list[i])




time4=time.time()
          
raw_Result=spaSearchRaw(query)

time5=time.time()
print("\n\n")

print("spaSearchRaw:",len(raw_Result),"results, cost =", time5-time4 ,"seconds")

for i in raw_Result:
     print(restaurant_list[i])




          

























