from datetime import datetime
import random 

try:

    ahora = datetime.now()
    fahora = ahora.strftime("%Y,%m,%d,%H,%M,%S,%f")
   
    #%Y year
    #%m month
    #%d day
    #%H hour
    #%M minutre
    #%S seconds
    #%f ms
    # MORE --> https://www.w3schools.com/python/python_datetime.asp

    print(fahora)

    # FAKE Gather some value from external API
    data = random.randint(10,300)    

    # Store
    with open("values.csv","a") as f:
        f.write("%s,%i\n"%(fahora,data))

except Exception as e:
    print("Se ha generado el siguiente error :",e)



