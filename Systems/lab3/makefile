
mallocTest: mallocTest.o duMalloc.o
	gcc mallocTest.o duMalloc.o -o mallocTest 

mallocTest.o: mallocTest.c duMalloc.h
	gcc mallocTest.c -c

duMalloc.o: duMalloc.c duMalloc.h
	gcc duMalloc.c -c

clean:
	rm -f *.0 
	rm -f mallocTest