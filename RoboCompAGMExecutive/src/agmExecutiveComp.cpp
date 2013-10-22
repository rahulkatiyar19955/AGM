/*
 *    Copyright (C) 2013 by Luis J. Manso - University of Extremadura
 *
 *    This file is part of AGM (Active Grammar-based Modeling)
 *
 *    RoboComp is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    RoboComp is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
 */

/** \mainpage AGMExecutive
 *
 * \section intro_sec Introduction
 *
 * The AGMExecutive
 *
 * \section interface_sec Interface
 *
 * AGMExecutive interface...
 *
 * \section install_sec Installation
 *
 * \subsection install1_ssec Software depencences
 * AGMExecutive ...
 *
 * \subsection install2_ssec Compile and install
 * cd AGMExecutive
 * <br>
 * cmake . && make
 * <br>
 * To install:
 * <br>
 * sudo make install
 *
 * \section guide_sec User guide
 *
 * \subsection config_ssec Configuration file
 *
 * <p>
 * The configuration file AGMExecutive/etc/config ...
 * </p>
 *
 * \subsection execution_ssec Execution
 *
 * Just: "${PATH_TO_BINARY}/AGMExecutive --Ice.Config=${PATH_TO_CONFIG_FILE}"
 *
 * \subsection running_ssec Once running
 *
 * ...
 *
 */
#include <QtCore>
#include <QtGui>

#include <Ice/Ice.h>
#include <Ice/Application.h>

#include <rapplication/rapplication.h>
#include <qlog/qlog.h>

#include <fstream>

#include "config.h"
#include "worker.h"
#include <executiveI.h>

#include <Planning.h>
#include <AGMCommonBehavior.h>
#include <AGMAgent.h>
#include <AGMExecutive.h>
#include <AGMWorldModel.h>

#include "config.h"

using namespace std;
using namespace RoboCompAGMExecutive;
using namespace RoboCompAGMCommonBehavior;
using namespace RoboCompAGMAgent;


#define PROGRAM_NAME    "agmexecutive"
#define SERVER_FULL_NAME   "AGMExecutive"


class AGMExecutiveMain : public RoboComp::Application
{
private:
	void initialize() {}
public:
	virtual int run(int, char*[]);
};

