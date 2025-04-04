
mallocTestVersion4: mallocTestVersion4.o dumalloc.o
	gcc mallocTestVersion4.o dumalloc.o -o mallocTestVersion4 

mallocTestVersion4.o: mallocTestVersion4.c dumalloc.h
	gcc mallocTestVersion4.c -c

dumalloc.o: dumalloc.c dumalloc.h
	gcc dumalloc.c -c

clean:
	rm -f *.0 
	rm -f mallocTestVersion4

