#from ast import arg
import sys;
import re;
import math;

def intersect(a,b,c,d):
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    x4, y4 = d
    # We represent line between a and b as A1x + B1y = C1
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1
    # Similarly , We represent line between c and d as A2x + B2y = C2
    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3

    det = A1* B2 - A2* B1

    if det == 0:
        return None
    else:
        x = (B2*C1 - B1*C2) / det
        y = (A1*C2 - A2*C1) / det
    
    ## Checking that x, y lies on first line segment:
    x_present_1 = (min(x1,x2) <= x <= max(x1,x2))
    y_present_1 = (min(y1,y2) <= y <= max(y1,y2))

    ## Checking that x, y lies on second line segment:
    x_present_2 = (min(x3,x4) <= x <= max(x3,x4))
    y_present_2 = (min(y3,y4) <= y <= max(y3,y4))

    if (x_present_1 and y_present_1 and x_present_2 and y_present_2):
        return (round(x,2),round(y,2))
    else:
        return None

def distance(a,b):
    x1,y1 = a
    x2, y2 = b
    return math.sqrt((y2-y1)**2 + (x2-x1)**2)



class GraphPrinter :
     # input : Graph (Edges + Vertices)
     # output : A graph in the Output format
    def __init__(self,graph):
         self.print_vertices(graph.vertices)
         self.print_edges(graph.edges)

    def print_vertices(self, vertices):
        print("V = {")
        for key, value in vertices.items():
            #my_arr = value
            #v_id = my_arr[6:]
            #print(key)
            print(' ',value,':',"  ({:.2f},{:.2f})".format(*key), sep='')
        # print ('\n'.join('\t{} : ({:.2f},{:.2f})'.format(value,*key) for key,value in vertices.items()))
        print("}")

    def print_edges(self, edges):
        print("E = {")

        
        if(len(edges)):
            print(',\n'.join(' <{},{}>'.format(v_1,v_2) for v_1,v_2 in edges))
            
        elif(len(edges) == ''):
            print('')
            #if(v1 == ' ' and v2== ' ' ):
            #    print('Empty')
        #//for v1, v2 in edges:
        #//    v_1 = v1[6:]
        #//    v_2 = v2[6:]
            # print(v_1)
            # print(v_2)
            #v_1 = int(v_1)
            #v_1 = int(v_1)
            #v_1 = round(v_1,2)
            #v_2 = round(v_2,2)
        #//    print('','<'+v_1+','+v_2+'>')
        # print(',\n'.join('\t<{},{}>'.format(v1,v2) for v1,v2 in edges))
        print("}")



