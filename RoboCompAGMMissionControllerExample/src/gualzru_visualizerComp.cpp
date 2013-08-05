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
#include <QtCore>
#include <QtGui>

#include <Ice/Ice.h>
#include <Ice/Application.h>

#include <rapplication/rapplication.h>
#include <qlog/qlog.h>

#include <AGMExecutive.h>

#include "config.h"
#include "worker.h"
#include <executiveTopicI.h>
#include <executiveVisualizationTopicI.h>


using namespace std;


class gualzru_behaviorVisualizerComp : public RoboComp::Application
{
private:
	void initialize() {}

public:
	virtual int run(int, char*[]);
};

int gualzru_behaviorVisualizerComp::run(int argc, char* argv[])
{
#ifdef USE_QTGUI
	QApplication a(argc, argv);  // GUI application
#else
	QCoreApplication a(argc, argv);  // NON-GUI application
#endif
	int status=EXIT_SUCCESS;


	string proxy;
	initialize();

	/// Behavior topic
	RoboCompAGMAgent::AGMAgentTopicPrx behaviorTopic;
	try
	{
		Ice::ObjectPrx obj = communicator()->stringToProxy("IceStorm/TopicManager:tcp -p 9999");
		IceStorm::TopicManagerPrx topicManager = IceStorm::TopicManagerPrx::checkedCast(obj);
		IceStorm::TopicPrx topic;
		while (!topic)
		{
			try
			{
				topic = topicManager->retrieve("AGMAgentTopic");
			}
			catch (const IceStorm::NoSuchTopic&)
			{
				try
				{
					topic = topicManager->create("AGMAgentTopic");
				}
				catch (const IceStorm::TopicExists&)
				{
					// Another client created the topic.
				}
			}
		}
		Ice::ObjectPrx pub = topic->getPublisher()->ice_oneway();
		behaviorTopic = RoboCompAGMAgent::AGMAgentTopicPrx::uncheckedCast(pub);
	}
	catch (const Ice::Exception& ex)
	{
		rInfo(QString("Can't connect to IceStorm!"));
		return EXIT_FAILURE;
	}

	RoboCompAGMExecutive::AGMExecutivePrx executive_proxy;
	try
	{
		proxy = getProxyString("AGMExecutiveProxy");
		executive_proxy = AGMExecutivePrx::uncheckedCast( communicator()->stringToProxy( proxy ) );
		if (!executive_proxy)
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
	rInfo("ExecutiveProxy initialized Ok!");

	Worker *worker = new Worker(behaviorTopic, executive_proxy);

	/// First topic A
	Ice::ObjectPrx objA = communicator()->stringToProxy("IceStorm/TopicManager:tcp -p 9999");
	IceStorm::TopicManagerPrx topicManagerA = IceStorm::TopicManagerPrx::checkedCast(objA);
	Ice::ObjectAdapterPtr adapterT = communicator()->createObjectAdapter("AGMExecutiveTopic");
	AGMExecutiveTopicPtr executiveTopic = new AGMExecutiveTopicI(worker);
	Ice::ObjectPrx proxyT = adapterT->addWithUUID(executiveTopic)->ice_oneway();
	IceStorm::TopicPrx topic;
	try
	{
		topic = topicManagerA->retrieve("AGMExecutiveTopic");
		IceStorm::QoS qos;
		topic->subscribeAndGetPublisher(qos, proxyT);
	}
	catch (const IceStorm::NoSuchTopic&)
	{
		printf("Error! No topic found!\n");
	}
	adapterT->activate();
	/// Second topic A
	Ice::ObjectPrx objB = communicator()->stringToProxy("IceStorm/TopicManager:tcp -p 9999");
	IceStorm::TopicManagerPrx topicManagerB = IceStorm::TopicManagerPrx::checkedCast(objB);
	Ice::ObjectAdapterPtr adapterVT = communicator()->createObjectAdapter("AGMExecutiveVisualizationTopic");
	AGMExecutiveVisualizationTopicPtr executiveVisualizationTopic = new AGMExecutiveVisualizationTopicI(worker);
	Ice::ObjectPrx proxyVT = adapterVT->addWithUUID(executiveVisualizationTopic)->ice_oneway();
	IceStorm::TopicPrx topicV;
	try
	{
		topicV = topicManagerB->retrieve("AGMExecutiveVisualizationTopic");
		IceStorm::QoS qos;
		topicV->subscribeAndGetPublisher(qos, proxyVT);
	}
	catch (const IceStorm::NoSuchTopic&)
	{
		printf("Error! No topic found!\n");
	}
	adapterVT->activate();



#ifdef USE_QTGUI
	a.setQuitOnLastWindowClosed( true );
#endif
	a.exec();
	status = EXIT_SUCCESS;
	
	/// Second part
	communicator()->waitForShutdown();
	topic->unsubscribe(proxyT);

	return status;
}

int main(int argc, char* argv[])
{
	bool hasConfig = false;
	string arg;
	gualzru_behaviorVisualizerComp app;

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
