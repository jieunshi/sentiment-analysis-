import csv

input_file =open("combined_unique_user_retweets_target.csv", 'r')
input_reader =csv.reader(input_file, delimiter='\t', quotechar= '\"')
input_file0 =open("combined_unique_user_retweets_target.csv", 'r')
input_reader0 =csv.reader(input_file0, delimiter='\t', quotechar= '\"')
input_file1 = open("democratic_twitter_actor_ids.csv", 'r')
input_reader1 = csv.reader(input_file1, delimiter='\t', quotechar= '\"')
input_file2 = open("republican_twitter_actor_ids.csv", "r")
input_reader2 = csv.reader(input_file2, delimiter='\t', quotechar='\"')

output_file= "user_retweet_patterns2.csv"

democratic_list =[]
republican_list=[]

for row, entry in enumerate(input_reader1):
	if row ==0:
		continue
	democratic_list.append(entry[0])
	print democratic_list
	

# print democratic_list

for row, entry in enumerate(input_reader2):
	if row ==0:
		continue
	republican_list.append(entry[0])
	print republican_list

# print republican_list

def generate_empty_entry():
	dict_entry =dict()
	dict_entry['democratic']=0
	dict_entry['republican']=0
	return dict_entry

democratic_dict = dict()
republican_dict = dict()

count =0 

for pea, bin in enumerate(input_reader):
	print pea
	if pea==0:
		continue

	if bin[0] not in republican_dict.keys():
		dict_entry =dict()
		dict_entry['republican']=0
		republican_dict[bin[0]] =dict_entry 

	result2 = "republican"
	if bin[3] in republican_list:
		# print bin[2]
		republican_dict[bin[0]][result2] +=1 
	else:
		pass 


print republican_dict 

count =0 

for row, content in enumerate(input_reader0):
	print row
	if row==0:
		continue

	if content[0] not in democratic_dict.keys():
		dict_entry =dict()
		dict_entry['democratic']=0
		democratic_dict[content[0]] =dict_entry

	result1 = "democratic"
	if content[3] in democratic_list:
		# print content[2]
		democratic_dict[content[0]][result1] +=1 
	else:
		pass 

print democratic_dict 
	# count +=1

	# if count %10 ==0: 
	# 	print str(count) + " have been processed..."


	# count +=1

	# if count %5 ==0: 
	# 	print str(count) + " have been processed..."


print "Merging"
final_dict =dict()

for k, v in democratic_dict.items():
	if k not in final_dict.keys():
		final_dict[k]=generate_empty_entry()

	final_dict[k]['democratic']=v['democratic']

for k, v in republican_dict.items():
	if k not in final_dict.keys():
		final_dict[k]=generate_empty_entry()

	final_dict[k]['republican']=v['republican']

print final_dict 
header =['actor_id', 'democratic', 'republican']

with open(output_file, 'w') as output:
	output_writer =csv.writer(output, delimiter ="\t")
	output_writer.writerow(header)
	for k, v in final_dict.items():
		output_entry = list()
		output_entry.append(k)
		output_entry.append(v['democratic'])
		output_entry.append(v['republican'])
		output_writer.writerow(output_entry)
