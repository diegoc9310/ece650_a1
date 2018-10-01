import sys
import re

# YOUR CODE GOES HERE
class Line(object):
    def __init__ (self, src, dst):
        self.src = src
        self.dst = dst

    def __str__(self):
        return str(round(self.src.index, 2)) + '-->' + str(round(self.dst.index, 2))

class Point(object):
    def __init__ (self, x, y,name):
        self.x = float(x)
        self.y = float(y)
        self.name = str(name)
        self.index = float((((self.x+self.y)*(self.x+self.y+1))/2)+self.y)
    def __str__ (self):
        return str(round(self.index, 2))+':  '+'(' + str(round(self.x,2)) + ',' + str(round(self.y,2))+ ')'

class Distance(object):
    def __init__(self, index, distance):
        self.index = index
        self.distance = distance

    @classmethod
    def sort_key(cls, key):
        if key == 'distance':
            return lambda obj: obj.distance
        elif key == 'index':
            return lambda obj: obj.index


def out_of_range(x1, y1, x2, y2, x3, y3, x4, y4, xcoor, ycoor,name,test):
    xbig    = first_bigger_second(x1,x2)
    ybig    = first_bigger_second(y1,y2)
    xbig2   = first_bigger_second(x3,x4)
    ybig2   = first_bigger_second(y3,y4)
    xsmall  = first_smaller_second(x1,x2)
    ysmall  = first_smaller_second(y1,y2)
    xsmall2 = first_smaller_second(x3,x4)
    ysmall2 = first_smaller_second(y3,y4)

    if (xcoor>xbig) or (xcoor<xsmall) or (xcoor>xbig2) or (xcoor<xsmall2) :
      return False

    if (ycoor>ybig) or (ycoor<ysmall) or (ycoor>ybig2) or (ycoor<ysmall2) :
      return False

    return Point(xcoor, ycoor, name)
  
def intersect (l1, l2):
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y

    xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
    xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
    yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)

    if (xden != 0) & (yden != 0):
      xcoor =  xnum / xden
      ycoor =  ynum / yden
    else:
      return False

    return out_of_range(x1, y1, x2, y2, x3, y3, x4, y4, xcoor, ycoor,"intersect",0)

def first_bigger_second ( first,  second):
  if (first >= second):
    return first;
  if (first < second):
    return second

def first_smaller_second ( first,  second):
  if (first >= second):
    return second;
  if (first < second):
    return first

def cross_product(p1, p2, p3):        
  x1 = p3.x - p1.x;
  y1 = p3.y - p1.y;

  x2 = p2.x - p1.x;
  y2 = p2.y - p1.y;
  cross = x1 * y2 - y1 * x2;

  if cross ==0:
    xbig    = first_bigger_second(p1.x,p2.x)
    ybig    = first_bigger_second(p1.y,p2.y)
    xsmall  = first_smaller_second(p1.x,p2.x)
    ysmall  = first_smaller_second(p1.y,p2.y)
    if (p3.x>xbig) or (p3.x<xsmall)  :
      return False
    if (p3.y>ybig) or (p3.y<ysmall) :
      return False
    else:
      return p3
  else:
    return False

##########################################
# Search Street Name
# Returns True if name foun false if not
# parameter: List of lists of point objects 
#########################################
def search_street_name(street_list,street_name):
  new_street="False"
  for i in range(0,(len(street_list))):
    if street_name.lower()==street_list[i][0].name.lower():
      new_street=i
  return new_street

##########################################
# COMMAND PARSER MODULE
# a->Add c->Change r->Remove g->Graph
# parser state 9 Represents that an 
# appropiate command has been recieved
# parameter: String input
#########################################
###########PARSER STATE MACHINE###########
def Parser(line):
    parser_state=0
    test_points=[]
    name=""
    sign_flag=0
    number_flag=0
    space_flag=0
    pointx=""
    pointy=""
    command=0
    point_list=[]
    for len_input in range(0,len(line),1):  
#########State 0#########
      if parser_state==0:
        x=line[len_input]
        if x ==" ":
          pass
        elif x.isalpha():
          if x=="a" or x=="c":
            command=x            
            parser_state=1
          elif x=="r":
            command=x
            parser_state=11
          elif x=="g":
            command=x        
            if len_input==len(line)-2:
              parser_state=9
            else:
             parser_state=14 ## This state is shared between graph and remove command
          else:
            print 'Error: Command not recognized'
            break 

        else:
          print 'Error: Command not recognized'
          break         
