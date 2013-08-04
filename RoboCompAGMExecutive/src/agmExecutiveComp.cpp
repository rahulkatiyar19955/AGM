/*
 *    Copyright (C) 2006-2011 by RoboLab - University of Extremadura
 *
 *    This file is part of RoboComp
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
/** \mainpage RoboComp::gualzru_executiveComp
 *
 * \section intro_sec Introduction
 *
 * The gualzru_executiveComp component...
 *
 * \section interface_sec Interface
 *
 * gualzru_executiveComp interface...
 *
 * \section install_sec Installation
 *
 * \subsection install1_ssec Software depencences
 * gualzru_executiveComp ...
 *
 * \subsection install2_ssec Compile and install
 * cd gualzru_executiveComp
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
 * The configuration file gualzru_executiveComp/etc/config ...
 * </p>
 *
 * \subsection execution_ssec Execution
 *
 * Just: "${PATH_TO_BINARY}/gualzru_executiveComp --Ice.Config=${PATH_TO_CONFIG_FILE}"
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
#include <GualzruCommonBehavior.h>
#include <GualzruBehavior.h>


using namespace std;
using namespace RoboCompExecutive;

using namespace RoboCompGualzruBehavior;
using namespace RoboCompGualzruCommonBehavior;


class gualzru_executiveComp : public RoboComp::Application
{
private:
	void initialize();
public:
	virtual int run(int, char*[]);
};

void gualzru_executiveComp::initialize()
{
	// Config file properties read example
	// configGetString( PROPERTY_NAME_1, property1_holder, PROPERTY_1_DEFAULT_VALUE );
	// configGetInt( PROPERTY_NAME_2, property1_holder, PROPERTY_2_DEFAULT_VALUE );
}

int gualzru_executiveComp::run(int argc, char* argv[])
{
#ifdef USE_QTGUI
	QApplication a(argc, argv);  // GUI application
#else
	QCoreApplication a(argc, argv);  // NON-GUI application
#endif
	int status=EXIT_SUCCESS;


	
	RoboCompPlanning::PlanningPrx planning_proxy;
	RoboCompSpeech::SpeechPrx speech_proxy;
	RoboCompInnerModelManager::InnerModelManagerPrx immanager_proxy;

	string proxy;

	initialize();



	try
	{
		proxy = getProxyString("PlanningProxy");
		planning_proxy = RoboCompPlanning::PlanningPrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
		if (!planning_proxy)
		{
			rInfo(QString("Error loading proxy!"));
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
		proxy = getProxyString("SpeechProxy");
		speech_proxy = RoboCompSpeech::SpeechPrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
		if (!speech_proxy)
		{
			rInfo(QString("Error loading proxy!"));
			return EXIT_FAILURE;
		}
	}
	catch(const Ice::Exception& ex)
	{
		cout << "[" << PROGRAM_NAME << "]: Exception: " << ex << endl;
		return EXIT_FAILURE;
	}
	rInfo("SpeechProxy initialized Ok!");

	try
	{
		proxy = getProxyString("InnerModelManagerProxy");
		immanager_proxy = RoboCompInnerModelManager::InnerModelManagerPrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
		if (!immanager_proxy)
		{
			rInfo(QString("Error loading proxy!"));
			return EXIT_FAILURE;
		}
	}
	catch(const Ice::Exception& ex)
	{
		cout << "[" << PROGRAM_NAME << "]: Exception: " << ex << endl;
		return EXIT_FAILURE;
	}
	rInfo("InnerModelManagerProxy initialized Ok!");


	RoboCompExecutive::ExecutiveTopicPrx executiveTopic;
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
				topic = topicManager->retrieve("ExecutiveTopic");
			}
			catch (const IceStorm::NoSuchTopic&)
			{
				try
				{
					topic = topicManager->create("ExecutiveTopic");
				}
				catch (const IceStorm::TopicExists&)
				{
					// Another client created the topic.
				}
			}
		}
		Ice::ObjectPrx pub = topic->getPublisher()->ice_oneway();
		executiveTopic = RoboCompExecutive::ExecutiveTopicPrx::uncheckedCast(pub);
	}
	catch (const Ice::Exception& ex)
	{
		rInfo(QString("Can't connect to IceStorm!"));
		return EXIT_FAILURE;
	}

	RoboCompExecutive::ExecutiveVisualizationTopicPrx executiveVisualizationTopic;
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
				topic = topicManager->retrieve("ExecutiveVisualizationTopic");
			}
			catch (const IceStorm::NoSuchTopic&)
			{
				try
				{
					topic = topicManager->create("ExecutiveVisualizationTopic");
				}
				catch (const IceStorm::TopicExists&)
				{
					// Another client created the topic.
				}
			}
		}
		Ice::ObjectPrx pub = topic->getPublisher()->ice_oneway();
		executiveVisualizationTopic = RoboCompExecutive::ExecutiveVisualizationTopicPrx::uncheckedCast(pub);
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
	parameters.immanager                   = immanager_proxy;
	parameters.executiveTopic              = executiveTopic;
	parameters.executiveVisualizationTopic = executiveVisualizationTopic;

	
	/// Read PDDLPath variable
	configGetString("PDDLPath", parameters.pddlPath);

	/// Read AGMBDPath variable
	configGetString("AGMBDPath", parameters.agmbdPath);

	/// Read the PDDL file and store it in a string
	std::ifstream t(parameters.pddlPath.c_str());
	std::stringstream buffer;
	buffer << t.rdbuf();
	parameters.grammarPDDLString = buffer.str();

	/// Create AGM object
	parameters.agm = new AGM(parameters.pddlPath, parameters.agmbdPath);


	/// Get proxies for agents
	AGMAgentVector agents = parameters.agm->table.agents;
	for (uint i=0; i<agents.size(); i++)
	{
		GualzruCommonBehaviorPrx behavior_proxy;
		try
		{
			proxy = getProxyString(agents[i].getName());
			behavior_proxy = GualzruCommonBehaviorPrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
			if (!behavior_proxy)
			{
				rInfo(QString("Error loading proxy!"));
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


/*

	
	parameters.planning                    = planning_proxy;
	parameters.speech                      = speech_proxy;
	parameters.immanager                   = immanager_proxy;
	parameters.executiveTopic              = executiveTopic;
	parameters.executiveVisualizationTopic = executiveVisualizationTopic;
	parameters.behaviorPitchRoll           = behaviorPitchRoll_proxy;
	parameters.behaviorSaccade             = behaviorSaccade_proxy;
	parameters.behaviorUnknown             = behaviorUnknown_proxy;
	parameters.behaviorDistance            = behaviorDistance_proxy;
	parameters.behaviorYaw                 = behaviorYaw_proxy;

*/



