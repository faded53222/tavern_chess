import random
import copy
max_minion=7
team=[[],[]] 
class minion():
	def __init__(self,team,name,race,attack,health,deathrattle=0,shield=0,aoe=0,taunt=0,toxic=0,windfury=0):
		self.team=team
		self.ene_team=(team+1)%2
		self.name=name
		self.race=race
		self.deathrattle=deathrattle
		self.attack=attack
		self.health=health
		self.shield=shield
		self.aoe=aoe
		self.taunt=taunt
		self.toxic=toxic
		self.windfury=windfury
		self.wind_count=0
		self.summon_num=0
		self.summon_thing=0
	def get_target(self):
		taunt_list=[]
		for i in range(len(team[self.ene_team])):
			if team[self.ene_team][i].taunt==1:
				taunt_list.append(i)
		if len(taunt_list)>0:
			return team[self.ene_team][taunt_list[random.randint(0,len(taunt_list)-1)]]
		else:
			return team[self.ene_team][random.randint(0,len(team[self.ene_team])-1)]
	def attack_a(self,target):
		global current_team
		shield_lab0=0
		shield_lab1=0
		#print(self.name,' attack ',target.name)
		if self.shield==1 and target.attack>0:
			self.shield=0
			shield_lab0+=1
		else:
			self.health-=target.attack
			if target.toxic==1 and target.attack>0:
				self.health=0
		targets=[]
		targets.append(target)
		if self.aoe==1:
			if team[target.team].index(target)-1>=0:
				targets.append(team[target.team][team[target.team].index(target)-1])
			if team[target.team].index(target)+1<=len(team[target.team])-1:
				targets.append(team[target.team][team[target.team].index(target)+1])
		for a_target in targets:
			if a_target.shield==1:
				a_target.shield=0
				shield_lab1+=1
			else:
				a_target.health-=self.attack
				if self.toxic==1:
					a_target.health=0
		death_deal()
		for i in range(shield_lab0):
			for each in team[self.team]:
				if each.name=='Bolvar.Fireblood':
					each.attack+=2					
				if each.name=='Drakonid_Enforcer':
					each.attack+=2
					each.health+=2
				if each is self:
					continue
				if each.name=='Holy_Mackerel':
					each.shield=1
		for i in range(shield_lab1):
			for each in team[target.team]:
				if each.name=='Bolvar.Fireblood':
					each.attack+=2
				if each.name=='Drakonid_Enforcer':
					each.attack+=4
					each.health+=4
				if each in targets:
					continue				
				if each.name=='Holy_Mackerel':
					each.shield=1		
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
def summon(summoner,pos_left):
	if min(pos_left,summoner.summon_num)>0:
		if summoner.summon_thing.race=='Mech':
			for each in team[summoner.team]:
				if each.health>0 and each.name=='Deflect_o_Bot':
					each.attack+=min(pos_left,summoner.summon_num)
					each.shield=1
	for i in range(min(pos_left,summoner.summon_num)):
		S=copy.deepcopy(summoner.summon_thing)
		team[summoner.team].insert(team[summoner.team].index(summoner)+1,S)
		#print('summon ',summoner.name+'.'+S.name+'.'+str(i))
def give_shield(giver,pos_left):
	alive_list=[]
	for each in team[giver.team]:
		if each.health>0 and each.shield==0:
			alive_list.append(each)
	if len(alive_list)>0:
		random.choice(alive_list).shield=1
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
			A0=minion(0,'Foe_Reaper_4000','Mech',39,23,summon,0,1,0,0,0)
			A0.summon_num=6
			A0.summon_thing=minion(0,'Microbots','Mech',1,1)
			A1=minion(0,'Murloc_Warleader','Murloc',49,34,summon,0,0,0,1,0)
			A1.summon_num=2
			A1.summon_thing=minion(0,'plant','Common',1,1)
			A2=minion(0,'Annihilan_Battlemaster','Demon',27,30)
			A3=minion(0,'Rat_Pack','Beast',51,34,summon)
			A3.summon_num=A3.attack
			A3.summon_thing=minion(0,'rat','Beast',2,2)
			A4=minion(0,'Selfless_Hero','Common',2,1,give_shield)
			A5=minion(0,'Lightfang_Enforcer','Common',7,7,0,0,0,1,0,0)
			A6=minion(0,'Bronze_Warden','Dragon',46,30,summon,1,0,1,0,0)
			A6.summon_num=1
			A6.summon_thing=minion(0,'Bronze_Warden','Dragon',2,1,0,1,0,0,0,0)
			team[0].append(A0)
			team[0].append(A1)
			team[0].append(A2)
			team[0].append(A3)
			team[0].append(A4)
			team[0].append(A5)
			team[0].append(A6)
			B0=minion(1,'Deflect_o_Bot','Mech',22,14,0,1,0,0,0,0)
			B1=minion(1,'Holy_Mackerel','Murloc',14,9,0,0,0,0,1,0)
			B2=minion(1,'Foe_Reaper_4000','Mech',15,10,summon,0,1,0,0,0)
			B2.summon_num=3
			B2.summon_thing=minion(1,'Microbots','Mech',1,1)
			B3=minion(1,'Maexxna','Beast',4,10,0,0,0,0,1,0)
			B4=minion(1,'Drakonid_Enforcer','Dragon',10,15)
			B5=minion(1,'Bolvar.Fireblood','Common',1,7,0,1,0,0,0,0)
			B6=minion(1,'Mechano_egg','Mech',14,15,summon,1,0,1,0,0)
			B6.summon_num=1
			B6.summon_thing=minion(1,'Robosaur','Mech',16,16)
			
			#team[1].append(B0)
			#team[1].append(B1)
			#team[1].append(B2)
			#team[1].append(B3)
			#team[1].append(B4)
			#team[1].append(B5)
			#team[1].append(B6)
			
			team[1].append(B2)
			team[1].append(B1)
			team[1].append(B5)
			team[1].append(B3)
			team[1].append(B4)
			team[1].append(B0)
			team[1].append(B6)
			result=battle(f)
			count[result]+=1
		print('when team ',f,' attack first')
		print('team 0 win rate is: ','percent: {:.2%}'.format(count[0]/turns))
		print('team 1 win rate is: ','percent: {:.2%}'.format(count[1]/turns))
		print('tie rate is: ','percent: {:.2%}'.format(count[-1]/turns))
