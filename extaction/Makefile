PREFIX?=/usr/local
CC	= g++-4.9
CFLAGS	= -Wall -g -std=c++11 -O3
LDFLAGS	= -L${PREFIX}/lib -pthread -lboost_system -lboost_thread
EXE = routing
OBJ = aisgraph.o
INC =

all: $(EXE)

clean:
	rm -f *~ *.o core $(EXE)
	rm -rf *.dSYM

$(EXE): % : %.o $(OBJ)
	$(CC) -o build/$@ $@.o $(OBJ) $(LDFLAGS)

%.o: %.cpp $(INC)
	$(CC) $(CFLAGS) -c $<