printf("%s: %s: %d\n", __FILE__, __PRETTY_FUNCTION__, __LINE__);
	Worker *worker = new Worker(parameters);
printf("%s: %s: %d\n", __FILE__, __PRETTY_FUNCTION__, __LINE__);

	/// First part
	proxy = getProxyString("IceStormProxy");
	Ice::ObjectPrx obj = communicator()->stringToProxy(proxy);
	IceStorm::TopicManagerPrx topicManager = IceStorm::TopicManagerPrx::checkedCast(obj);
	Ice::ObjectAdapterPtr adapterT = communicator()->createObjectAdapter("GualzruBehaviorTopic");
	GualzruBehaviorTopicPtr behaviorTopic = new GualzruBehaviorTopicI(worker);
	Ice::ObjectPrx proxyT = adapterT->addWithUUID(behaviorTopic)->ice_oneway();
	IceStorm::TopicPrx topic;
	try
	{
		topic = topicManager->retrieve("GualzruBehavior");
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
		Ice::ObjectAdapterPtr adapter = communicator()->createObjectAdapter("gualzruexecutive");
		ExecutiveI *executiveI = new ExecutiveI(worker);
		adapter->add(executiveI, communicator()->stringToIdentity("gualzruexecutive"));
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
	gualzru_executiveComp app;

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
