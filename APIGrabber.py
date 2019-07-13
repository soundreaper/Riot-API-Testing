import requests
import json

#Loads a file containing all champions and their respective ID numbers
with open('champions.txt') as json_file:
    champion_data = json.load(json_file)

#Takes in list of last 20 champions played and returns the most played
def currentlyMastering(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_freq = List.count(i)
        if(curr_freq > counter):
            counter = curr_freq
            num = i
    return num

def identifyChampion(num):
    for x in champion_data:
        if x['id'] == num:
            champ = x['name']
    return champ

#Uses region, summoner name, and API Key to build URL for Summoner Info
def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

#Uses region, summoner ID, and API Key to build URL for Ranked Info
def requestRankedData(region, summID, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

#Uses region, summoner ID, and API Key to build URL for Champion Mastery Info
def requestMasteryData(region, summID, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

#Uses region, account ID, and API Key to build URL for last 20 games played
def requestMatchHistory(region, acctID, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + acctID + "?endIndex=20&beginIndex=0&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

#Uses region, match ID, and API Key to build URL for match data
def requestMatchData(region, matchID, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/match/v4/matches/" + matchID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def main():
    #Asking for user inputted region (ONLY NA AND EUW work right now)
    region = input("Enter your region: ")
    summonerName = input("Enter your summoner ID: ")

    #Checks to see if summoner name has a space in it and replaces with "%20" 
    for check in summonerName:
        if (check.isspace()) == True:
            whiteSpace_fix = summonerName.split(" ")
            summonerName = whiteSpace_fix[0] + "%20" + whiteSpace_fix[1]

    #My personal Riot provided developer API Key
    APIKey = "RGAPI-af349bdc-9279-4742-948a-dfe812e5c642"

    #Calling first function to get encrypted summoner ID
    responseJSON = requestSummonerData(region, summonerName, APIKey)

    #Changing summoner ID and account ID to a string and assigning it to a var
    summonerID = str(responseJSON["id"])
    #accountID = str(responseJSON['accountId'])

    #Calling second function to get ranked data
    responseJSON2 = requestRankedData(region, summonerID, APIKey)

    #Calling third function to get champion mastery data
    responseJSON3 = requestMasteryData(region, summonerID, APIKey)

    #Calling fourth function to get match history of 20 games
    #responseJSON4 = requestMatchHistory(region, accountID, APIKey)

    #Making sure the displayed info is for Solo Queue and not Flex Queue
    if responseJSON2[0]["queueType"] == "RANKED_SOLO_5x5":
        infoNum = 0
    else:
        infoNum = 1

    #Printing Name, Queue Type, Rank, and LP
    print()
    print("-------------------------------------")
    print("Summoner Name: " + responseJSON2[infoNum]["summonerName"])
    print("Level: " + str(responseJSON['summonerLevel']))
    print("Queue Type: Ranked Solo/Duo")

    rank = responseJSON2[infoNum]["tier"]
    rankEdit = rank.lower().capitalize()
    print("Rank: " + rankEdit + " " + responseJSON2[infoNum]["rank"])
    print("League Points: " + str(responseJSON2[infoNum]["leaguePoints"]) + " LP")
    
    #Assigning Win & Loss and calculating winrate
    wins = str(responseJSON2[infoNum]["wins"])
    losses = str(responseJSON2[infoNum]["losses"])
    winrate_dec = responseJSON2[infoNum]["wins"]/(responseJSON2[infoNum]["wins"] + responseJSON2[infoNum]["losses"])
    winrate = str(round(winrate_dec * 100, 2))
    
    #Printing Win/Loss and Winrate %
    print("Win/Loss: " + wins + "/" + losses)
    print("Winrate: " + winrate + "%")

    #Finding highest mastery champ and assigning mastery level & mastery points
    champID = responseJSON3[0]["championId"]
    champName = identifyChampion(champID)
    masteryLevel = str(responseJSON3[0]["championLevel"])
    masteryPoints = str(responseJSON3[0]["championPoints"])
    
    #Printing Highest Mastery Champion, Mastery Level, and Mastery Points
    print()
    print("Favorite Champion: " + champName)
    print("Mastery Level: " + masteryLevel)
    print("Mastery Points: " + masteryPoints)
    print("-------------------------------------\n")

    '''
    #Collects list of last 20 played champions and identifies the most played
    twentyMatchChamps = responseJSON4['matches']
    champArr = []
    for x in twentyMatchChamps:
        champArr.append(x['champion'])
    mostPlayedID = currentlyMastering(champArr)
    champName = identifyChampion(mostPlayedID)

    #Printing the champion you are currently mastering
    print()
    print("Currently Mastering: " + champName)
    
    #Calculating winrate of currently mastering champion
    twentyMatchID = responseJSON4['matches']
    matchIDArr = []
    for x in twentyMatchID:
        matchIDArr.append(x['gameId'])

    for y in matchIDArr:
        matchData = [requestMatchData(region, str(y), APIKey)]
    
    print(matchData[0]['teams'][0]['win'])
    '''

if __name__ == "__main__":
    main()