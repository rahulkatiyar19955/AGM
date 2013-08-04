#ifndef ROBOCOMPAGMEXECUTIVE_ICE
#define ROBOCOMPAGMEXECUTIVE_ICE

#include <AGMWorldModel.ice>
#include <Planning.ice>

module RoboCompAGMExecutive
{
	interface AGMExecutive
	{
		void activate();
		void deactivate();
		void reset();
		void broadcastModel();

		bool modificationProposal(RoboCompWorldModel::ModelEvent modification);

		/// For visualization purposes
		void getData(out RoboCompWorldModel::GualzruWorld world, out RoboCompWorldModel::GualzruWorld target, out RoboCompPlanning::Plan plan);
	};

	interface AGMExecutiveVisualizationTopic
	{
		void update(RoboCompWorldModel::GualzruWorld world, RoboCompWorldModel::GualzruWorld target, RoboCompPlanning::Plan plan);
	};

	interface AGMExecutiveTopic
	{
		void modelModified(RoboCompWorldModel::ModelEvent modification);
		void modelUpdated(RoboCompWorldModel::GualzruWorldNode modification);
	};

};

#endif
