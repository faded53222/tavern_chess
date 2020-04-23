import random
max_minion=7
team=[[],[]] 
class minion():
	def __init__(self,team,name,attack,health,deathrattle=0,shield=0,aoe=0,taunt=0,toxic=0,revive=0,windfury=0,):
		self.team=team
		self.ene_team=(team+1)%2
		self.name=name
		self.deathrattle=deathrattle
		self.attack=attack
		self.health=health
		self.shield=shield
		self.aoe=aoe
		self.taunt=taunt
		self.toxic=toxic
		self.revive=revive
		self.windfury=windfury
		self.wind_count=0
	def get_target(self):
		taunt_list=[]
		for i in range(len(team[self.ene_team])):
			if team[self.ene_team][i].taunt==1:
				taunt_list.append[i]
		if len(taunt_list)>0:
			return team[self.ene_team][taunt_list[random.randint(0,len(taunt_list)-1)]]
		else:
			return team[self.ene_team][random.randint(0,len(team[self.ene_team])-1)]
	def attack_a(self,target):
		global current_team
		#print(self.name,' attack ',target.name)
		if self.shield==1 and target.attack>0:
			self.shield=0
		else:
			self.health-=target.attack
			if target.toxic==1 and target.attack>0:
				self.health=0
		targets=[]
		targets.append(target)
		if self.aoe==1:
			if team[target.team].index(target)-1>0:
				targets.append(team[target.team][team[target.team].index(target)-1])
			if team[target.team].index(target)+1<max_minion-1:
				targets.append(team[target.team][team[target.team].index(target)+1])
		for a_target in targets:
			if target.shield==1:
				a_target.shield=0
			else:
				a_target.health-=self.attack
				if self.toxic==1:
					a_target.health=0
		death_deal()
		if self.windfury==1:
			self.wind_count=(self.wind_count+1)%2
		if not (self.wind_count==1 and self.health>0):
			current_team=(current_team+1)%2
		if self.health>0 and self.wind_count!=1:
			current_minion[self.team]=team[self.team][(team[self.team].index(self)+1)%len(team[self.team])]
current_minion=[0,0]
def death_deal():
	death_list=[[],[]]
	temp_max=[0,0]
	for i in (0,1):
		for each in team[i]:
			if each.health<=0:
				death_list[i].append(each)
		temp_max[i]=len(death_list[i])+max_minion
		for each in death_list[i]:
			if each.deathrattle!=0:
				each.deathrattle(each,temp_max[i]-len(team[i]))
		for each in death_list[i]:
			if each is current_minion[i]:
				current_index=team[i].index(each)
				for k in range(0,len(team[i])-1):
					current_index=(current_index+1)%len(team[i])
					if team[i][current_index] not in death_list[i]:
						current_minion[i]=team[i][current_index]
						break
			team[i].remove(each)
current_team=0
def battle(offensive_team):
	global current_team
	current_minion[0]=team[0][0]
	current_minion[1]=team[1][0]
	current_team=offensive_team
	while(1):
		if len(team[1])==0:
			if len(team[0])==0:
				return -1
			else:
				return 0
		elif len(team[0])==0:
			return 1
		target=current_minion[current_team].get_target()
		current_minion[current_team].attack_a(target)
def summon_two_1_1(summoner,pos_left):
	F0=minion(summoner.team,summoner.name+'.1_1.0',1,1)
	F1=minion(summoner.team,summoner.name+'.1_1.1',1,1)
	if pos_left>=1:
		team[summoner.team].insert(team[summoner.team].index(summoner)+1,F0)
		#print('summon ',summoner.name+'.1_1.0')
	if pos_left>=2:
		team[summoner.team].insert(team[summoner.team].index(summoner)+2,F1)
		#print('summon ',summoner.name+'.1_1.1')
if __name__ == "__main__":
	for f in (0,1):
		count={}
		count[0]=0
		count[1]=0
		count[-1]=0
		turns=100000
		for k in range(turns):
			team[0].clear()
			team[1].clear()
			for i in range(0,6):
				A=minion(0,'A'+str(i),1,100,summon_two_1_1,1,0,0,1,0,1)
				team[0].append(A)
				B=minion(1,'B'+str(i),1,100,summon_two_1_1,1,0,0,1,0,0)
				team[1].append(B)	
			A6=minion(0,'A6',1,100)
			team[0].append(A6)
			B6=minion(1,'B6',1,100)
			team[1].append(B6)		
			result=battle(f)
			count[result]+=1
		print('when team ',f,' attack first')
		print('player 1 win rate is: ','percent: {:.2%}'.format(count[0]/turns))
		print('player 2 win rate is: ','percent: {:.2%}'.format(count[1]/turns))
		print('tie rate is: ','percent: {:.2%}'.format(count[-1]/turns))
