//
// main.cc
// routing
//
// Created by tomaszbrue on 27/01/15.
// Copyright (c) 2015 Thomas Brüggemann. All rights reserved.
//

#include <iostream>
#include "config.h"
#include "mongo/client/dbclient.h"

using namespace std;
using mongo::BSONElement;
using mongo::BSONObj;
using mongo::BSONObjBuilder;

int main(int argc, const char * argv[])
{
	// init mongodb client
	mongo::client::initialize();
	try
	{
		// connect to mongodb
		std::string errmsg;
		mongo::ConnectionString cs = mongo::ConnectionString::parse(MONGO_CONN_URL, errmsg);
		if(!cs.isValid())
		{
			cout << "error parsing url: " << errmsg << endl;
			return EXIT_FAILURE;
		}

		boost::scoped_ptr<mongo::DBClientBase> conn(cs.connect(errmsg));
		if(!conn)
		{
			cout << "couldn't connect: " << errmsg << endl;
			return EXIT_FAILURE;
		}
		
		cout << "connected ok" << endl;
	}
	catch(const mongo::DBException &e)
	{
		cout << "caught " << e.what() << endl;
	}

	return EXIT_SUCCESS;
}