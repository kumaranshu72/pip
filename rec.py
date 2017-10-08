from surprise import AlgoBase
from surprise import Dataset
from surprise import evaluate
from math import sqrt
import collections

class PIP(AlgoBase):

    def __init__(self,user_dataset,item_dataset):
        # Always call base method before doing anything.
        AlgoBase.__init__(self)
        self.Rmin = 1
        self.Rmax = 5
        self.Rmid = (self.Rmin + self.Rmax)/2.0
        # Movie id with title
        self.movies = {}
        for line in open(item_dataset):
            (id,title) = line.split('|')[0:2]
            self.movies[id]=title

        # Load users data
        self.userData ={}
        for line in open(user_dataset):
            (user,movieid,rating,ts)=line.split('\t')
            self.userData.setdefault(user,{})
            self.userData[user][self.movies[movieid]]=float(rating)

        # Creating User list
        self.UsersList = [i for i in self.userData]

    def Agreement(self,r1,r2):
        self.r1 = r1
        self.r2 = r2
        if (self.r1 > self.Rmid and self.r2 < self.Rmid) or (self.r1 < self.Rmid and self.r2 > self.Rmid):
            return False
        return True

    def Proximity(self,r1,r2):
        if self.Agreement(r1,r2):
            self.absDist = abs(r1-r2)
        self.absDist = 2*abs(r1-r2)
        return ((2*(self.Rmax-self.Rmin)+1)-self.absDist)**2

    def Impact(self,r1,r2):
        return (((abs(r1-self.Rmid)+1)*(abs(r2-self.Rmid)+1)) if self.Agreement(r1,r2) else (1.0/((abs(r1-self.Rmid)+1)*(abs(r2-self.Rmid)+1))))

    def Popularity(self,r1,r2,item):
        itemRating = []
        for itm in self.itemData[item]:
            itemRating.append(self.itemData[item][itm])

        self.avg = self.mean(itemRating)
        return ((1 + (((r1+r2)/2.0 - self.avg)**2)) if (r1 > self.avg and r2 > self.avg) or (r1 < self.avg and r2 < self.avg) else 1)

    def similarity(self,user1,user2,choice):
       self.createItemData()
       if choice:
           data = self.userData
       else:
           data = self.itemData
       # Get the list of the shared_items
       commonItem = {}
       for item in data[user1]:
           if item in data[user2]:
               commonItem[item] = 1

       # if no common items
       if len(commonItem)==0: return 0

       # PIP calculation
       result = 0
       for item in data[user1]:
           if item in data[user2]:
               r1 = data[user1][item]
               r2 = data[user2][item]
               result += self.Proximity(r1,r2)*self.Impact(r1,r2)*self.Popularity(r1,r2,item)

       return result


    def estimate(self, user,distanceType):
        tot = collections.defaultdict(float)
        sums = collections.defaultdict(float)

        for other in self.userData:

            # Don't compare me to myself
            if other == user: continue
            simi = distanceType(user,other,True)

            # Ignore scores of zero or lower
            if simi <= 0: continue
            for item in self.userData[other]:

                # Only scores movies I haven't seen yet
                if item not in self.userData[user] or self.userData[user][item]==0:
                    # Similarity * Score
                    tot[item]+=self.userData[other][item]*simi
                    # Sum of similarities
                    sums[item]+=simi



        # Create the normalized list
        rankings = [(total/sums[item],item) for (item, total) in tot.items()]
        # Return the sorted list
        rankings.sort()
        rankings.reverse()
        return rankings

    def createItemData(self):
        result = collections.defaultdict(dict)
        for person in self.userData:
            for item in self.userData[person]:
                # Flip item and person
                result[item][person] = self.userData[person][item]
        self.itemData = result

    def mean(self,listinput):
        total = 0.0
        for entry in listinput:
            total += entry
        return total/len(listinput)

R = PIP('u.data','u.item')
print 'PIP :: ', R.estimate('87',R.similarity)[0:10],'\n'
