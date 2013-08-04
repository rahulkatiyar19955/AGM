#ifndef ROBOCOMPAGMAGENTS_ICE
#define ROBOCOMPAGMAGENTS_ICE

#include <AGMWorldModel.ice>

module RoboCompAGMAgents
{
	interface AgentsTopic
	{
		void modificationProposal(RoboCompWorldModel::ModelEvent modification);
		void update(RoboCompWorldModel::GualzruWorldNode nodeModification);
	};
};

#endif