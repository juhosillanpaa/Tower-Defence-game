'''
Created on 27.3.2017

@author: sillanj5
'''

from square import Square
from round import Round

def create_road(current_game):
    '''
    Luo kartan lukemalla tiedostosta missa kohdassa on tieta.
    kartta on gamefile.txt. tiedostossa #kartan_nimi ja
    metodi lukee sen jalkeen niin monta rivia kuin pelin koko on
    (pelin kartta on neliskanttinen ja sivun ruutujen maara saadaan 
    get_size metodilla
    '''
    map = current_game.get_map()
    tiedosto = open("gamefile.txt", "r")
    #luetaan tiedostoa kartan tunnukseen asti
    for rivi in tiedosto:
        if (rivi[0:5] == "#"+ map):
            break #
    x = 0
    #luetaan tiedostoa pelin koon maaraama rivimaara
    for rivi in tiedosto:
        rivi = rivi.rstrip()
        if x >= current_game.get_size():
            break
        for y in range(current_game.get_size()):
            if rivi[y] == "-":
                current_game.get_square(y,x).change_to_road()
        x+=1      
    tiedosto.close()  
    return current_game  

def get_different_maps():
    
    '''
    lukee gamefiletiedostosta erilaisten karttojen nimet ja palauttaa
    listan, joka sisaltaa ne kaikki
    '''
    
    tiedosto = open("gamefile.txt", "r")
    kartat = []
    for rivi in tiedosto:
        rivi = rivi.rstrip()
        if rivi == "":
            continue
        if rivi[0] =="#":
            kartat.append(rivi[1:]) 
    tiedosto.close()
    return kartat
                
def read_round_info(current_game):
    '''
    Lukee tiedostoa tunnisteesta "Rounds of "+map eteenpain
    luo samalla Round luokkia, jotka saavat tiedon vihollistensa lukumaarasta
    ja tyypista. Nama luokat lisataan game-luokan kierroslistaan.
    luku paattyy kun saavutan # merkkiin
    '''
    map = current_game.get_map()
    tiedosto = open("gamefile.txt","r")
    for rivi in tiedosto:
        if rivi.rstrip() == "Rounds for " + map:
            break
    for rivi in tiedosto:
        rivi = rivi.rstrip()
        osa = rivi.split(":")
        if osa[0] == "&":
            break
        else:
            round = Round(current_game, int(osa[0]),osa[1],int(osa[2]) )
            current_game.add_round(round)
    tiedosto.close()
    return current_game

def save_game(game):
    vanha = open("saved_games.txt", "r")
    tiedosto = open("saved_games.txt","w")
    
    name = game.name
    next_round = game.next_round
    tiedosto.write("%:{:s}".format(name))
    tiedosto.write(":{:s}".format(game.current_map))
    tiedosto.write(":{:d}".format(next_round))
    tiedosto.write(":{:d}".format(game.health))
    tiedosto.write(":{:d}\n".format(game.money))
    for torni in game.towers:
        tiedosto.write("{:d}:{:d}:{:d}\n".format(torni.level, torni.x, torni.y))
    tiedosto.write("&\n")
    skippaa = False
    for rivi in vanha:
        rivi = rivi.rstrip()
        osat = rivi.split(":")
        if osat[0] == "%" and osat[1] == name:
            skippaa = True
            continue
        if skippaa and osat[0] == "&":
            skippaa = False
            continue
        if skippaa:
            continue
        else:
            tiedosto.write(rivi)
    tiedosto.close()
    vanha.close()
    
def load_game(game, name):
    '''
    Lataa nimen mukaisen pelin tiedostosta ja palauttaa sen,
    jos pelia ei loyty niin palautetaan -1
    '''
    tiedosto =open("saved_games.txt", "r")
    loytyi = False
    for rivi in tiedosto:
        rivi = rivi.rstrip()
        osat = rivi.split(":")
        if osat[0] == "%" and osat[1] == name:
            loytyi = True
            game.implement_loaded_game( osat[2], int(osat[3]), int(osat[4]), int(osat[5]))
            
            for rivi in tiedosto:
                rivi = rivi.rstrip()
                osat = rivi.split(":")
                if osat[0] == "&":
                    tiedosto.close()
                    return game
                else:
                    game.add_loaded_tower(int(osat[0]), int(osat[1]), int(osat[2]))             
        if not loytyi:
            tiedosto.close()
            return -1
                
                
                
                
                
                
                