class GraphGenerator :
    # input : Street database 
    # output : Graph (Edges + Vertices) 
    def __init__(self, street_db):
        # Grouping vertices in the graph
        self.vertices = set()
        for str in street_db:
            for ver in street_db[str]:
                self.vertices.add(ver)
        # Vertax map
        self.vertax_map = {}
        self.inverse_vertax_map = {}
        vertax_id = 1
        for vertax in self.vertices:
            self.vertax_map[vertax] = "{0}".format(vertax_id)
            self.inverse_vertax_map["{0}".format(vertax_id)] = vertax
            vertax_id += 1

        # Create a map from all line segment in the street database
        self.line_segment = {}
        self.inv_line_segment = {}
        line_segment_id = 1
        for street in street_db:
            str_point = street_db[street]
            ## Pending
            for i in range(len(str_point) - 1):
                p_1 = str_point[i]
                p_2 = str_point[i+1]
                id = "Line Segment{0}".format(line_segment_id)
                self.line_segment[(self.vertax_map[p_1],self.vertax_map[p_2])] = id
                self.inv_line_segment[id] = (self.vertax_map[p_1], self.vertax_map[p_2])
                line_segment_id += 1

        street_list = list(street_db.keys())
        n_street = len(street_list)
        street_pair = []

        # Creating all pairs for streets    
        for i in range(n_street - 1) :
            j = i + 1
            while( j < n_street):
                street_pair.append((street_list[i], street_list[j]))
                j += 1
        self.new_edges = set()
        graph_vertax_array = []
        intersection_points = {}

        #Finding intersectins in 2 different streets
        for s1, s2 in street_pair:
            s1_points =  street_db[s1]
            s2_points = street_db[s2]
            for i1 in range(len(s1_points)-1):
                p_1 = s1_points[i1]
                p_2 = s1_points[i1 + 1]
                for i2 in range(len(s2_points)-1):
                    p_3 = s2_points[i2]
                    p_4 = s2_points[i2 + 1]   
                    intersection_point = intersect(p_1, p_2, p_3, p_4)
                    if intersection_point :
                        # Adding intersection points in vertex list
                        # Pending
                        for vertax in [p_1, p_2, p_3, p_4, intersection_point]:
                            graph_vertax_array.append(vertax)
                        if vertax not in self.vertax_map :
                            self.vertax_map[vertax] = "{0}".format(vertax_id)
                            vertax_id += 1
                        # If intersection point is line segment's endpoint it should be remove
                        if vertax == intersection_point:
                            first_ls = self.line_segment[self.vertax_map[p_1],self.vertax_map[p_2]]
                            second_ls = self.line_segment[self.vertax_map[p_3],self.vertax_map[p_4]]
                            if vertax not in intersection_points:
                                intersection_points[vertax] = [first_ls, second_ls]
                            else:
                                intersection_points[vertax] += [first_ls, second_ls]

        for point in intersection_points:
            intersection_points[point] = set(intersection_points[point])

        # Creating an edge  at each intersection 
        for point in intersection_points:
            line_seg = list(intersection_points[point])
            for ls in line_seg:
                point1,point2 = self.inv_line_segment[ls]
                if point1 != self.vertax_map[point] and (self.vertax_map[point],point1) not in self.new_edges:
                    self.new_edges.add((point1,self.vertax_map[point]))
                if point2 != self.vertax_map[point] and (point2,self.vertax_map[point]) not in self.new_edges:
                    self.new_edges.add((self.vertax_map[point],point2))                  

        # Here Graph vertax_array contains vertax of graph
        self.new_vertices = {}
        for vertax in graph_vertax_array:
            self.new_vertices[vertax] = self.vertax_map[vertax]


        # Used dictionary to track intersection points of line segments.
        # Key is line segment and value is intersection point for that perticular line segment 
        lsegment_int_point = {}
        for segment in self.inv_line_segment:
                lsegment_int_point[segment] = []
                for point in intersection_points:
                    if segment in intersection_points[point]:
                        lsegment_int_point[segment].append(point)

        for segment in lsegment_int_point:
            p1,p2 = self.inv_line_segment[segment]
            # Sorting points of line segment according to distance from point 1 
            if len(lsegment_int_point[segment]) > 1:
                point = lsegment_int_point[segment]
                # print(point)
                # print(self.inverse_vertax_map[p1])
                # print(self.inverse_vertax_map[p2])
                # Created int_point1_sort which ontains intersection points sorted in the increasing order of distance from point1
                int_point1_sort = sorted(point, key = lambda pt : distance(self.inverse_vertax_map[p1],pt))
                for pnt in int_point1_sort:
                    if (p1 != self.vertax_map[pnt] and ((p1, self.vertax_map[pnt]) in self.new_edges)):
                        self.new_edges.remove((p1,self.vertax_map[pnt]))
                    if (p2 != self.vertax_map[pnt] and ((self.vertax_map[pnt], p2) in self.new_edges)):
                        self.new_edges.remove((self.vertax_map[pnt],p2))                
                # Adding new edges in final graph 
                if (p1 != self.vertax_map[int_point1_sort[0]] and (self.vertax_map[int_point1_sort[0]],p1) not in self.new_edges):
                    self.new_edges.add((p1,self.vertax_map[int_point1_sort[0]]))
                if (p2 != self.vertax_map[int_point1_sort[-1]] and (p2, self.vertax_map[int_point1_sort[-1]]) not in self.new_edges):
                    self.new_edges.add((self.vertax_map[int_point1_sort[-1]], p2))

                for i in range(0, len(int_point1_sort) - 1):
                    point_1 = int_point1_sort[i]
                    point_2 = int_point1_sort[i+1]
                    if ((self.vertax_map[point_2],self.vertax_map[point_1]) not in self.new_edges):
                        self.new_edges.add((self.vertax_map[point_1], self.vertax_map[point_2]))                             


class Graph :
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

class StreetDataBase :
    def __init__(self):
        self.streets = {}

    def add_street(self, street_name, vertices):
        self.streets[street_name] = vertices

    def delete_street(self, street_name):
        del self.streets[street_name]

    def change_street(self, street_name , vertices):
        if(street_name in self.streets):
            self.streets[street_name] = vertices


