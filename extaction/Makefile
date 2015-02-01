PREFIX?=/usr/local
CC	= g++-4.9
CFLAGS	= -Wall -g -I${PREFIX}/include/mongo 
LDFLAGS	= -L${PREFIX}/lib -pthread -lmongoclient -lboost_thread -lboost_system -lboost_regex
EXE = extraction
OBJ =
INC =

all: $(EXE)

clean:
	rm -f *~ *.o core $(EXE)
	rm -rf *.dSYM

$(EXE): % : %.o $(OBJ)
	$(CC) -o build/$@ $@.o $(OBJ) $(LDFLAGS)

%.o: %.cpp $(INC)
	$(CC) $(CFLAGS) -c $<