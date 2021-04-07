import csv

file = open('가구공방.csv', 'r')
rdr = csv.reader(file)

woodFile = open('wood.csv', 'a')
woodRdr = csv.writer(woodFile)

glassFile = open('glass.csv', 'a')
glassRdr = csv.writer(glassFile)

leatherFile = open('leather.csv', 'a')
leatherRdr = csv.writer(leatherFile)

furnitureFile = open('furniture.csv', 'a')
furnitureRdr = csv.writer(furnitureFile)

dojaFile = open('doja.csv', 'a')
dojaRdr = csv.writer(dojaFile)

yugiFile = open('yugi.csv', 'a')
yugiRdr = csv.writer(yugiFile)

clothFile = open('cloth.csv', 'a')
clothRdr = csv.writer(clothFile)

metalFile = open('metal.csv', 'a')
metalRdr = csv.writer(metalFile)

foodFile = open('food.csv', 'a')
foodRdr = csv.writer(foodFile)

jewelyFile = open('jewely.csv', 'a')
jewelyRdr = csv.writer(jewelyFile)

candleFile = open('candle.csv', 'a')
candleRdr = csv.writer(candleFile)

remainFile = open('remain1.csv', 'a')
remainRdr = csv.writer(remainFile)

for line in rdr:
    if line[0].find('나무') != -1 or line[0].find('목공') != -1 or line[0].find('우드') != -1 or line[0].find('옻') != -1 or line[0].find('목기') != -1:
        print(line)
        woodRdr.writerow(line)
        line.clear
    elif line[0].find('유리') != -1 or line[0].find('글라스') != -1 or line[0].find('글래스') != -1:
        print(line)
        glassRdr.writerow(line)
        line.clear
    elif line[0].find('가죽') != -1 or line[0].find('레더') != -1 or line[0].find('leather') != -1:
        print(line)
        leatherRdr.writerow(line)
        line.clear
    elif line[0].find('가구') != -1:
        print(line)
        furnitureRdr.writerow(line)
        line.clear
    elif line[0].find('도자') != -1 or line[0].find('도예') != -1 or line[0].find('접시') != -1 or line[0].find('디쉬') != -1:
        print(line)
        dojaRdr.writerow(line)
        line.clear
    elif line[0].find('유기') != -1:
        print(line)
        yugiRdr.writerow(line)
        line.clear
    elif line[0].find('뜨개') != -1 or line[0].find(' 천 ') != -1 or line[0].find('자수') != -1 or line[0].find('미싱') != -1:
        print(line)
        clothRdr.writerow(line)
        line.clear
    elif line[0].find('금속') != -1 or line[0].find('메탈') != -1 or line[0].find('metal') != -1 or line[0].find('철공') != -1:
        print(line)
        metalRdr.writerow(line)
        line.clear
    elif line[0].find('케이크') != -1 or line[0].find('베이커리') != -1 or line[0].find('제빵') != -1 or line[0].find('음식') != -1 or line[0].find('베이킹') != -1 or line[0].find('튀김') != -1 or line[0].find('맥주') != -1:
        print(line)
        foodRdr.writerow(line)
        line.clear
    elif line[0].find('보석') != -1 or line[0].find('주얼리') != -1 or line[0].find('반지') != -1:
        print(line)
        jewelyRdr.writerow(line)
        line.clear
    elif line[0].find('캔들') != -1 or line[0].find('비누') != -1 or line[0].find('양초') != -1:
        print(line)
        candleRdr.writerow(line)
        line.clear
    else:
        remainRdr.writerow(line)
        line.clear