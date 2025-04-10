exe: dumalloc.o mallocTestVersion1.o
	gcc dumalloc.o mallocTestVersion1.o -o exe

dumalloc.o: dumalloc.c dumalloc.h
	gcc dumalloc.c -c

mallocTestVersion1.o: mallocTestVersion1.c 
	gcc mallocTestVersion1.c -c

clean:
	rm -f *.o exe
