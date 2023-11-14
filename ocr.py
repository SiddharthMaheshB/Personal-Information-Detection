import easyocr

def Read_Image(img):
    reader=easyocr.Reader(['en'], gpu=True)
    results = reader.readtext(img)
    print(results)
    text = ''
    if results:
      for i in results:
        if(i[2]>0.5):
           text = text + i[1] + " "
    return text,results

def get_coords(flags,results):
    '''if flags:
        coords = []
        for i in results:
            if(i[1] in flags):
                coords.append(i[0])'''
    coords = []
    flag = []
    common = "The be so up to of and a in that have I it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what  out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most this there that then where who what why us"
    common = common.lower()
    common = common.split()

    for i in flags:
        for j in i.split():
            print(j,end=" ")
            if j.lower() not in common:
                flag.append(j.lower())
                
    print("COMMON", common)
    print("RESULTS",results)
    print("FLAGS",flags)
    print("FLAG", flag)
    for i in results:
       for j in flag:
          if j in i[1].lower():
             coords.append(i[0])
    return coords