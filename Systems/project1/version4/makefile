
mallocTestVersion4: mallocTestVersion4.o dumalloc.o
	gcc mallocTestVersion4.o dumalloc.o -o mallocTestVersion4 -lm

mallocTestVersion4.o: mallocTestVersion4.c dumalloc.h
	gcc mallocTestVersion4.c -c

dumalloc.o: dumalloc.c dumalloc.h
	gcc dumalloc.c -c

clean:
	rm -f *.o 
	rm -f mallocTestVersion4

# Path: project1/version4/mallocTestVersion4.c