########ADD/CHANGE COMMAND########
###State 1###
      elif parser_state==1:
        if line[len_input]==" ":
          parser_state=2
        else:
          if len_input==len(line)-1:
            print 'Error: Missing required arguments'
          else:
            print 'Error: Add a space between command and arguments'
          break
###State 2###
      elif parser_state==2:
        if line[len_input]==" ":
          pass
        elif line[len_input]=='"':
          parser_state=3 ##Go Next
          name=""
        else:
          print 'Incorrect street name argument format use: "Street Name"'
          break
###State 3###
      elif parser_state==3:
        x=line[len_input]
        if x.isalpha():
          name+=line[len_input]
        elif x.isdigit():
          print 'Error: Do not enter numbers or special characters in Street Name'
          break
        elif line[len_input]!='"' and line[len_input]!=' ':
          print 'Error: Do not enter numbers or special characters in Street Name'
          break
        elif line[len_input]=='"':
          if len(name)>=1:
            parser_state=4##Go Next
          else:
            print 'Error: Name not found'
            break
        elif line[len_input]==" ":
          name+=line[len_input] 
        else:
          print 'Error: Do not enter numbers or special characters in Street Name'
          break
###State 4###
      elif parser_state==4:
        
        if line[len_input]==" ":
          parser_state=5
        else:
          print'Error: Space nedded between "Name" argument and coordinates (x,y)'
          break
###State 5###
      elif parser_state==5:
        if line[len_input]==" ":
          pass
        elif line[len_input]=="(":
          parser_state=6 ##Go Next
        else:
          print 'Error: coordinates need to be inside (x,y)'
          break
###State 6###

      elif parser_state==6:
        if line[len_input]==" ":
          if number_flag==1 or sign_flag==1:
           space_flag=1
          else:
            pass
        elif line[len_input]=="-":
          if sign_flag==0 and space_flag==0:
            pointx+=line[len_input]
            sign_flag=1
          else:
            print 'Error: wrong coordinate format'
            break
        elif line[len_input].isdigit():
          if space_flag==0:
            pointx+=line[len_input] 
            number_flag=1
            sign_flag=1
          else:
            print 'Error: wrong coordinate format'
            break
        elif line[len_input]==",":
          parser_state=7
          sign_flag=0
          space_flag=0
          number_flag=0
        else:
          print 'Error: wrong coordinate format'
          break
###State 7###
      elif parser_state==7:
        if line[len_input]==" ":
          if number_flag==1 or sign_flag==1:
           space_flag=1
          else:
            pass
        elif len_input==len(line)-2:
          if line[len_input]==")":
            test_points.append('('+str(pointx)+','+str(pointy)+')')
            pointx=""
            pointy=""
            parser_state=9
          else:
            print 'Error: wrong coordinate format'
            break
        else:
          if line[len_input]=="-":
            if sign_flag==0:
              pointy+=line[len_input]
              sign_flag=1
            else:
              print 'Error: wrong coordinate format'
              break
          elif line[len_input].isdigit():
            if space_flag==0:
              pointy+=line[len_input] 
              number_flag=1
              sign_flag=1
            else:
              print 'Error: wrong coordinate format'
              break
          elif line[len_input]==")":
            parser_state=8
            test_points.append('('+str(pointx)+','+str(pointy)+')')
            pointx=""
            pointy=""
            sign_flag=0

          else:
            print 'Error: wrong coordinate format'
            break
###State 8###  
      elif parser_state==8:
        if len_input==len(line)-2:
          if line[len_input]==" ":
             parser_state=9
          else:
            'Error: Wrong coordinate format'
        else:
          if line[len_input]==" ":
            pass
          elif line[len_input]=="(":
            if len_input!=len(line)-1:
              parser_state=6
              sign_flag=0
              space_flag=0
              number_flag=0
          else: 
            print 'Error: Wrong coordinate format'
            break
######ADD/CHANGE COMMAND END######
##########REMOVE COMMAND##########
###State 11###
      elif parser_state==11:
        if line[len_input]==" ":
          parser_state=12
        else:
          if len_input==len(line)-1:
            print 'Error: required "Name" argument'
          else:
            print 'Error: required space separation between command and argument'
          break
###State 12###
      elif parser_state==12:
        if line[len_input]==" ":
          pass
        elif line[len_input]=='"':
          parser_state=13 ##Go Next
          name=""
        else:
          print 'Error: required "Name" argument'
          break
