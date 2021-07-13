import streamani

streamani.init()
animelink = streamani.getlink()
startt = streamani.getstart()
endd = streamani.getend()
quality =  streamani.getquality()
filetype = streamani.getfiletype()
streamani.main(animelink, startt, endd, quality, filetype)
streamani.success(animelink)