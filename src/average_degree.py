import json
from datetime import *

#Adjacency matrix format
#adj_mat[0] = node1
#adj_mat[0][0] = node1 tweet hashtag
#adj_mat[0][1] = list of adjacent hashtags and connecting time info [("Bernie",time1),("Trump",time2)]
#adj_mat[0][1][0] = node first adjacent hashtag list ["Bernie",time1]
#adj_mat[0][1][0][0] = node's first adjacent hashtag "Bernie"
#adj_mat[0][1][0][1] = node's first adjacent hashtag's time time1

global adj_mat
adj_mat = []

def calculate_avg_deg():
    if len(adj_mat) == 0:
        return 0
    degree_sum = 0
    for nodes in adj_mat:
        degree_sum = degree_sum + len(nodes[1])
    return round(degree_sum / len(adj_mat), 3)
        

def get_current_adj_hashtags(hashtag):
    adj_list = []
    for node in range(len(adj_mat)):
        for adjacent_hashtags in adj_mat[node][1]:
            if adjacent_hashtags[0] == hashtag and not adjacent_hashtags[0] in adj_list:
                adj_list.append(adj_mat[node][0]) # Add the node's hashtag that holds the searched hashtag
    return adj_list

def hashtag_in_graph(hashtag):
    for nodes in range(len(adj_mat)):
            if adj_mat[nodes][0] == hashtag:
                return [True,nodes] #return location in adjacency matrix
    return [False,0]

def convert_tweet_info(omit_ht, tweet_info):
    new_format = []
    for hashtags in tweet_info[0]:
        if hashtags != omit_ht:
            new_format.append([hashtags,tweet_info[1]])
    return new_format
    

def update_tweet_hashtag(new_hashtag, tweet_info):
    hashtag_edges = convert_tweet_info(new_hashtag, tweet_info)
    # if the hashtag isnt a node in the graph, add it
    if not hashtag_in_graph(new_hashtag)[0]:  
        adj_mat.append([new_hashtag,hashtag_edges])
    time = hashtag_edges[0][1]
    # update the nodes corresponding to the new hashtag's edges
    for hts in hashtag_edges:
            #if they are a node add the new hashtag
            in_graph = hashtag_in_graph(hts[0])[0]
            node = hashtag_in_graph(hts[0])[1]
            if in_graph:
                update_node(node,new_hashtag,tweet_info,time)

def has_edge(node,edge_ht):
    for edges in range(len(adj_mat[node][1])):
        if adj_mat[node][1][edges][0] == edge_ht:
            return [True,edges] # return the location of the edge in the node's hashtag-time list
    return [False,0]

def update_edge(node,edge_location,new_time):
    adj_mat[node][1][edge_location][1] = new_time
        

# check if hashtag is in node's adj_hashtags and add/update it
def update_node(node,hashtag,tweet_info,time):
    adj_hts = convert_tweet_info(hashtag,tweet_info)
    has_edge_bool = has_edge(node,hashtag)
    if has_edge(node,hashtag)[0] :
        edge_location = has_edge(node,hashtag)[1]
        if time > adj_mat[node][1][edge_location][1]:
            update_edge(node,edge_location,time)
        elif time == adj_mat[node][1][edge_location][1]:
            pass
    else:
        adj_mat[node][1].append([hashtag,time])
        
# delete edges in the list edge_list
def delete_edges(node,edge_list):
    for hashtag_and_time in edge_list:
        adj_mat[node][1].remove(hashtag_and_time)
        
# delete nodes at the indices of node_list                              
def delete_nodes(node_list):
    for node in node_list:
        adj_mat.remove(node)


def check_edge_times(max_time):
    node_list = []
    for nodes in range(len(adj_mat)):
        edge_list = []
        for edges in range (len(adj_mat[nodes][1])):
            time = adj_mat[nodes][1][edges][1]
            if out_of_range(time,max_time):
                edge_list.append(adj_mat[nodes][1][edges])
        delete_edges(nodes,edge_list,adj_mat)
    for nodes in range(len(adj_mat)):
        if len(adj_mat) == 0:
            continue
        if len(adj_mat[nodes][1]) == 0:
            node_list.append(adj_mat[nodes])
    delete_nodes(node_list)
                

# Checks if older than 60s
def out_of_range(time,max_time):
    return (max_time-time).seconds > 60

def convert_time(st):
    return datetime.strptime(st,'%a %b %d %H:%M:%S +0000 %Y')



def main():
    cd = os.getcwd()
    challenge_dir = os.path.split(cd)
    finput = "\tweet_input\tweets.txt"
    foutput = "\tweet_output\tweets.txt"
    fin = challenge_dir[0]+finput
    fout = challenge_dir[0]+foutput
    with open(fin, 'r') as f:
        out_file = open(fout,"w")
        lines = f.readlines()
        # initialize variables
        max_time = datetime.strptime("Mon Jan 01 00:00:00 +0000 0001",'%a %b %d %H:%M:%S +0000 %Y')
        for line in lines:
            json_type = line
            json_type = json_type.split(":") 
            # Check if line is a tweet or rate-limit
            if "created_at" in json_type[0]:
                # Convert json to a list of hashtags and time
                tweet_json = json.loads(line)
                time = tweet_json['created_at']
                time = convert_time(time)
                hashtag_list = []
                for info in tweet_json['entities']['hashtags']:
                    hashtags = str(info).split("'")
                    hashtag_list.append(hashtags[3])
                tweet = [hashtag_list,time]
                # Now begin to update adjacency matrix
                if time > max_time:
                    max_time = time
                    check_edge_times(max_time)
                elif time < max_time:
                    if out_of_range(time,max_time):
                        out_file.write (str(avg_deg)+"\n")
                        continue
                if len(hashtag_list) < 2:
                    avg_deg = calculate_avg_deg()
                    out_file.write (str(avg_deg)+"\n")
                    continue
                for hashtags in hashtag_list:
                    in_graph = hashtag_in_graph(hashtags)
                    update_tweet_hashtag(hashtags,tweet)
                    #print(adj_mat)
        
                
                
                avg_deg = calculate_avg_deg()            
                out_file.write (str(avg_deg)+"\n")
        out_file.close()

main()