###State 13###
      elif parser_state==13:
        x=line[len_input]
        if x.isalpha():
          name+=line[len_input]
        elif x.isdigit():
          print 'Error: Do not enter numbers or special characters in Street Name'
          break
        elif line[len_input]!='"' and line[len_input]!=' ':
          print 'Error: Do not enter numbers or special characters in Street Name'
          break
        elif line[len_input]=='"':
          if len_input==len(line)-2:
            if len(name)>=1:
              parser_state=9##Go Next
            
            else:
              print 'Error: Name not found'
              break

          elif len(name)>=1:
            parser_state=14##Go Next
          else:
            print 'Error: Name not found'
            break

        elif line[len_input]==" ":
          name+=line[len_input] 
        else:
          print 'Error: Do not enter numbers or special characters in Street Name'
          break
###State 14###
      elif parser_state==14:
        error_flag=0
        for a in range(len_input,len(line)-1,1):
          if line[a]==" ":
            pass
          else:
            error_flag=1
        if error_flag==0:
          parser_state=9
          break
        else:
          if command=='r':
            print'Error: Wrong command format'
          elif command=='g':
            if line[len_input]!=" ":
              print 'Error: Wrong command format'
            else:
              print'Error: Command recieves no arguments'
          else:
            print 'Error: Wrong command format'
          break
########REMOVE COMMAND END########
#########PARSER STATE MACHINE END#########
    if parser_state==9:
      for i in xrange(0,len(test_points),1):
        points = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", test_points[i])
        p=Point(points[0],points[1],name)
        point_list.append(p)
      return command,name,point_list
    else:
      print "error_code[",parser_state,"]"
      return False

##########################################
# GRAPHING MODULE
# Computes and prints Edges and vertexes
# parameter: List of List of Street points
#########################################
def graph_calculator(street_list):
  delete_list=[]
  intercept_list=[]
  point_intercept_list=[]
  street_intercept_list=[]
  intercept_found=False
  point_test=0
  dist_list=[]
  edge_list=[]
  sorted_street_list=[]
  vertex_list=[]

  for i in xrange(0,(len(street_list))):
    x= len(street_list[i])-1
    for j in xrange(0,x,1):
      for k in xrange(0,len(street_list)):
        if k!=i:
          for l in xrange(0,(len(street_list[k])-1)):
            line_1=Line(street_list[i][j],street_list[i][j+1])
            line_2=Line(street_list[k][l],street_list[k][l+1])
            point_test= intersect(line_1, line_2)
            if point_test!= False:
              intercept_found=True
              if(len(intercept_list)>0):
                for a in range(0,(len(intercept_list))):
                  if (intercept_list[a].x!=point_test.x) or (intercept_list[a].y!=point_test.y):
                    intercept_list.append(point_test)

              else:
                intercept_list.append(point_test)
            else:
              p1=cross_product(street_list[i][j],street_list[i][j+1],street_list[k][l])
              if p1!= False:
                intercept_found=True
                intercept_list.append(street_list[k][l])
                point_test=True
              p2=cross_product(street_list[i][j],street_list[i][j+1],street_list[k][l+1])
              if p2!= False:
                intercept_found=True
                street_list[k][l+1].name="intersect"
                intercept_list.append(street_list[k][l+1])
                point_test=True
        if point_test!= False:
              
          point_intercept_list.append( street_list[i][j]  )       
          for z in range(0,(len(intercept_list))):
            point_intercept_list.append(intercept_list[z])
          point_intercept_list.append(  street_list[i][j+1] )
          intercept_list[:]=[]
          point_test=0
    if intercept_found==True:
      street_intercept_list.append(point_intercept_list[:])
      intercept_found=False
    point_intercept_list[:]=[]
          
#find index of repeated values in the streets and delete them 
  for x in range(0,(len(street_intercept_list))):
    delete_list[:]=[]
    for a in range(0,(len(street_intercept_list[x]))):
      for b in range(1+a,(len(street_intercept_list[x]))):
        if (street_intercept_list[x][a].x==street_intercept_list[x][b].x) and(street_intercept_list[x][a].y==street_intercept_list[x][b].y):
          if b not in delete_list:
            delete_list.append(b)
    delete_list = sorted(delete_list)
    for i in xrange(0,(len(delete_list))):
      de= delete_list[i]-i
      del street_intercept_list[x][de]

