from scipy import special
from scipy.stats import linregress
from os import walk
import json
import operator 
slope, intercept, r_value, p_value, std_err = linregress([1 ,2, 3], [0, 2, 4 ])
#print(slope)

## does linear regression on all stats in given folder
def linRegAll(folder):
    d = {}
    for path, dirnames, filenames in walk(folder):
        for fname in filenames:
            name = folder + '/' + fname
            f = open(name).read()
            data = json.loads(f)
            slope, intercept, r_value, p_value, std_err = linregress(data)
            d[fname] = {"slope":slope, "intercept": intercept,"r_value": r_value, "p_value": p_value, "std_err":std_err, "number": len(data), "data": data}
    return sorted(d.items(), key = operator.itemgetter(0))

# for i in reversed(linRegAll(folder = "teamGoldTeamScore")):
#     print(i[0], "slope ",  i[1][0] , " intercept: " ,  i[1][1] , " r_value: " , i[1][2] , " p_value: " , i[1][3], " std_err: ", i[1][4], " count: " , i[1][5])

teamGoldTeamScore = (linRegAll(folder = "teamGoldTeamScore"))
teamGoldIndScore = (linRegAll(folder = "teamGoldIndScore"))
indGoldIndScore = (linRegAll(folder = "indGoldIndScore"))

scores = sorted(indGoldIndScore, key = lambda l:-1* l[1]["slope"])
x = 1; 
for tup in scores:
    if(tup[1]["r_value"] > .5):
        print(x, ",", tup[0],",", tup[1]["slope"])
        x+=1; 


champs = []
for i in teamGoldIndScore:
    champs.append(i[0])
def findIndex(champ):
    count = 0
    for i in champs:
        if (i == champ):
            return count
        else: 
            count+=1
import numpy as np
import matplotlib.pyplot as plt

def graphChamp(champ):
    ind = findIndex(champ)
    tt = teamGoldTeamScore[ind]
    ti = teamGoldIndScore[ind]
    ii = indGoldIndScore[ind]
    print("tt r value: ", tt[1]["r_value"])
    print("ti r value: ", ti[1]["r_value"])
    print("ii r value: " , ii[1]["r_value"])
    x = np.linspace(0, 25, 100)
    Tt_y = tt[1]["slope"] * x + tt[1]["intercept"]
    ti_y = ti[1]["slope"] * x + ti[1]["intercept"]
    ii_y = ii[1]["slope"] * x + ii[1]["intercept"]
    #plt.plot(x, tt_y, 'r')
    #plt.plot(x, ti_y, 'g')
    plt.plot(x, ii_y,'r')
    
    
    plt.title(champ)
    plt.xlabel("% Game Gold")
    plt.ylabel("score")
    
    ##scatter plots
    data_tt = tt[1]["data"]
    # for point in data_tt: 
    #     plt.scatter(point[0], point[1], c = 'r', s = 70)
    # data_ti = ti[1]["data"]
    # for point in data_ti: 
    #     plt.scatter(point[0], point[1], c = 'g', s = 70)
    data_ii = ii[1]["data"]
    for point in data_ii: 
        plt.scatter(point[0], point[1], c = 'g', s = 70)
    plt.xlim([5,17])
    plt.ylim([-20,20])
    plt.show()
    

graphChamp("LeeSin")

## Graph CDF of all slopes (score vs gold regressions)
def graphCDF(alist, color = "blue"): 
    alist = sorted(alist)
    yvals = [i for i in range(0,len(alist))]
    yvals = map(lambda el: (el + 1) / len(alist), yvals)
    yvals = [i for i in yvals]
    alist = [i for i in alist]
    plt.plot(alist, yvals,  color = color, linestyle = "solid", linewidth = 5)
    plt.title("CDF of Each Champion's Correlation between Gold and Score")
    plt.xlabel("Correlation")
    plt.ylabel("Cummulative Distribution")
    plt.show()
    
