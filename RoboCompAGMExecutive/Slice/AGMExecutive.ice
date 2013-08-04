#ifndef ROBOCOMPAGMEXECUTIVE_ICE
#define ROBOCOMPAGMEXECUTIVE_ICE

#include <AGMWorldModel.ice>
#include <Planning.ice>

module RoboCompAGMExecutive
{
	interface AGMExecutive
	{
		// Activation and deactivation
		void activate();
		void deactivate();
		void reset();

		// For agents
		bool modificationProposal(RoboCompAGMWorldModel::ModelEvent modification);

		// For setting the mission
		void setMission();

		/// For visualization purposes
		void getData(out RoboCompAGMWorldModel::World world, out RoboCompAGMWorldModel::World target, out RoboCompPlanning::Plan plan);
		void broadcastModel();
	};

	interface AGMExecutiveVisualizationTopic
	{
		void update(RoboCompAGMWorldModel::World world, RoboCompAGMWorldModel::World target, RoboCompPlanning::Plan plan);
	};

	interface AGMExecutiveTopic
	{
		void modelModified(RoboCompAGMWorldModel::ModelEvent modification);
		void modelUpdated(RoboCompAGMWorldModel::WorldNode modification);
	};

};

#endif
