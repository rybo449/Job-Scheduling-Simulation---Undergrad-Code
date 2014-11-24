from collections import deque
import time
import os
import sys
blocks=int(raw_input())
processors=int(raw_input())
clock_ticks=0
flag=0
flag1=0
count_flag=0
waiting_processes={i:[] for i in xrange(blocks)}
waiting_time={i:[] for i in xrange(blocks)}
processor_dict={i:{j:{k:0 for k in xrange(2)} for j in xrange(processors)} for i in xrange(blocks)}
local_dict={i:deque() for i in xrange(20)}
gang_dict=deque()
length_of_waiting_queue={i:0 for i in xrange(100)}


def print_output():
	global count_flag
	if flag==0 and count_flag==0:
		print "Flag Has been set! There are no more local jobs left to arrive!"
		print
		count_flag=count_flag+1
	print "Block Number\tProcessor Number\tProcessor Queue\t\tTime"
	print 
	for i in xrange(blocks):
		for j in xrange(processors):
			print i+1,"\t\t",j+1,"\t\t\t",processor_dict[i][j],"\t\t",clock_ticks
			print
	for i in xrange(blocks):
		print "Local Queue of Block ",(i+1)," is: ",local_dict[i]
		print
	print "Centralized Gang Queue: ",gang_dict
	print
def clock_count():
	global clock_ticks
	clock_ticks=clock_ticks+1
	if clock_ticks%3==0:
		os.system('clear')
	print_output()
	time.sleep(1)
	for i in xrange(blocks):
		for j in xrange(processors):
			for k in xrange(2):
				if processor_dict[i][j][k]!=0:
					processor_dict[i][j][k]=processor_dict[i][j][k]-1
	if flag==0:
		for i in xrange(blocks):
			for k in xrange(len(waiting_time[i])):
				waiting_time[i][k]=waiting_time[i][k]-1
	
	
def execute_processes():
	count=0
	count1=0
	count2=0
	for i in xrange(blocks):
		count1=0
		for j in xrange(processors):
			count=0
			for k in xrange(2):
				if processor_dict[i][j][k]==0:
					count=count+1
			if count==2:
				count1=count1+1	
		if count1==processors:
			count2=count2+1
	if count2!=blocks:
		clock_count()
		execute_processes()
	else:
		sys.exit()



def iteration():
	global clock_ticks
	global flag
	count=0
	#print "flag=",flag
	#print "Waiting time=",waiting_time
	if flag==0:
		for i in xrange(blocks):
			#if len(waiting_time[i])!=0:
			length_of_waiting_queue[i]=len(waiting_time[i])
			if len(waiting_time[i])==0:
				count=count+1
				if count==blocks:
					flag=1
					#print "Flag is Set"
					break
				else:
					continue
			if waiting_time[i][length_of_waiting_queue[i]-1]<=0:
				w=waiting_processes[i][length_of_waiting_queue[i]-1]
				waiting_processes[i].pop()
				waiting_time[i].pop()
				add_to_local_queue(w,i)

	for i in xrange(blocks):
		for j in xrange(processors):
			for k in xrange(len(processor_dict[i][j])):
				if processor_dict[i][j][k]==0:
					if len(gang_dict)>0:
						w=gang_dict.popleft()
						add_to_local_queue(w,i)
					if len(local_dict[i])>0:
						processor_dict[i][j][k]=local_dict[i].popleft()
						#print "Local Job of Block %d with Runtime %d is Assigned to the %d Processor of its block at time %d"%(i,processor_dict[i][j][k],j,clock_ticks)
					'''elif len(gang_dict)>0:
						processor_dict[i][j][k]=gang_dict.popleft()
						print "One Part of a Gang Job of Runtime %d is Assigned to Processor %d of Block %d at time %d"%(processor_dict[i][j][k],j,i,clock_ticks)
						if len(gang_dict)==0:
							return'''
		#print "Local Queue=",local_dict[i]

	count_no_of_blocks=0
	count_no_of_processors=0

	'''for i in xrange(blocks):
		count_no_of_processors=0
		for j in xrange(processors):
			print len(waiting_processes[i])
			if len(waiting_processes[i])==0:
				count_no_of_processors=count_no_of_processors+1
			print "No of processors=",count_no_of_processors
		if count_no_of_processors==processors:
			count_no_of_blocks=count_no_of_blocks+1
			print "No of Blocks=",count_no_of_blocks'''
	#print "Length of Gang=",len(gang_dict)
	if flag==1 and len(gang_dict)==0 and flag1==1:
		print_output()
		return
	elif flag==1 and len(gang_dict)==0 and flag1==0:
		execute_processes()
	else:
		clock_count()
		iteration()
	return

	
def add_to_waiting_processes(a,b,i):
	waiting_processes[i].append(a)
	waiting_time[i].append(b)
	for x in xrange(len(waiting_processes[i])):
		for y in xrange(i+1,len(waiting_processes[i])):
			if waiting_time[i][x]<waiting_time[i][y]:
				temp=waiting_time[i][x];
				waiting_time[i][x]=waiting_time[i][y];
				waiting_time[i][y]=temp

				temp=waiting_processes[i][x]
				waiting_processes[i][x]=waiting_processes[i][y]
				waiting_processes[i][y]=temp
	
def add_to_gang_queue(a,b):
	for j in xrange(b):
		gang_dict.append(a)


def add_to_local_queue(a,i):
	local_dict[i].append(a)


def main():
	for i in xrange(blocks):
		local_queue_size=int(raw_input())
		for k in xrange(local_queue_size):
			ip=raw_input().split()
			a=int(ip[0])
			b=int(ip[1])
			if b>0:
				add_to_waiting_processes(a,b,i)
				length_of_waiting_queue[i]=length_of_waiting_queue[i]+1
			else:
				add_to_local_queue(a,i)
	print waiting_processes
	gang_queue_size=int(raw_input())

	for i in xrange(gang_queue_size):
		ip=raw_input().split()
		a=int(ip[0])
		b=int(ip[1])
		add_to_gang_queue(a,b)



	#print "Start Time= %d"%(clock_ticks)


	for i in xrange(blocks):
		for j in xrange(processors):
			for k in xrange(2):
				if processor_dict[i][j][k]==0:
					if len(local_dict[i])>0:
						processor_dict[i][j][k]=local_dict[i].popleft()
						#print "Local Job of Block %d with Runtime %d is Assigned to the %d Processor of its block at time %d"%(i,processor_dict[i][j][k],j,clock_ticks)
					elif len(gang_dict)>0:
						processor_dict[i][j][k]=gang_dict.popleft()
						#print "One Part of a Gang Job of Runtime %d is Assigned to Processor %d of Block %d at time %d"%(processor_dict[i][j][k],j,i,clock_ticks)
	print gang_dict

	clock_count()
	print waiting_processes
	#while len(gang_dict)>0 or len(waiting_processes)>0:
	iteration()


if __name__=="__main__":
	main()	


		