int AGMExecutiveMain::run(int argc, char* argv[])
{
	QCoreApplication a(argc, argv);  // NON-GUI application
	int status=EXIT_SUCCESS;
	
	RoboCompPlanning::PlanningPrx pelea_proxy;
	RoboCompPlanning::PlanningPrx planning_proxy;
	RoboCompSpeech::SpeechPrx speech_proxy;

	string proxy;

	initialize();

	try
	{
		proxy = getProxyString("PlanningProxy");
		planning_proxy = RoboCompPlanning::PlanningPrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
		if (!planning_proxy)
		{
			rInfo(QString("Error loading planningproxy!"));
			return EXIT_FAILURE;
		}
	}
	catch(const Ice::Exception& ex)
	{
		cout << "[" << PROGRAM_NAME << "]: Exception: " << ex << endl;
		return EXIT_FAILURE;
	}
	rInfo("PlanningProxy initialized Ok!");

	try
	{
		proxy = getProxyString("PeleaProxy");
		pelea_proxy = RoboCompPlanning::PlanningPrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
		if (!pelea_proxy)
		{
			rInfo(QString("Error loading peleaproxy!"));
			return EXIT_FAILURE;
		}
	}
	catch(const Ice::Exception& ex)
	{
		cout << "[" << PROGRAM_NAME << "]: Exception: " << ex << endl;
		return EXIT_FAILURE;
	}
	rInfo("PeleaProxy initialized Ok!");

	try
	{
		proxy = getProxyString("SpeechProxy");
		speech_proxy = RoboCompSpeech::SpeechPrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
		if (!speech_proxy)
		{
			rInfo(QString("Error loading speech proxy!"));
			return EXIT_FAILURE;
		}
	}
	catch(const Ice::Exception& ex)
	{
		cout << "[" << PROGRAM_NAME << "]: Exception: " << ex << endl;
		return EXIT_FAILURE;
	}
	rInfo("SpeechProxy initialized Ok!");


	RoboCompAGMExecutive::AGMExecutiveTopicPrx executiveTopic;
	try
	{
		proxy = getProxyString("IceStormProxy");
		Ice::ObjectPrx obj = communicator()->stringToProxy(proxy);
		IceStorm::TopicManagerPrx topicManager = IceStorm::TopicManagerPrx::checkedCast(obj);
		IceStorm::TopicPrx topic;
		while (!topic)
		{
			try
			{
				topic = topicManager->retrieve("AGMExecutiveTopic");
			}
			catch (const IceStorm::NoSuchTopic&)
			{
				try
				{
					topic = topicManager->create("AGMExecutiveTopic");
				}
				catch (const IceStorm::TopicExists&)
				{
					// Another client created the topic.
				}
			}
		}
		Ice::ObjectPrx pub = topic->getPublisher()->ice_oneway();
		executiveTopic = RoboCompAGMExecutive::AGMExecutiveTopicPrx::uncheckedCast(pub);
	}
	catch (const Ice::Exception& ex)
	{
		rInfo(QString("Can't connect to IceStorm!"));
		return EXIT_FAILURE;
	}

	RoboCompAGMExecutive::AGMExecutiveVisualizationTopicPrx executiveVisualizationTopic;
	try
	{
		proxy = getProxyString("IceStormProxy");
		Ice::ObjectPrx obj = communicator()->stringToProxy(proxy);
		IceStorm::TopicManagerPrx topicManager = IceStorm::TopicManagerPrx::checkedCast(obj);
		IceStorm::TopicPrx topic;
		while (!topic)
		{
			try
			{
				topic = topicManager->retrieve("AGMExecutiveVisualizationTopic");
			}
			catch (const IceStorm::NoSuchTopic&)
			{
				try
				{
					topic = topicManager->create("AGMExecutiveVisualizationTopic");
				}
				catch (const IceStorm::TopicExists&)
				{
					// Another client created the topic.
				}
			}
		}
		Ice::ObjectPrx pub = topic->getPublisher()->ice_oneway();
		executiveVisualizationTopic = RoboCompAGMExecutive::AGMExecutiveVisualizationTopicPrx::uncheckedCast(pub);
	}
	catch (const Ice::Exception& ex)
	{
		rInfo(QString("Can't connect to IceStorm!"));
		return EXIT_FAILURE;
	}

	WorkerParameters parameters;


	/// Fixed proxies
	parameters.planning                    = planning_proxy;
	parameters.speech                      = speech_proxy;
	parameters.executiveTopic              = executiveTopic;
	parameters.executiveVisualizationTopic = executiveVisualizationTopic;
	parameters.pelea                       = pelea_proxy;
	
	/// Read PDDLPath variable
	configGetString("PDDLPath", parameters.pddlPath);
	/// Read PDDLCompletePath variable
	configGetString("PDDLCompletePath", parameters.pddlCompletePath);
	/// Read AGMBDPath variable
	configGetString("AGMBDPath", parameters.agmbdPath);

	/// Read the PDDL file and store it in a string
	{
		std::ifstream t(parameters.pddlPath.c_str());
		std::stringstream buffer;
		buffer << t.rdbuf();
		parameters.grammarPDDLString = buffer.str();
	}
	/// Read the Complete PDDL file and store it in a string
	{
		std::ifstream t(parameters.pddlCompletePath.c_str());
		std::stringstream buffer;
		buffer << t.rdbuf();
		parameters.grammarCompletePDDLString = buffer.str();
	}

	/// Create AGM object
	parameters.agm = new AGM(parameters.pddlPath, parameters.agmbdPath);


	/// Get proxies for agents
	AGMAgentVector agents = parameters.agm->table.agents;
	for (uint i=0; i<agents.size(); i++)
	{
		AGMCommonBehaviorPrx behavior_proxy;
		try
		{
			proxy = getProxyString(agents[i].getName());
			behavior_proxy = AGMCommonBehaviorPrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
			if (!behavior_proxy)
			{
				printf("%s\n", agents[i].getName().c_str());
				printf("%s\n", agents[i].getName().c_str());
				rInfo(QString("Error loading behavior proxy!"));
				return EXIT_FAILURE;
			}
		}
		catch(const Ice::Exception& ex)
		{
			cout << "[" << PROGRAM_NAME << "]: Exception: " << ex << endl;
			return EXIT_FAILURE;
		}

		parameters.agentProxies[agents[i].getName()] = behavior_proxy;
		printf("Agent %s initialized ok\n", agents[i].getName().c_str());
	}

	Worker *worker = new Worker(parameters);

	/// First part
	proxy = getProxyString("IceStormProxy");
	Ice::ObjectPrx obj = communicator()->stringToProxy(proxy);
	IceStorm::TopicManagerPrx topicManager = IceStorm::TopicManagerPrx::checkedCast(obj);
	Ice::ObjectAdapterPtr adapterT = communicator()->createObjectAdapter("AGMAgentTopic");
	AGMAgentTopicPtr agentTopic = new AGMAgentTopicI(worker);
	Ice::ObjectPrx proxyT = adapterT->addWithUUID(agentTopic)->ice_oneway();
	IceStorm::TopicPrx topic;
	try
	{
		topic = topicManager->retrieve("AGMAgentTopic");
		IceStorm::QoS qos;
		topic->subscribeAndGetPublisher(qos, proxyT);
	}
	catch (const IceStorm::NoSuchTopic&)
	{
		printf("Error! No topic found!\n");
	}
	adapterT->activate();

	try
	{
		Ice::ObjectAdapterPtr adapter = communicator()->createObjectAdapter("AGMExecutive");
		AGMExecutiveI *executiveI = new AGMExecutiveI(worker);
		adapter->add(executiveI, communicator()->stringToIdentity("agmexecutive"));
		adapter->activate();

#ifdef USE_QTGUI
		a.setQuitOnLastWindowClosed(true);
#endif
		worker->start();
		a.exec();
		status = EXIT_SUCCESS;
	}
	catch(const Ice::Exception& ex)
	{
		status = EXIT_FAILURE;
		cout << "[" << PROGRAM_NAME << "]: Exception raised on main thread: " << endl;
		cout << ex;
#ifdef USE_QTGUI
		a.quit();
#endif
	}

	/// Second part
	communicator()->waitForShutdown();
	topic->unsubscribe(proxyT);

	
	return status;
}

int main(int argc, char* argv[])
{
	bool hasConfig = false;
	string arg;
	AGMExecutiveMain app;

	// Search in argument list for --Ice.Config= argument
	for (int i = 1; i < argc; ++i)
	{
		arg = argv[i];
		if ( arg.find ( "--Ice.Config=", 0 ) != string::npos )
			hasConfig = true;
	}

	if ( hasConfig )
		return app.main( argc, argv );
	else
		return app.main(argc, argv, "config"); // "config" is the default config file name
}
