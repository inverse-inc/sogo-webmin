all:
	tar --exclude .DS_Store -zcvf sogo.wbm.gz sogo

clean:
	rm -f sogo.wbm.gz
