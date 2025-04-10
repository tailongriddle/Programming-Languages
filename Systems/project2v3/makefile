Simulation: Simulation.o Memory.o Cache.o Sets.o Block.o AddressDecoder.o PerformanceCounter.o
	g++ Simulation.o Memory.o Cache.o Sets.o Block.o AddressDecoder.o PerformanceCounter.o -o Simulation
Simulation.o:  Simulation.cc   Memory.h  Cache.h  Sets.h  Block.h  AddressDecoder.h  PerformanceCounter.h
	g++ -c  Simulation.cc -o Simulation.o
Memory.o:  Memory.cc  Memory.h
	g++ -c  Memory.cc -o Memory.o
Cache.o:  Cache.cc  Cache.h  Sets.h  Block.h Memory.h AddressDecoder.h PerformanceCounter.h
	g++ -c  Cache.cc -o Cache.o
Sets.o:  Sets.cc  Sets.h  Block.h PerformanceCounter.h
	g++ -c  Sets.cc -o Sets.o
Block.o:  Block.cc  Block.h Memory.h
	g++ -c  Block.cc -o Block.o
AddressDecoder.o:  AddressDecoder.cc  AddressDecoder.h Memory.h
	g++ -c  AddressDecoder.cc -o AddressDecoder.o
PerformanceCounter.o:  PerformanceCounter.cc  PerformanceCounter.h
	g++ -c  PerformanceCounter.cc -o PerformanceCounter.o
clean:
	rm -f *.o Simulation