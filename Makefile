all::

CORPUS = corpus/pan16-author-clustering-training-dataset-2016-02-17/
CONTROL = corpus/control

recur:
	git clone https://github.com/douglasbagnall/recur.git

recur/local.mak: recur
	cp $@.example.x86_64 $@

recur/charmodel.so: recur/local.mak
	cd recur && git pull
	cd recur && make charmodel.so

charmodel.so: recur/charmodel.so
	ln -s $^ $@

pgm-clean:
	rm -rf images
	mkdir images

pyc-clean:
	rm -f *.pyc mappings/*.pyc

.PHONY: all pgm-clean all-mappings answers-rev

.SECONDARY: recur recur/local.mak

mappings/nl.py:
	./corpus-utils -m nl -d --decompose-caps > $@

mappings/en.py:
	./corpus-utils -m en -d --decompose-caps > $@

mappings/gr.py:
	./corpus-utils -m gr -d --decompose-caps --collapse-latin > $@

all-mappings: mappings/gr.py mappings/en.py  mappings/es.py mappings/nl.py

answers-rev:
	make-answers.sh
