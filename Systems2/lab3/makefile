parallel: primeParallels.o 
	g++ primeParallels.cpp -fopenmp -o parallel

primeParallels.o: primeParallels.cpp
	g++ -c primeParallels.cpp -fopenmp -o primeParallels.o

clean:
	rm -f *.o 
	rm -f parallel