class CommandParser:
    def __init__(self):
            self.commands = {'add' : "Add a street", 'mod' : "Modify a street" , 'rm': "Remove a street", "gg": "Generate Graph"}

    def valid_parenthesis(self, string):
        stack = []
        for char in str(string):
            if(char == '('):
                #if(not char.isspace()):
                #    Exception("Error: Spaces in parenthesis not supported")  
                stack.append(char)
            elif(char == ')'):
                if(len(stack)>0):
                    stack.pop()
                else:
                    return False
        return (len(stack) == 0)


    def parse_cmd(self, input_str):

        try:
            arg = input_str.split()
            # print(arg[2])
            street_name = ""
            exception = False
            street_vertices = []
            vertices = []
            command = arg[0]
            street_name_part = []
            # print(street_db.streets.keys())
            if command == 'add' or command == 'mod':
                #print("Adding or changing street")
                street_name_part = re.findall(r"[a-z]+\s+\"([a-zA-Z ]+)\"\s+", input_str)
                if '+' in input_str:
                    raise Exception("Error: '+' Command not supported")
                if '- ' in input_str:
                    raise Exception("Error: Spacing after '-'  not supported")

                #print(street_name_part)
                #print(len(street_name_part))

            elif command == 'rm':
                #print("Removing")
                street_name_part = re.findall(r"\s+\"([a-zA-Z ]+)\"", input_str)


            if command not in self.commands:
                exception = True
                raise Exception("Incorrect input format")

            else:
                if command != 'gg':
                    if len(street_name_part) == 1:
                            street_name = street_name_part[0].lower()
                            vertices_part = input_str.split('"')[2].strip()
                            # print(vertices_part)
                            if(self.valid_parenthesis(vertices_part)):

                                vertices = re.findall(r'\(.*?\)', vertices_part)
                                # print(vertices)
                                # If spacing in coordinates are not allowed then uncomment below
                                #for i in vertices:
                                
                                #    if( (' ' in i) == True ):
                                #        raise Exception("Error: Spaces in cordinates not supported")

                                street_vertices = [eval(point) for point in vertices]
                                # print(street_vertices)


                    else:
                        if command == 'add':
                            exception = True
                            raise Exception("Invalid input for 'add' command")
                        else:
                            exception = True
                            raise Exception("Too few arguments for 'add' command")

                    if command != 'add' and street_name not in street_db.streets.keys():
                        exception = True
                        raise Exception("'mod' or 'rm' specified for a street that does not exist")

                    if command == 'add':
                        if street_name in street_db.streets.keys():
                            exception = True
                            raise Exception("'add' command specified for already existing street")

                    if (command == 'add' or command == 'mod') and len(street_vertices) < 2:
                        exception = True
                        raise Exception("Too few points for a street")

                    if command == 'rm' and (len(street_name_part) > 1 or len(street_vertices) > 0 or len(vertices_part) != 0):
                        exception = True
                        raise Exception("Too many arguements for 'rm' command")

                else:
                    if (len(street_name_part) > 0 or len(street_vertices) > 0 or len(input_str.split(" ")) > 1):
                        exception = True
                        raise Exception("Too many arguements")
    

        except SyntaxError as e:
            print('Error: Please enter a valid input',)

            #street_name = arg[1]
            #street_vertices = arg[2]
            # print(street_name);

        except Exception as e:
            print('Error: ' + str(e))

        finally:
            return {                   
                    "command" : command,
                    "street_name" : street_name,
                    "street_vertices" : street_vertices,
                    "exception" : exception                   
                    
                }

            

cmdparser = CommandParser()
street_db = StreetDataBase()

def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.

    ### make sure to remove all spurious print statements as required

    ### by the assignment
    init_streets = {}
    streets = {}

    while True:
        try:
            cmd = input().lower()
            if (cmd == ''):
                raise Exception("Error: Empty Command not supported")
                
            parse = cmdparser.parse_cmd(cmd)  # python3 input


            if not parse['exception']:
                command = parse['command']
                street_name = parse['street_name']
                street_vertices = parse['street_vertices']
                if (command in cmdparser.commands):
                    if command == 'add':
                        street_db.add_street(street_name, street_vertices)
                    elif command == 'rm':
                        street_db.delete_street(street_name)
                    elif command == 'mod':
                        street_db.change_street(street_name, street_vertices)
                    elif command == 'gg':
                        # print("Under construction")
                        graph_generator = GraphGenerator(street_db.streets)
                        graph = Graph(graph_generator.new_vertices, graph_generator.new_edges)
                        GraphPrinter(graph)
                        # print(street_db)

            # key = get_streetname(command)
            #parsed_cmd = cmd_parser.parse_command(cmd)
            # if cmd == '':
            #    break
        # return exit code 0 on successful termination
        except EOFError:
            #print('Error: End Of File exception')
            sys.exit(0)

        except KeyboardInterrupt:
            #print('Error: keyboard interrupt exception')
            sys.exit(0)

        except Exception as e:
            print('Error: ' + str(e))



if __name__ == '__main__':
    main()


# add "Weber" (2,-1) (2,2) (5,5) (5,6) (3,8)
# add "King" (4,-2) (4,8)
# add "Davenport" (1,4) (5,8)
# gg
# mod "Weber" (2,1) (2,2)
# gg
# rm "King"
# gg