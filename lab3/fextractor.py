import os
import argparse
import statistics
#CSF1819: 
    #Here you should add more features to the feature vector (features=[]) representing a cell trace

    #Function extract receives as input two sequences:
    #    times: timestamp of each cell
    #    sizes: direction of each cell (-1 / +1)

    #As of now, the only feature being used to distinguish between page loads is the total
    # amount of cells in each cell sequence and is given by len(times).

    # Shall some feature be missing due to impossibility of its calculation, 
    #please replace its value with "X". It will be replaced later.

def extract(times, sizes, minus, plus, minusf, plusf,mean,std,median,ts,t,meanTime,stdTime,mediaTime,meanReq,stdReq,medianReq,maxSucc,meanIn,stdIn,medianIn,maxSucc2,burstIn,burstOut,meanChunks,stdChunks,medianChunks,outChunks,maxChunks,percentil,percentilIn,percentilTime,percentilReq,percentilChunks,concentrationSum,meanInVector,stdInVector,meanOutVector,stdOutVector,inVector,outVector):
    features = []

    #Total amount of cells in sequence
    features.append(len(times))
    features.append(minus)
    features.append(plus)
    features.append(minusf)
    features.append(plusf)
    features.append(mean)
    features.append(std)
    features.append(median)
    features.append(ts)
    features.append(t)
    features.append(meanTime)
    features.append(stdTime)
    features.append(medianTime)
    features.append(meanReq)
    features.append(stdReq)
    features.append(medianReq)
    features.append(maxSucc)
    features.append(meanIn)
    features.append(stdIn)
    features.append(medianIn)
    features.append(maxSucc2)
    features.append(burstIn)
    features.append(burstOut)
    #direcçoes dos 100 primeiros pacotes
    for i in range(0,100):
        try:
            features.append(sizes[i])
        except:
            features.append(0)
    features.append(meanChunks)
    features.append(stdChunks)
    features.append(medianChunks)
    #soma de out + in + numero de cells
    features.append(len(times) + minus + plus)
    #numero de outgoing requests em cada chunk
    for i in range(0,100):
        try:
            features.append(outChunks[i])
        except:
            features.append(0)
    features.append(maxChunks)
    features.append(percentil)
    features.append(percentilIn)
    features.append(percentilTime)
    features.append(percentilReq)
    features.append(percentilChunks)
    features.append(concentrationSum)
    features.append(meanInVector)
    features.append(stdInVector)
    features.append(meanOutVector)
    features.append(stdOutVector)
    for i in range(0,500):
        try:
            features.append(inVector[i])
        except:
            features.append(0)
    for i in range(0,500):
        try:
            features.append(outVector[i])
        except:
            features.append(0)
    return features

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def impute_missing(x):
        """Accepts a list of features containing 'X' in
        place of missing values. Consistently with the code
        by Cai et al, replaces 'X' with -1.
        """
        for i in range(len(x)):
            if x[i] == 'X':
                x[i] = -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract feature vectors')
    parser.add_argument('--traces', type=str, help='Original traces directory.',
                        required=True)
    parser.add_argument('--out', type=str, help='Output directory for features.',
                        required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.out):
        os.makedirs(args.out)

    #this takes quite a while
    print ("Gathering features for monitored sites...")
    for site in range(0, 100):
        print (site)
        for instance in range(0, 90):
            fname = str(site) + "-" + str(instance)
            #Set up times, sizes
            f = open(args.traces + "/" + fname, "r")
            times = []
            sizes = []

            outIn = []
            plusOne = 0
            minusOne = 0;
            lastTimeStamp = 0
            temp = []
            for x in f:
                x = x.split("\t")
                if int(x[1]) == 1:
                    temp.append(int(float(x[0])))
                    
                times.append(float(x[0]))
                sizes.append(int(x[1]))
                outIn.append(int(x[1]))
                lastTimeStamp = float(x[0])
                #primeira ideia
                if int(x[1]) > 0:
                    plusOne += 1
                else:
                    minusOne += 1
            #extrai os 1s sucessivos
            succ = []
            count = 0
            isFirst = True
            for i in range(0,len(outIn)):
                if(isFirst):
                    if int(outIn[i]) == 1:
                        count = 1
                    isFirst = False
                    continue
                if int(outIn[i]) == 1 :
                    if int(outIn[i-1]) == 1:
                        count += 1
                    else:
                        count = 1
                else:
                    if(count > 0):
                        succ.append(count)
                    count = 0
            if count > 0:
                succ.append(count)
            #extrai os -1s sucessivos
            succ2 = []
            count = 0
            isFirst = True
            for i in range(0,len(outIn)):
                if(isFirst):
                    if int(outIn[i]) == -1:
                        count = 1
                    isFirst = False
                    continue
                if int(outIn[i]) == -1 :
                    if int(outIn[i-1]) == -1:
                        count += 1
                    else:
                        count = 1
                else:
                    if(count > 0):
                        succ2.append(count)
                    count = 0
            if count > 0:
                succ2.append(count)
            #faz a media dos 1s
            counter = 0
            for i in succ:
                counter += i
            mean = float(counter)/len(succ)
            #faz desvio padrao dos 1s
            try:
                std = statistics.stdev(succ)
            except:
                std = 0
            #faz mediana dos 1s
            median = statistics.median(succ)
            #percentil 50
            percentil = statistics.median_grouped(succ)
            #faz a media dos -1s
            counter = 0
            for i in succ2:
                counter += i
            meanIn = float(counter)/len(succ2)
            #faz o desvio padrao dos -1s
            try:
                stdIn = statistics.stdev(succ2)
            except:
                stdIn = 0
            #faz mediana dos -1s
            medianIn = statistics.median(succ2)
            #percentil 50
            percentilIn = statistics.median_grouped(succ2)
            #pacotes transmitidos por segundo
            throughput = float(len(times))/lastTimeStamp
            #faz a media do tempo
            counter = 0
            for i in times:
                counter += i
            meanTime = float(counter)/len(times)
            #faz o desvio padrao do tempo
            try:
                stdTime = statistics.stdev(times)
            except:
                stdTime = 0
            #mediana
            medianTime = statistics.median(times)
            #percentil 50
            percentilTime = statistics.median_grouped(times)
            #pedidos enviados a cada segundo
            #media
            counter = 0
            for i in temp:
                counter += i
            meanReq = float(counter)/len(temp)
            #desvio padrao
            try:
                stdReq = statistics.stdev(temp)
            except:
                stdReq = 0
            #mediana
            medianReq = statistics.median(temp)
            #percentil 50
            percentilReq = statistics.median_grouped(temp)
            #numero maximo de 1s
            maxSucc = max(succ)
            #numero maximo de -1s
            maxSucc2 = max(succ2)
            #numero de bursts de 1 > 4
            succTemp = [ elem for elem in succ if elem > 4]
            burstIn = len(succTemp)
            #numero de bursts de -1 > 4
            succ2Temp = [ elem for elem in succ2 if elem > 4]
            burstOut = len(succ2Temp)
            minusFraction = float(minusOne)/len(times)
            plusFraction = float(plusOne)/len(times)
            #divido o sizes em chunks de 20 e vejo quantos outgoing requests é que estão em cada um
            chunksList = [sizes[i:i + 5] for i in range(0, len(sizes), 20)]
            outChunks = []
            for lista in chunksList:
                counter = 0
                for elm in lista:
                    if elm == 1:
                        counter += 1
                outChunks.append(counter)
            #chunks concentration sum
            concentrationChunks = []
            for lista in chunksList:
                counter = 0 
                for elm in lista:
                    if elm == 1:
                        counter += 1
                concentrationChunks.append(float(counter)/len(lista))
            concentrationSum = 0
            for i in concentrationChunks:
                concentrationSum += i    
            #com base nos chunks:
            #média
            counter = 0
            for i in outChunks:
                counter += i
            meanChunks = float(counter)/len(outChunks)
            #desvio padrao
            try:
                stdChunks = statistics.stdev(outChunks)
            except:
                stdChunks = 0
            #mediana
            medianChunks = statistics.median(outChunks)
            #percentil 50
            percentilChunks = statistics.median_grouped(outChunks)
            #chunk maximo
            maxChunks = max(outChunks)
            #vetores com as posicoes de ingoing e outgoing
            outVector=[]
            inVector=[]
            for i in range(0,len(sizes)):
                if int(sizes[i]) == 1:
                    outVector.append(i)
                else:
                    inVector.append(i)
            #media do inVector
            counter = 0
            for i in inVector:
                counter += i
            meanInVector = float(counter)/len(inVector)
            #desvio padrao do inVector
            try:
                stdInVector = statistics.stdev(inVector)
            except:
                stdInVector = 0
            #media do outVector
            counter = 0
            for i in outVector:
                counter += i
            meanOutVector = float(counter)/len(outVector)
            #desvio padrao do outVector
            try:
                stdOutVector = statistics.stdev(outVector)
            except:
                stdOutVector = 0
            



            #Extract features. All features are non-negative numbers or X. 
            features = extract(times, sizes,minusOne, plusOne,minusFraction,plusFraction,mean,std,median,lastTimeStamp,throughput,meanTime,stdTime,medianTime,meanReq, stdReq, medianReq, maxSucc,meanIn,stdIn,medianIn,maxSucc2,burstIn,burstOut,meanChunks,stdChunks,medianChunks,outChunks,maxChunks,percentil,percentilIn,percentilTime,percentilReq,percentilChunks,concentrationSum,meanInVector,stdInVector,meanOutVector,stdOutVector,inVector,outVector)

            #Replace X by -1 (Cai et al.)
            impute_missing(features)

            fout = open(args.out + "/" + fname + ".features", "w")
            for x in features[:-1]:
                fout.write(repr(x) + ",")
            fout.write(repr(features[-1]))
            fout.close()

    print ("Finished gathering features for monitored sites.")

    print ("Gathering features for non-monitored sites...")
    #open world
    for site in range(0, 9000):
        print (site)
        fname = str(site)
        #Set up times, sizes
        f = open(args.traces + "/" + fname, "r")
        times = []
        sizes = []
        for x in f:
            x = x.split("\t")
            times.append(float(x[0]))
            sizes.append(int(x[1]))
        f.close()
    
        #Extract features. All features are non-negative numbers or X. 
        features = extract(times, sizes)

        #Replace X by -1 (Cai et al.)
        impute_missing(features)

        fout = open(args.out + "/" + fname + ".features", "w")
        for x in features[:-1]:
            fout.write(repr(x) + ",")
        fout.write(repr(features[-1]))
        fout.close()

    print ("Finished gathering features for non-monitored sites.")
    f.close()