#Order street values by distance from starting point 
  for t in range(0,(len(street_intercept_list))):
    sorted_line_list=[]
    dist_list[:]=[]
    for a in range(1,(len(street_intercept_list[t]))):
      xdif = street_intercept_list[t][a].x-street_intercept_list[t][0].x
      ydif = street_intercept_list[t][a].y-street_intercept_list[t][0].y
      new1= ((xdif*xdif)+(ydif*ydif))**(.5)
      dist_list.append(Distance(a,new1))
    dist_list.sort(key=Distance.sort_key('distance'))
    sorted_line_list.append(street_intercept_list[t][0])
    for a in range(0,(len(dist_list))):
      x=dist_list[a].index
      sorted_line_list.append(street_intercept_list[t][x])
    sorted_street_list.append(sorted_line_list[:])
        
#Generate Edge List from ordered List   
  for a in range(0,(len(sorted_street_list))):
    for b in range(0,(len(sorted_street_list[a])-1)):
      if sorted_street_list[a][b].name==sorted_street_list[a][b+1].name:
        if sorted_street_list[a][b].name!="intersect":
          pass ## no intercept not considered edge
        else:
          edge_list.append(Line(sorted_street_list[a][b], sorted_street_list[a][b+1]))
      else:
        edge_list.append(Line(sorted_street_list[a][b], sorted_street_list[a][b+1]))
      
#Save all Vertexes from edge list before filtering
  for a in range(0,(len(edge_list))):
    vertex_list.append(edge_list[a].src)
    vertex_list.append(edge_list[a].dst)

#Find index of repeated Vertexes
  delete_list[:]=[]
  for a in range(0,(len(vertex_list))):
    for b in range(1+a,(len(vertex_list))):
      if (vertex_list[a].x==vertex_list[b].x) and(vertex_list[a].y==vertex_list[b].y):
        if b not in delete_list:
          delete_list.append(b)
  delete_list = sorted(delete_list)
#Delete repeated Vertexes 
  for i in xrange(0,(len(delete_list))):
    de= delete_list[i]-i
    del vertex_list[de]
      
#Print Graph 
  print 'V = {'   
  for i in xrange(0,(len(vertex_list))):
    print vertex_list[i]      
  print'}'
  print 'E = {'
  for i in xrange(0,(len(edge_list))):
    print edge_list[i]  
  print'}'



def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
  point_list=[]
  street_list=[]
  while True:
    line = sys.stdin.readline()
    input_data=Parser(line)
    if input_data!=False:

########Extract Input Data########
      input_data=list(input_data)
      command = input_data[0]
      street_name = input_data[1]
      point_list = input_data[2][:]

########Add Command Interpretation########
      if command=='a':

        if len(street_list)>=1:
          name_found=search_street_name(street_list,street_name)
          if name_found=="False":
            if len(point_list)>1:
              street_list.append(point_list[:])
              print "Street successfully added"
            else:
              print "Error: Streets need to contain at least two point coordinates"
          else:
            print "Error: this street has all ready been registered to change it use the c command"
        else:
          if len(point_list)>1:
            street_list.append(point_list[:])
            print "Street successfully added"
          else:
            print "Error: Streets need to contain at least two point coordinates"


########Change Command Interpretation#####
      elif command=='c':
        if len(street_list)>=1:
          name_found=search_street_name(street_list,street_name)
          if name_found=="False":
            print "Error: Street not found"
          else:
            if len(point_list)>1:
              del street_list[name_found]
              street_list.append(point_list[:])
              print "Street successfully changed"
            else:
              print "Error: Streets need to contain at least two point coordinates"
        else:
          print "Error: currently there are no added Streets"


########Remove Command Interpretation#####
      elif command=='r':
        if len(street_list)>=1:
          name_found=search_street_name(street_list,street_name)
          if name_found=="False":
            print "Error: Street not found"
          else:
            del street_list[name_found]
            print "Street successfully removed"
        else:
          print "Error: currently there are no added Streets"
        pass

########Graph Command Interpretation######
      elif command=='g':
        if len(street_list)>=1:
          graph_calculator(street_list)
        else:
          print "Error: currently there are no added Streets"
   
  
    for i in xrange(0,len(street_list),1):
      for j in xrange(0,len(street_list[i]),1):
        print street_list[i][j]
  sys.exit(0)

if __name__ == '__main__':
  while True:
    main()
