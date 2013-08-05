#ifndef ROBOCOMPAGMAGENTS_ICE
#define ROBOCOMPAGMAGENTS_ICE

#include <AGMWorldModel.ice>

module RoboCompAGMAgent
{
	interface AGMAgentTopic
	{
		void modificationProposal(RoboCompAGMWorldModel::Event modification);
		void update(RoboCompAGMWorldModel::Node nodeModification);
	};
};

#endif