#graphCDF()
correlations = [i for i in map( lambda el : el[1]["r_value"], [i for i in indGoldIndScore])]
graphCDF(correlations)
#given string gets role of champ
def getRole(champ):
    f = open("champ_data.txt").read()
    champ_data = json.loads(f)
    return(champ_data['data'][champ]["tags"][0])

def graphCDFRole(role, color = 'black', criticalValue = 0):

    scores = sorted(indGoldIndScore, key = lambda l:1*l[1]["slope"])## sort -1 to reverse order
    champs = []
    print(role, " : ")
    removed = []
    counter = 0
    for tup in scores: 
        if(getRole(tup[0]) == role):
            if(tup[1]["r_value"] > criticalValue):
                champs.append(tup)
                counter +=1
                print(counter, ",",tup[0],",", tup[1]["slope"])
            else: 
                removed.append(tup[0])
    print("\n")

    wantedSlopes = map(lambda el: el[1]["slope"], champs)
    yVals = [num for num in range(0, len(champs) + 1)]
    div = []
    for i in yVals: 
        div.append((i )/ (len(yVals) - 1))
    wanted = [i for i in wantedSlopes]
    wanted.insert(0,0)
    plt.plot(wanted, div,  color = color, linestyle = "solid", linewidth = 5)
    plt.xlabel("Slope of Score / % of Game Gold")
    plt.ylabel("% of champions")
    return removed


plt.show()
def graphAllRoles(criticalValue = 0):
    plt.title("CDF of the Score Ratio for the Support and Marskman Roles")
    sup = 'green'
    marksman = 'red'
    mage = 'blue'
    tank = 'black'
    assasin  = 'pink'
    fighter = 'brown'
    removed = {}
    removed["support"] = graphCDFRole("Support", sup, criticalValue)
    removed["marksman"] = graphCDFRole("Marksman", marksman, criticalValue)
    removed["mage"] = graphCDFRole("Mage", mage, criticalValue)
    removed["tank"] = graphCDFRole("Tank", tank, criticalValue)
    removed["assassin"]= graphCDFRole("Assassin", assasin, criticalValue)
    removed["fighter"] = graphCDFRole("Fighter", fighter, criticalValue)
    plt.legend(["Support", "Marksman", "Mage", "Tank", "Assassin", "Fighter"], loc=4)
    #plt.legend(["Support", "Marksman"], loc=4);
    print(removed)

    plt.show()

graphAllRoles(criticalValue = .5)







# n_groups = len(teamGoldIndScore)


# mean_tt = []
# for i in teamGoldTeamScore:
#     mean_tt.append(i[1][0])

# mean_ti = []
# for i in teamGoldIndScore:
#     mean_ti.append(i[1][0])

# mean_ii = []
# for i in indGoldIndScore:
#     mean_ii.append(i[1][0])




# fig, ax = plt.subplots()

# index = np.arange(n_groups)

# bar_width = .7
# opacity = 0.9
# error_config = {'ecolor': '0.3'}

# rect_ii = plt.bar(index, mean_ii, bar_width,
#                   alpha=opacity,
#                   color='b',
#                   #yerr=std_men,
#                   error_kw=error_config,
#                   label='indGoldIndScore')

# # rects_tt = plt.bar(index + bar_width, mean_tt, bar_width,
# #                   alpha=opacity,
# #                   color='r',
# #                   #yerr=std_women,
# #                   error_kw=error_config,
# #                   label='teamGoldTeamScore')
# # rects_ti = plt.bar(index + bar_width + bar_width, mean_ti, bar_width,
# #                   alpha=opacity,
# #                   color='y',
# #                   #yerr=std_women,
# #                   error_kw=error_config,
# #                   label='teamGoldIndScore')

# plt.xlabel('Group')
# plt.ylabel('Scores')
# plt.title('Scores by group and gender')
# plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E'))
# plt.legend()
# plt.show()
