#!/Python33/python

# ADD FILTERING BASED ON TRAFFIC(edge weights)
import networkx as nx
import cgi, sys
import sqlite3
# import community
import json


print("Content-type: json\n\n")
fs = cgi.FieldStorage()
Time_start = fs["time-start"].value
Time_end = fs["time-end"].value
Date_start = fs["date-start"].value
Date_end = fs["date-end"].value

City = fs["name"].value

db_path = ""
if City == "Boston":
	db_path = "data/hubway.db"
elif City == "Chicago":
	db_path = "data/divvy.db"
else:
	db_path = "data/capitalbikeshare.db"

conn = sqlite3.connect(db_path)
# print "Opened database successfully"

# Time_start = "06:00:00"
# Time_end = "10:30:00"
# Date_start = "2011-10-28"
# Date_end = "2012-02-29"


g=nx.Graph()

cursor = conn.execute('select distinct st_id from stations')
for row in cursor:
	g.add_node(row[0],type = 'station')
	
# print g.nodes()


cursor1 = conn.execute('select start_st_id,end_st_id from trips where start_date>=date("'+Date_start+'")'+ ' and start_time>=time("'+Time_start+'")'+' and end_date<=date("'+ Date_end +'")'+ ' and end_time<=time("'+Time_end +'")')
for row in cursor1:
	if g.has_edge(row[0],row[1]):
		g[row[0]][row[1]]['weight'] = g[row[0]][row[1]]['weight'] +1
	else:
		g.add_edge(row[0],row[1], weight=1)


# Remove edges below a certain weight(!!!!!delete this part of Louvain!!!!)
for (s,t) in g.edges():
	if g[s][t]['weight']<5 :
		g.remove_edge(s,t)

# MAX CLIQUE
list_clique = list(nx.find_cliques(g))
(index, list_max) = max(enumerate(list_clique), key = lambda tup: len(tup[1]))
list_clique[index].sort()

data =  json.dumps(list_clique[index])
print(data)

# LOUVAIN
# partition = community.best_partition(g)
# print len(partition.keys())
# print "Louvain Modularity: ", community.modularity(partition, g)
# print "Louvain Partition: ", partition

